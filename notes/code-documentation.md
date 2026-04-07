# The Didactical Approach

The key insight is that codebases are not best explained linearly (file by file) but conceptually, in layers. Here's a proven structure:
Start with the "why" before the "what." Before any code appears, explain the problem the system solves, the key constraints it operates under, and the major design decisions (and their trade-offs). This gives readers a mental scaffold to hang details on.
Use a top-down, progressive-disclosure structure:

System overview — a single architecture diagram showing the major components and how data/control flows between them. This is the "map" readers will refer back to constantly.
Component deep-dives — each major subsystem gets its own section: what it does, its public API/interface, and how it relates to neighbors. No implementation details yet.
Key flows / walkthroughs — pick 3–5 representative scenarios (e.g., "what happens when a user submits a form") and trace them end-to-end through the system. This is where people actually build intuition — it bridges the static architecture with runtime behavior.
Implementation details — now you go file-by-file or module-by-module, but only after the reader has context. Annotated code snippets here, not full dumps.
Decision log / ADRs — why things are the way they are, what alternatives were considered. This is the most underrated section and the one that saves the most time for new contributors.

Other pedagogical principles that matter: use diagrams heavily (one good sequence diagram beats a page of prose), provide a glossary of domain terms early, and always show concrete examples alongside abstractions.

# Tooling Recommendations

Docusaurus (or similar: Nextra, Starlight, VitePress) — this is probably your best bet overall. Markdown-based (trivial for AI agents to generate), built-in code highlighting with Prism, supports MDX so you can embed React components for side-by-side views or interactive diagrams, and Mermaid integration for diagrams-as-code. Docusaurus specifically has versioning, search, and sidebar navigation out of the box. The output is a static site you can host anywhere. The Markdown source is also perfectly readable in a plain editor or on GitHub, which matters for maintainability.

For the AI-agent workflow specifically: have the agent output one .md file per section following the layered structure above, with Mermaid code blocks for diagrams and standard fenced code blocks for snippets. A human reviewer can then read the raw Markdown (it's perfectly legible), or build the site for the polished version. This keeps the authoring format identical to the delivery format, which avoids lossy conversions.

In Docusaurus, side-by-side code is typically done with MDX (which is just Markdown + React components). There are two common approaches:

**True side-by-side with a custom MDX component**

Create a reusable component, then use it in any `.mdx` file:

```jsx
// src/components/CodeSideBySide.jsx
import React from 'react';
import CodeBlock from '@theme/CodeBlock';

export default function CodeSideBySide({ left, right }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
      <div>
        {left.title && <h4>{left.title}</h4>}
        <CodeBlock language={left.language}>{left.code}</CodeBlock>
      </div>
      <div>
        {right.title && <h4>{right.title}</h4>}
        <CodeBlock language={right.language}>{right.code}</CodeBlock>
      </div>
    </div>
  );
}
```

Then in your docs:

```mdx
import CodeSideBySide from '@site/src/components/CodeSideBySide';

## Repository Pattern

<CodeSideBySide
  left={{
    title: "Interface",
    language: "typescript",
    code: `interface UserRepo {
  find(id: string): Promise<User>;
  save(user: User): Promise<void>;
}`
  }}
  right={{
    title: "Postgres Implementation",
    language: "typescript",
    code: `class PgUserRepo implements UserRepo {
  async find(id: string) {
    const row = await sql\`SELECT * FROM users WHERE id = \${id}\`;
    return toUser(row);
  }
}`
  }}
/>
```

