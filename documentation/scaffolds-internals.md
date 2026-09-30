# Scaffolds Internals

## Runtime Scaffolding Was Removed

Spaceport commit `758c096` removed the `--create-port` dispatch branch, the `spaceport.bridge.Onboarding` class and bundled scaffold resources. Current JARs reject the old command. The previous wizard's eight-step process and resource-loading internals describe an older runtime, not a supported API.

## Current Ownership

[Create Spaceport App](https://github.com/spaceport-dev/create-spaceport-app) owns its bootstrap prompt, templates and scaffold choices. The runtime owns configuration loading, startup, ignition, module compilation and migration execution. Ground Control owns IntelliJ editor support and its plugin build.

Framework documentation has one authoritative source: [spaceport-dev/documentation](https://github.com/spaceport-dev/documentation). Starter kits and support tooling fetch ignored caches pinned to an explicit revision; contribute corrections to the authoritative repository.

## Updating an Existing Project

Existing projects produced by the old wizard do not need to be generated again. Keep their manifest, modules, templates and data; review their settings against the [Manifest API](manifest-api.md). Replace instructions that invoke `--create-port` with the current bootstrap or starter workflow.

## See Also

- [Scaffolds Overview](scaffolds-overview.md)
- [Scaffolds API Reference](scaffolds-api.md)
- [CLI Overview](cli-overview.md)
