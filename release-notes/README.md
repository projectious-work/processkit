# Release notes

Every tag published through `scripts/maintain.sh` requires a curated tracked
file named:

```text
release-notes/vX.Y.Z.md
```

The file is the authoritative GitHub Release body. It must state:

- supported or prerelease classification;
- user-visible changes;
- compatibility and migration constraints;
- platform and runtime support;
- verification evidence; and
- known limitations.

Release notes are reviewed before tagging. Generated notes are not accepted as
a substitute for this file.
