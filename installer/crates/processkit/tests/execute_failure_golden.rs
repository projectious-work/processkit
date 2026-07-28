use serde_json::{json, Value};
use std::fs;
use std::path::Path;
use std::process::Command;

const API_VERSION: &str =
    "processkit.projectious.work/installer/v1alpha1";

fn run_case(name: &str) -> (std::process::Output, Value, Value) {
    let case = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/fixtures/execute-failures")
        .join(name);
    let output = Command::new(env!("CARGO_BIN_EXE_processkit"))
        .current_dir(&case)
        .args(["execute", "--request", "request.json"])
        .output()
        .expect("execute failure fixture");
    let actual = serde_json::from_slice(&output.stdout)
        .expect("execute failure output must be one JSON object");
    let expected = serde_json::from_slice(
        &fs::read(case.join("expected.json"))
            .expect("execute failure expected fixture"),
    )
    .expect("valid expected JSON");
    (output, actual, expected)
}

fn assert_common(output: &std::process::Output, actual: &Value) {
    assert_eq!(output.status.code(), Some(3));
    assert!(output.stderr.is_empty());
    assert_eq!(actual["apiVersion"], API_VERSION);
    assert_eq!(actual["status"], "invalid");
    assert_eq!(actual["changes"], json!([]));
    assert_eq!(actual["conflicts"], json!([]));
    assert_eq!(actual["warnings"], json!([]));
    assert_eq!(actual["errors"].as_array().map(Vec::len), Some(1));
    assert_eq!(actual["errors"][0]["code"], "request-failed");
    assert_eq!(actual["errors"][0]["path"], "");
}

#[test]
fn exact_execute_failures_remain_stable() {
    for name in [
        "unsupported-operation",
        "missing-release-input",
        "bad-release-root",
        "invalid-signed-envelope",
    ] {
        let (output, actual, expected) = run_case(name);
        assert_common(&output, &actual);
        assert_eq!(actual, expected, "fixture {name}");
    }
}

#[test]
fn malformed_request_keeps_stable_envelope_and_message_prefix() {
    let (output, actual, expected) = run_case("malformed-request");
    assert_common(&output, &actual);
    let message = actual["errors"][0]["message"]
        .as_str()
        .expect("request failure message");
    let prefix = expected["messagePrefix"]
        .as_str()
        .expect("expected message prefix");
    assert!(message.starts_with(prefix), "{message:?}");
}
