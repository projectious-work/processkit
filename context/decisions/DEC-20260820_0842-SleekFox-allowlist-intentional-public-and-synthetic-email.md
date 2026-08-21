---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260820_0842-SleekFox-allowlist-intentional-public-and-synthetic-email
  created: '2026-08-20T08:42:06+00:00'
spec:
  title: Allowlist intentional public and synthetic email addresses
  state: accepted
  decision: Allowlist info@projectious.work and deploy@example.local in the pk-doctor
    sensitive-data email allowlist.
  context: The sensitive-data check reported six occurrences across CODE_OF_CONDUCT.md,
    SECURITY.md, and mirrored pk-doctor skill documentation.
  rationale: The user confirmed that info@projectious.work is intentionally public
    and deploy@example.local is synthetic example data.
  consequences: pk-doctor will suppress email-address findings for these two exact
    addresses only; secrets and other personal-data findings remain unaffected.
  decided_at: '2026-08-20T08:42:06+00:00'
---
