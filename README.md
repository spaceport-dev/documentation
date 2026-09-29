# Spaceport documentation

The shared framework documentation for Spaceport. Read it on
[Frontier](https://frontier.spaceport.sh/docs/) or start with the
[introduction](documentation/_index.md) and [table of contents](documentation/_toc.md).

This repository is the source for the website, Port Echo, Port Mercury,
Create Spaceport App, and the Spaceport support plugin. Edit documentation here.
Consumer repositories keep fetch instructions and an optional untracked cache.

## Use in a project

Browse the Markdown on GitHub, or download a local reference without nested Git
repositories. Python 3.9 or newer is required for the fetch helper; it has no
third-party dependencies. Select a full commit SHA from this repository:

```sh
python3 fetch.py --revision FULL_COMMIT_SHA --destination /path/to/project/documentation
```

The helper downloads the archive for that revision, validates the documentation,
then replaces the cache. A failed download leaves existing docs intact. It retains
`README.md` and `.gitignore` placeholders, records the revision and checksums in
`.spaceport-docs.json`, and refuses to overwrite unmanaged or locally modified
files. Make contributions in a checkout of this repository, not in a cache.

## Contributing

- Keep relative `.md` links between pages so GitHub and Frontier both work.
- Use standard Markdown headings, fenced code, tables, and lists.
- Preserve public page names. Record historical page names in `aliases.json`.
- `legacy-anchors.json` preserves old website anchors when replacing old pages.
- Link live demos at Frontier, including `/tictactoe`, `/meeting-room`, and `/todo/`.
- Run `python3 -m unittest discover -s tests -v` for the fetch helper.

Frontier reads a local, explicitly deployed checkout of this repository and renders
Markdown with CommonMark Java and its table extension. It does not fetch GitHub
on page requests. Publishing a commit does not automatically deploy it; the
Spaceport orchestration workspace owns deployment, rendered-link verification,
and browser checks.

## Provenance

Imported from `spaceport-dev/port-echo` commit
`418ceee92d0c29ce0ef3307b06a31012bf6d9d90` on 2026-09-29. Its 70 documents match
Create Spaceport App, Port Mercury, and the support plugin after line-ending
normalization. The existing Frontier introduction contributes the Todo walkthrough
and entry points to live examples. `provenance.json` records original checksums.
Existing attribution is retained; this migration does not introduce a new license.
