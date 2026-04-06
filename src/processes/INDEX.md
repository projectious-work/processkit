# processes/

Process definitions — declarative descriptions of workflows (code-review, release,
incident-response, ...). Processes declare WHAT happens and in what order; skills
provide HOW to do each step; context artifacts store the results.

**Phase 1 (v0.1.0):** this directory is empty. Process definitions migrate in Phase 2.

Each process is a Markdown file with YAML frontmatter describing:
- steps (ordered list referencing skills)
- roles (which actors participate)
- gates (validation points)
- definition of done

Processes are thin on purpose — the actual execution is delegated to skills.
