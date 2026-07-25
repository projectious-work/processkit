use serde_json::Value;
use std::path::PathBuf;
use std::process::Command;

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/plans")
        .join(name)
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
