---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260727_0617-NeatJay-migrate-processkit-documentation-to-hugo-docsy
  created: '2026-07-27T06:17:57+00:00'
spec:
  title: Migrate processkit documentation to Hugo + Docsy with versioned v0.x/v1.x
    lines
  state: accepted
  decision: 'Replace the Docusaurus `docs-site/` with a Hugo + Docsy documentation
    site laid out at the repository root (hugo.yaml, content/, assets/, layouts/,
    static/, themes/docsy submodule), mirroring the projectious-work/kubeclaw reference
    implementation. Publish two documentation lines to GitHub Pages from a single
    gh-pages branch: the v0.x line at the site root (built from the v0.x-dev branch)
    and the v1.x line under /v1.x/ as an alpha preview (built from the v1.x-dev branch),
    switchable via the Docsy version menu. Style the site from the projectious-work/brand
    design system. Introduce a new processkit logo derived from the projectious brand
    mark (midnight process ring, white arrowhead, orange checkpoint dot) and use it
    for the site navbar, favicons, and README.'
  context: 'The project''s documentation was a Docusaurus 3 site under `docs-site/`,
    published manually to the gh-pages branch, using stock Docusaurus green/teal theming
    with no brand alignment and no project logo (docusaurus.config.js referenced an
    `img/favicon.ico` that was never shipped). The sibling project projectious-work/kubeclaw
    had already solved the same problem with Hugo + Docsy styled from the shared projectious-work/brand
    design system, including a brand-derived mark, fingerprinted favicons, and a DOCS_VERSION-aware
    deploy script that publishes versioned builds into subdirectories of one gh-pages
    branch. processkit maintains two active documentation lines simultaneously: the
    released and dogfooded v0.28.x line on v0.x-dev, and the v1.0 alpha line on v1.x-dev.
    Decided by the project owner (Bernhard) in session on 2026-07-26.'
  rationale: Hugo + Docsy matches the established projectious-work house pattern,
    so brand SCSS, favicon handling, font loading, and the deploy script transfer
    across projects rather than being reimplemented per site. Docsy's built-in version
    menu and the kubeclaw deploy script's DOCS_VERSION support give versioned documentation
    lines without a second Pages site or a second repository. Placing v0.x at the
    root reflects that it is the currently released and supported line — visitors
    who arrive without a version in mind should land on documentation that describes
    shipping behaviour, not an alpha. The v1.x line remains reachable and clearly
    labelled as a preview. Deriving the logo from the projectious mark's construction
    (midnight silhouette, white inner form, orange accent dot) keeps processkit visually
    in the same family as kubeclaw without reusing either mark.
  alternatives:
  - option: Keep Docusaurus and only restyle it to the brand
    why_not: Would not match the kubeclaw reference the owner asked the site to be
      measured against, and leaves two different documentation stacks to maintain
      across projectious-work projects.
  - option: v1.x at the site root, v0.x archived under /v0.x/
    why_not: 'Considered and rejected by the owner: the v1.x line is a pre-alpha rebuild,
      so making it the default landing documentation would misrepresent what is actually
      shipping.'
  - option: One Hugo site carrying both lines as content sections, no versioned builds
    why_not: v0.x and v1.x have divergent primitives and reference material; interleaving
      them in one tree forces every reference page to caveat which line it describes.
  consequences: The `docs-site/` Docusaurus tree is removed and its Markdown content
    is converted to Hugo/Docsy front matter and link syntax. The repository gains
    root-level `content/`, `assets/`, `layouts/`, `static/`, and `themes/` directories
    plus a `themes/docsy` git submodule and a Node dev-dependency set for Bootstrap
    and Font Awesome; local docs work now requires Hugo extended and npm rather than
    npm alone. The same migration has to be applied to both v0.x-dev and v1.x-dev,
    and the two branches' deploy invocations differ only by DOCS_VERSION. Publishing
    stays manual (no GitHub Actions), consistent with the repository's existing no-CI
    policy.
  decided_at: '2026-07-27T06:17:57+00:00'
---
