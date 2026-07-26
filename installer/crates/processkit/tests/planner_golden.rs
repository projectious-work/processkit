use serde_json::Value;
use sha2::{Digest, Sha256};
use std::path::PathBuf;
use std::process::Command;

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/plans")
        .join(name)
}

fn copy_tree(source: &std::path::Path, target: &std::path::Path) {
    std::fs::create_dir_all(target).unwrap();
    for entry in std::fs::read_dir(source).unwrap() {
        let entry = entry.unwrap();
        let destination = target.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() {
            copy_tree(&entry.path(), &destination);
        } else {
            std::fs::copy(entry.path(), destination).unwrap();
        }
    }
}

fn set_fixture_release(distribution: &std::path::Path, version: &str, payload: Option<&str>) {
    let manifest = distribution.join(".processkit/installer/distribution.yaml");
    let mut text = std::fs::read_to_string(&manifest).unwrap();
    text = text.replace("version: 0.0.0-test", &format!("version: {version}"));
    if let Some(payload) = payload {
        std::fs::write(distribution.join("payload/hello.txt"), payload).unwrap();
    } else {
        text = format!(
            "apiVersion: processkit.projectious.work/distribution/v1alpha1\n\
             kind: Distribution\n\
             metadata:\n\
             \u{20}\u{20}name: fixture-processkit\n\
             \u{20}\u{20}version: {version}\n\
             spec:\n\
             \u{20}\u{20}installer:\n\
             \u{20}\u{20}\u{20}\u{20}protocol: processkit.projectious.work/installer/v1alpha1\n\
             \u{20}\u{20}components: []\n\
             \u{20}\u{20}profiles:\n\
             \u{20}\u{20}\u{20}\u{20}managed:\n\
             \u{20}\u{20}\u{20}\u{20}\u{20}\u{20}include: []\n"
        );
    }
    std::fs::write(&manifest, &text).unwrap();
    let manifest_sha256 = format!("{:x}", Sha256::digest(text.as_bytes()));
    let descriptor = distribution.join(".processkit/installer/release-descriptor.json");
    let mut value: Value = serde_json::from_slice(&std::fs::read(&descriptor).unwrap()).unwrap();
    value["distribution"]["manifestSha256"] = Value::String(manifest_sha256);
    std::fs::write(descriptor, serde_json::to_vec_pretty(&value).unwrap()).unwrap();
}

fn plan(name: &str) -> std::process::Output {
    let case = fixture(name);
    Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "plan",
            "--root",
            case.join("project").to_str().unwrap(),
            "--distribution",
            case.join("distribution").to_str().unwrap(),
            "--profile",
            "managed",
            "--format",
            "json",
        ])
        .output()
        .expect("planner command starts")
}

fn assert_golden(name: &str) {
    let first = plan(name);
    let second = plan(name);
    assert!(
        first.status.success(),
        "{}",
        String::from_utf8_lossy(&first.stderr)
    );
    assert_eq!(
        first.stdout, second.stdout,
        "plan output must be deterministic"
    );
    let actual: Value = serde_json::from_slice(&first.stdout).unwrap();
    let expected: Value =
        serde_json::from_slice(&std::fs::read(fixture(name).join("expected.json")).unwrap())
            .unwrap();
    assert_eq!(actual, expected);
}

#[test]
fn empty_plan_is_golden_and_non_mutating() {
    let project = fixture("empty").join("project");
    let before = std::fs::read_dir(&project).unwrap().count();
    assert_golden("empty");
    assert_eq!(std::fs::read_dir(project).unwrap().count(), before);
}

#[test]
fn existing_managed_file_is_a_golden_conflict() {
    assert_golden("conflict");
}

#[test]
fn traversal_destination_is_a_golden_invalid_plan() {
    assert_golden("invalid-destination");
}

#[test]
fn install_writes_owned_state_and_payload() {
    let root = std::env::temp_dir().join(format!(
        "processkit-installer-test-{}-{}",
        std::process::id(),
        "install"
    ));
    std::fs::create_dir_all(&root).unwrap();
    let case = fixture("empty");
    let output = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "install",
            "--root",
            root.to_str().unwrap(),
            "--distribution",
            case.join("distribution").to_str().unwrap(),
            "--profile",
            "managed",
            "--yes",
            "--json",
        ])
        .output()
        .expect("install command starts");
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let state: Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(state["release"]["name"], "fixture-processkit");
    assert_eq!(state["ownedPaths"].as_array().unwrap().len(), 1);
    assert_eq!(
        std::fs::read_to_string(root.join("payload/hello.txt")).unwrap(),
        "fixture payload\n"
    );
    assert!(root.join(".processkit/state.json").is_file());
    let verified = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args(["verify", "--root", root.to_str().unwrap(), "--json"])
        .output()
        .expect("verify command starts");
    assert!(
        verified.status.success(),
        "{}",
        String::from_utf8_lossy(&verified.stderr)
    );
    let result: Value = serde_json::from_slice(&verified.stdout).unwrap();
    assert_eq!(result["status"], "verified");

    std::fs::write(root.join("payload/hello.txt"), "user modification\n").unwrap();
    let drifted = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args(["verify", "--root", root.to_str().unwrap(), "--json"])
        .output()
        .expect("drift verify command starts");
    assert_eq!(drifted.status.code(), Some(4));
    let result: Value = serde_json::from_slice(&drifted.stdout).unwrap();
    assert_eq!(result["status"], "drifted");
    assert_eq!(result["errors"][0]["code"], "managed-path-drift");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn recovery_removes_only_digest_matched_interrupted_files() {
    let root = std::env::temp_dir().join(format!(
        "processkit-installer-test-{}-{}",
        std::process::id(),
        "recover"
    ));
    std::fs::create_dir_all(root.join(".processkit/transactions")).unwrap();
    std::fs::write(root.join("created.txt"), "fixture payload\n").unwrap();
    std::fs::write(
        root.join(".processkit/transactions/install-1.json"),
        r#"{
          "apiVersion":"processkit.projectious.work/installer/v1alpha1",
          "transactionId":"install-1",
          "operation":"install",
          "phase":"applying",
          "oldStateSha256":null,
          "newStateSha256":"pending",
          "actions":[{
            "kind":"create",
            "path":"created.txt",
            "oldSha256":null,
            "newSha256":"565b24bc77ebeee74f70f6c608e099956666c3589ed85146fcea7e77d9f25356",
            "stagedPath":null,
            "backupPath":null,
            "createdParents":[],
            "ownership":"managed-three-way",
            "applied":true
          }]
        }"#,
    )
    .unwrap();
    let output = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "recover",
            "--root",
            root.to_str().unwrap(),
            "--yes",
            "--json",
        ])
        .output()
        .expect("recover command starts");
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(!root.join("created.txt").exists());
    assert!(!root
        .join(".processkit/transactions/install-1.json")
        .exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn recovery_repairs_a_process_interrupted_after_rename() {
    let root = std::env::temp_dir().join(format!(
        "processkit-installer-test-{}-{}",
        std::process::id(),
        "interrupted-install"
    ));
    std::fs::create_dir_all(&root).unwrap();
    let case = fixture("empty");
    let interrupted = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .env("PROCESSKIT_INSTALLER_FAIL_AFTER_ACTION", "0")
        .args([
            "install",
            "--root",
            root.to_str().unwrap(),
            "--distribution",
            case.join("distribution").to_str().unwrap(),
            "--profile",
            "managed",
            "--yes",
        ])
        .status()
        .expect("interrupted install starts");
    assert_eq!(interrupted.code(), Some(75));
    assert!(root.join("payload/hello.txt").is_file());

    let recovered = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args(["recover", "--root", root.to_str().unwrap(), "--yes"])
        .status()
        .expect("recovery starts");
    assert!(recovered.success());
    assert!(!root.join("payload/hello.txt").exists());
    assert!(!root.join(".processkit/state.json").exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn uninstall_removes_only_unchanged_managed_files() {
    let root = std::env::temp_dir().join(format!(
        "processkit-installer-test-{}-{}",
        std::process::id(),
        "uninstall"
    ));
    std::fs::create_dir_all(root.join("payload")).unwrap();
    std::fs::create_dir_all(root.join(".processkit")).unwrap();
    std::fs::write(root.join("payload/hello.txt"), "fixture payload\n").unwrap();
    std::fs::write(
        root.join(".processkit/state.json"),
        r#"{
          "apiVersion":"processkit.projectious.work/installer/v1alpha1",
          "release":{"name":"fixture-processkit","version":"0.0.0-test","manifestSha256":"e43f58aec791ca1874fc98d0b208996ac4821de5bf48971733d8d9db0bf6300f"},
          "profiles":["managed"],
          "harnesses":[],
          "ownedPaths":[{
            "path":"payload/hello.txt","component":"payload","operation":"copy/v1","ownership":"managed-three-way",
            "installedSha256":"565b24bc77ebeee74f70f6c608e099956666c3589ed85146fcea7e77d9f25356"
          }]
        }"#,
    )
    .unwrap();
    let output = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "uninstall",
            "--root",
            root.to_str().unwrap(),
            "--yes",
            "--json",
        ])
        .output()
        .expect("uninstall command starts");
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(!root.join("payload/hello.txt").exists());
    assert!(!root.join(".processkit/state.json").exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn update_reconciles_replace_preserve_and_stale_removal() {
    let case = fixture("empty");
    let root = std::env::temp_dir().join(format!(
        "processkit-installer-test-{}-update",
        std::process::id()
    ));
    let release = std::env::temp_dir().join(format!(
        "processkit-installer-release-{}-update",
        std::process::id()
    ));
    std::fs::create_dir_all(&root).unwrap();
    copy_tree(&case.join("distribution"), &release);
    let install = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "install",
            "--root",
            root.to_str().unwrap(),
            "--distribution",
            release.to_str().unwrap(),
            "--yes",
        ])
        .status()
        .unwrap();
    assert!(install.success());

    set_fixture_release(&release, "0.0.1-test", Some("upstream update\n"));
    let update = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "update",
            "--root",
            root.to_str().unwrap(),
            "--distribution",
            release.to_str().unwrap(),
            "--yes",
        ])
        .status()
        .unwrap();
    assert!(update.success());
    assert_eq!(
        std::fs::read_to_string(root.join("payload/hello.txt")).unwrap(),
        "upstream update\n"
    );

    std::fs::write(root.join("payload/hello.txt"), "user update\n").unwrap();
    let preserve = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "update",
            "--root",
            root.to_str().unwrap(),
            "--distribution",
            release.to_str().unwrap(),
            "--yes",
        ])
        .status()
        .unwrap();
    assert!(preserve.success());
    assert_eq!(
        std::fs::read_to_string(root.join("payload/hello.txt")).unwrap(),
        "user update\n"
    );

    set_fixture_release(&release, "0.0.2-test", None);
    let stale = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .args([
            "update",
            "--root",
            root.to_str().unwrap(),
            "--distribution",
            release.to_str().unwrap(),
            "--yes",
        ])
        .status()
        .unwrap();
    assert!(stale.success());
    assert!(
        root.join("payload/hello.txt").is_file(),
        "user-modified stale file must be preserved"
    );
    let state: Value =
        serde_json::from_slice(&std::fs::read(root.join(".processkit/state.json")).unwrap())
            .unwrap();
    assert!(state["ownedPaths"].as_array().unwrap().is_empty());
    std::fs::remove_dir_all(root).unwrap();
    std::fs::remove_dir_all(release).unwrap();
}
