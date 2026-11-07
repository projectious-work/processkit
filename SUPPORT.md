# Support

processkit is an open-source project maintained through GitHub.

## Before opening an issue

1. Confirm whether the project uses the supported v0 line or an exact v1
   prerelease.
2. Read the [documentation](https://projectious-work.github.io/processkit/).
3. Run the appropriate health check and retain its output:

   ```sh
   uv run context/skills/processkit/pk-doctor/scripts/doctor.py --no-log
   ```

4. Search existing
   [issues](https://github.com/projectious-work/processkit/issues).

## What to include

- exact processkit version or commit;
- operating system and architecture;
- Python, `uv`, and Rust CLI versions where relevant;
- the command or MCP operation that failed;
- redacted diagnostic output; and
- a minimal reproduction when possible.

Use [SECURITY.md](SECURITY.md), not a public issue, for vulnerabilities or
sensitive reports.
