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
