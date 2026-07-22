---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260721_1905-SkilledMesa-include-feature-branch-workflow-in-the
  created: '2026-07-21T19:05:57+00:00'
spec:
  title: Include Feature Branch Workflow in the git-branching skill
  state: accepted
  decision: 'Include Feature Branch Workflow as a first-class strategy in the git-branching
    skill. Distinguish it from GitHub Flow: feature branches describe isolated work
    and integration into a shared branch, while GitHub Flow adds a mainline-centric
    deployment convention and pull-request collaboration.'
  context: The proposed git-branching skill initially listed GitHub Flow, Trunk-Based
    Development, Gitflow, GitLab Flow, and the processkit version-line model. The
    user asked whether feature branches were included.
  rationale: Feature branches are a common independently selectable workflow and a
    building block of several named models. Making them explicit helps users choose
    a lightweight shared-integration model without importing the full Gitflow or GitHub
    Flow conventions.
  alternatives:
  - option: Mention feature branches only within the other strategies
    rejected_because: Rejected because it hides a common standalone choice and blurs
      its distinction from GitHub Flow.
  consequences: The skill's comparison matrix will cover six strategies and will explain
    that short-lived task branches are often used within several of them.
  decided_at: '2026-07-21T19:05:57+00:00'
---
