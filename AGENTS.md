# Shared framework documentation

This repository owns Spaceport framework documentation. Read README.md first.
Edit documentation/*.md here; other projects and Frontier consume this source.
Preserve useful tutorials, code examples, relative Markdown links, page names,
and historical aliases. Never treat example GHTML as executable site templates.

Keep examples consistent with the documented runtime version. Verify APIs against
framework sources or authoritative documentation; do not invent methods. Changes
here do not deploy Frontier automatically. Coordinate website changes through the
Spaceport orchestration workspace and record the exact deployed revision.

Run fetch-helper tests after changing fetch.py. For content changes, use Frontier's
actual renderer and link checker, then browser checks for rendering changes.
Do not commit caches, generated output, secrets, or runtime JARs.

## Documentation voice and scope

- Describe supported behavior in the present tense. Explain what an API does,
  when to use it, its inputs, outputs, defaults, errors, and practical limits.
- Keep release-history narration out of reference pages and setup guides. Avoid
  “now,” “no longer,” “previously,” “used to,” and “was removed” when comparing
  framework versions. Write “output goes to stdout,” not “a missing console no
  longer breaks output.” Ordinary sequences, state changes, and tutorial steps
  may use temporal language when it helps explain the current behavior.
- Put change history in release notes or audit records. Retain a concise,
  explicitly labeled migration or compatibility note only when it gives readers
  an actionable upgrade step or a version-specific requirement. Lead with the
  supported workflow; do not retell obsolete implementations.
- Use em dashes (—) for prose punctuation rather than double or triple hyphens.
  Preserve CLI flags, code, URLs, table delimiters and Markdown thematic breaks.
- Use plain, direct language and concrete examples. Avoid marketing claims,
  filler, vague claims of novelty, and references to the editing session.
- Keep overview, reference, internals, and tutorial pages consistent. When a
  workflow changes, review surrounding introductions, tables of contents,
  cross-links, and duplicated explanations for stale instructions.
- State version and revision boundaries where they affect accuracy. Distinguish
  framework runtime requirements from build tooling and IDE requirements.
  Verification evidence belongs in audit records unless it establishes a useful
  compatibility boundary for readers.
- Preserve page names, useful examples, and public anchors when editing headings;
  add retired heading IDs to `legacy-anchors.json` as needed.
- Keep agent instructions at this repository root. The `documentation/` folder
  contains published pages; its Markdown files are rendered as public docs.
