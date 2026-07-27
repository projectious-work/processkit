# 

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

# aibox v1 installer integration

aibox should treat processkit as an opaque local executable. It creates a
versioned JSON request, invokes `processkit execute --request <path>`, parses
the single JSON result, and does not duplicate processkit ownership policy.

The producer integration checkpoint is the schema bundle under
`src/.processkit/installer/schemas/`, the executable built from `installer/`,
and these local gates:

```sh
scripts/test-installer-local.sh
scripts/test-installer-pilot-local.sh
```

The stable request fields are `apiVersion`, `operation`, `root`,
`distributionPath`, `envelopePath`, `signaturePath`, `trustStorePath`,
`profiles`, `harnesses`, and `yes`. Plan, install, and update accept either a
development `distributionPath` or the three signed-release paths. Production
consumers use the signed-release form. Mutation operations require
`yes: true`.

The stable result core is `apiVersion`, `status`, `changes`, `conflicts`,
`warnings`, and `errors`. Install additionally returns the committed state.
Callers must use `status` and the process exit code, not human output.

Cancellation is process cancellation. A subsequent `recover` request is the
only supported interruption repair path. Retries are safe after recovery; the
target lock prevents concurrent mutations. Installation state and transaction
evidence contain no private release key.

For the first integration increment, aibox should:

1. build or obtain the standalone executable;
2. validate the shipped schema bundle;
3. replace its provisional fixture call with `execute`;
4. run plan, install, cancellation/recovery, update, and uninstall in a
   disposable project;
5. preserve its v0 policy until parity and rollback evidence passes.

The readiness signal for removing the provisional adapter is a tagged
processkit prerelease containing this protocol and a passing
`scripts/test-installer-local.sh` result on both repositories.

For M5, pin the immutable `v1.0.0-alpha.3` release, not a branch or moving
reference. The aibox consumer test must download the archive, release
envelope, signature, public key, and matching native installer from that
GitHub release, verify the signed envelope, then exercise the opaque request
contract. Keep the v0 compatibility bridge enabled; this prerelease is an
explicit project opt-in and does not change the default processkit line.
