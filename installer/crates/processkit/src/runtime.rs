//! Native runtime diagnostics that delegate domain checks to Python.

use crate::filesystem::{ensure_non_symlink_directory, ensure_regular_file};
use serde::Serialize;
use serde_json::Value;
use std::path::Path;
use std::process::Command;

const RUNTIME_API_VERSION: &str = "processkit.projectious.work/runtime/v1alpha1";
const DOCTOR_RELATIVE: &str = "context/skills/processkit/pk-doctor/scripts/doctor.py";

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct RuntimeInfo {
    uv_version: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct DoctorResult {
    api_version: &'static str,
    kind: &'static str,
    status: &'static str,
    root: String,
    runtime: RuntimeInfo,
    doctor: Value,
    errors: Vec<Value>,
}

impl DoctorResult {
    pub(crate) fn has_errors(&self) -> bool {
        self.doctor["totals"]["error"].as_u64().unwrap_or(1) > 0
    }

    pub(crate) fn summary(&self) -> String {
        format!(
            "{}: {} error(s), {} warning(s), {} actionable finding(s)",
            self.status,
            self.doctor["totals"]["error"].as_u64().unwrap_or(0),
            self.doctor["totals"]["warn"].as_u64().unwrap_or(0),
            self.doctor["action_totals"]["actionable"]
                .as_u64()
                .unwrap_or(0)
        )
    }
}

pub(crate) fn run_doctor(root: &Path, category: Option<&str>) -> Result<DoctorResult, String> {
    run_doctor_with_uv(root, category, Path::new("uv"))
}

fn run_doctor_with_uv(
    root: &Path,
    category: Option<&str>,
    uv: &Path,
) -> Result<DoctorResult, String> {
    ensure_non_symlink_directory(root, "doctor root")?;
    let root = root
        .canonicalize()
        .map_err(|error| format!("doctor root: {error}"))?;
    let doctor = root.join(DOCTOR_RELATIVE);
    ensure_regular_file(&root, &doctor, "doctor script")?;

    let probe = Command::new(uv)
        .arg("--version")
        .output()
        .map_err(|error| format!("uv is unavailable: {error}"))?;
    if !probe.status.success() {
        return Err(format!(
            "uv version probe failed with {}",
            probe.status.code().unwrap_or(3)
        ));
    }
    let uv_version = String::from_utf8(probe.stdout)
        .map_err(|_| "uv version output was not UTF-8".to_owned())?
        .trim()
        .to_owned();
    if uv_version.is_empty() {
        return Err("uv version probe returned no output".to_owned());
    }

    let mut command = Command::new(uv);
    command
        .current_dir(&root)
        .arg("run")
        .arg("--script")
        .arg(&doctor)
        .arg("--json")
        .arg("--no-log")
        .arg("--repo-root")
        .arg(&root);
    if let Some(category) = category {
        if category.is_empty()
            || !category
                .bytes()
                .all(|byte| byte.is_ascii_alphanumeric() || b"_,-".contains(&byte))
        {
            return Err("doctor category contains unsupported characters".to_owned());
        }
        command.arg(format!("--category={category}"));
    }
    let output = command
        .output()
        .map_err(|error| format!("failed to launch Python doctor: {error}"))?;
    if output.stdout.is_empty() {
        return Err(format!(
            "Python doctor returned no JSON output: {}",
            redacted_stderr(&output.stderr)
        ));
    }
    let payload: Value = serde_json::from_slice(&output.stdout)
        .map_err(|error| format!("Python doctor returned invalid JSON: {error}"))?;
    let reported_exit = payload["exit_code"]
        .as_i64()
        .ok_or_else(|| "Python doctor JSON has no integer exit_code".to_owned())?;
    let process_exit = i64::from(output.status.code().unwrap_or(3));
    if reported_exit != process_exit || !matches!(reported_exit, 0 | 1) {
        return Err(format!(
            "Python doctor exit mismatch: process={process_exit}, payload={reported_exit}"
        ));
    }
    let errors = payload["totals"]["error"]
        .as_u64()
        .ok_or_else(|| "Python doctor JSON has no totals.error".to_owned())?;
    Ok(DoctorResult {
        api_version: RUNTIME_API_VERSION,
        kind: "DoctorResult",
        status: if errors == 0 { "healthy" } else { "findings" },
        root: root.to_string_lossy().into_owned(),
        runtime: RuntimeInfo { uv_version },
        doctor: payload,
        errors: Vec::new(),
    })
}

fn redacted_stderr(stderr: &[u8]) -> String {
    let rendered = String::from_utf8_lossy(stderr);
    let first_line = rendered.lines().next().unwrap_or("no stderr");
    first_line.chars().take(240).collect()
}

#[cfg(all(test, unix))]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Write;
    use std::os::unix::fs::PermissionsExt;
    use std::path::PathBuf;
    use tempfile::TempDir;

    fn fixture(exit_code: i32) -> (TempDir, PathBuf) {
        let root = TempDir::new().expect("temporary root");
        let doctor = root.path().join(DOCTOR_RELATIVE);
        fs::create_dir_all(doctor.parent().expect("doctor parent")).expect("create doctor parent");
        fs::write(&doctor, "# fixture\n").expect("write doctor fixture");
        let uv = root.path().join("fake-uv");
        let mut uv_file = fs::File::create(&uv).expect("create fake uv");
        uv_file
            .write_all(
                format!(
                    "#!/bin/sh\n\
                 if [ \"$1\" = \"--version\" ]; then echo 'uv 0.test'; exit 0; fi\n\
                 printf '%s\\n' '{{\"totals\":{{\"error\":{exit_code},\"warn\":0,\
                 \"info\":1}},\"action_totals\":{{\"actionable\":0}},\
                 \"exit_code\":{exit_code}}}'\n\
                 exit {exit_code}\n"
                )
                .as_bytes(),
            )
            .expect("write fake uv");
        uv_file.sync_all().expect("sync fake uv");
        drop(uv_file);
        let mut permissions = fs::metadata(&uv).expect("fake uv metadata").permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&uv, permissions).expect("make fake uv executable");
        (root, uv)
    }

    #[test]
    fn clean_doctor_result_is_wrapped() {
        let (root, uv) = fixture(0);
        let result = run_doctor_with_uv(root.path(), Some("drift"), &uv).expect("doctor result");
        assert_eq!(result.status, "healthy");
        assert!(!result.has_errors());
        assert_eq!(result.runtime.uv_version, "uv 0.test");
    }

    #[test]
    fn doctor_findings_preserve_nonzero_exit() {
        let (root, uv) = fixture(1);
        let result = run_doctor_with_uv(root.path(), None, &uv).expect("doctor findings");
        assert_eq!(result.status, "findings");
        assert!(result.has_errors());
    }

    #[test]
    fn unsafe_category_is_rejected() {
        let (root, uv) = fixture(0);
        let error = run_doctor_with_uv(root.path(), Some("drift;env"), &uv)
            .err()
            .expect("invalid category");
        assert!(error.contains("unsupported characters"));
    }
}
