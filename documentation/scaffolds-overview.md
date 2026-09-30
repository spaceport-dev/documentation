# Scaffolds Overview

A scaffold is the layout of modules, Launchpad templates, assets and configuration in a Spaceport project. The manifest determines where the runtime finds these files; you can use the layout that suits your application.

## Project Creation

Project creation is handled by [Create Spaceport App](https://github.com/spaceport-dev/create-spaceport-app), starter kits, or manual setup. Choose one of these approaches:

| Situation | Approach |
|---|---|
| AI-assisted project setup | Create Spaceport App: clone, fetch the pinned documentation, then follow `BOOTSTRAP.md` |
| Minimal starter | [Port Echo](https://github.com/spaceport-dev/port-echo) |
| Full application example | [Port Mercury](https://github.com/spaceport-dev/port-mercury) |
| Existing application layout | Create a manifest and directories manually |
| Small experiment | `--start --no-manifest` |

Create Spaceport App offers backend-only, public-site, full-app and custom scaffold levels. Its bootstrap workflow creates the project and manifest; the Spaceport JAR runs the result. Download the JAR separately and configure your CouchDB connection before starting.

## Zero-Config Prototyping with --no-manifest

Create `modules/App.groovy`, then run:

```bash
java -jar spaceport.jar --start --no-manifest
```

The defaults bind to `127.0.0.1:10000`, load `modules/*`, serve `assets/*` at `/assets/`, enable debug mode and connect to CouchDB at `http://127.0.0.1:5984`. If the database is unavailable, unattended startup fails unless you explicitly pass `--continue`.

An explicit manifest is required to customize host, source paths, credentials or application settings. See [Manifest Overview](manifest-overview.md).

## Typical Project Layout

```text
config.spaceport
modules/
launchpad/
  parts/
  elements/
assets/
stowaways/
ignition/
migrations/
```

Use only the folders your project needs. Ignition scripts run once during startup; migrations are selected separately with `--migrate`.

## See Also

- [Scaffolds API Reference](scaffolds-api.md) — Setup and Ground Control build steps
- [Scaffolds Internals](scaffolds-internals.md) — Source ownership and existing project configuration
- [Developer Onboarding](developer-onboarding.md) — Start a first application
- [CLI Overview](cli-overview.md) — Runtime commands
