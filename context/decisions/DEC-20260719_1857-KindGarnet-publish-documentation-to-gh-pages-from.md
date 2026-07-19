---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260719_1857-KindGarnet-publish-documentation-to-gh-pages-from
  created: '2026-07-19T18:57:55+00:00'
  updated: '2026-07-19T18:58:03+00:00'
spec:
  title: Publish documentation to gh-pages from local builds
  state: accepted
  decision: Publish the documentation site by building it locally and committing the
    generated static files to the gh-pages branch. Keep repository-authored GitHub
    Actions workflows and custom actions absent.
  context: The prior policy removed both GitHub Actions and GitHub Pages. The owner
    has now explicitly requested restoration of gh-pages documentation while retaining
    manual local build and publishing.
  rationale: A locally built, committed static branch provides hosted documentation
    without maintaining a repository workflow file.
  alternatives:
  - option: Keep documentation local only
    reason: Rejected by the owner's explicit request to redeploy gh-pages.
  - option: Add a GitHub Actions deployment workflow
    reason: Rejected because the owner does not want repository workflows or actions.
  consequences: Maintainers must build and publish the site manually. GitHub may retain
    or invoke its platform-managed Pages deployment mechanism even though the repository
    contains no workflow YAML.
  decided_at: '2026-07-19T18:57:55+00:00'
  supersedes: DEC-20260719_1430-HonestOak-use-manual-local-verification-instead-of
---
