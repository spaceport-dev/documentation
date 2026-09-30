# Scaffolds Internals

## Scaffold Ownership

[Create Spaceport App](https://github.com/spaceport-dev/create-spaceport-app) owns its bootstrap prompt, templates and scaffold choices. The runtime owns configuration loading, startup, ignition, module compilation and migration execution. Ground Control owns IntelliJ editor support and its plugin build.

Framework documentation has one authoritative source: [spaceport-dev/documentation](https://github.com/spaceport-dev/documentation). Starter kits and support tooling fetch ignored caches pinned to an explicit revision; contribute corrections to the authoritative repository.

## Updating an Existing Project

Existing projects do not need to be generated again to use a different setup workflow. Keep their manifest, modules, templates and data; review their settings against the [Manifest API](manifest-api.md). Use the bootstrap or starter workflow for new projects.

## See Also

- [Scaffolds Overview](scaffolds-overview.md)
- [Scaffolds API Reference](scaffolds-api.md)
- [CLI Overview](cli-overview.md)
