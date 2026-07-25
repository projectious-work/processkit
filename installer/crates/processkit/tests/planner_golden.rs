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
