# Scaffolds API Reference

## Create a Project

For AI-assisted setup, clone Create Spaceport App:

```bash
git clone https://github.com/spaceport-dev/create-spaceport-app my-project
cd my-project
```

Follow that repository's pinned documentation-fetch instructions, open Claude Code, and use its `BOOTSTRAP.md` workflow. The bootstrap creates a project based on your answers; download the framework JAR separately. For a ready-to-edit project, clone [Port Echo](https://github.com/spaceport-dev/port-echo) or [Port Mercury](https://github.com/spaceport-dev/port-mercury).

## Run the Project

Update `config.spaceport` with the correct source paths, host and database connection. From the project directory:

```bash
java -jar spaceport.jar --start config.spaceport
```

Use `--headless` for explicit unattended execution. Database connection failures exit unless `--continue` is supplied or a person confirms continuation in a terminal. See [CLI API](cli-api.md).

## Ground Control Builds

Ground Control is the dedicated Spaceport IntelliJ plugin. Version 1.1.0 targets IntelliJ Platform `2026.2.0.1`, since-build `262`, uses Gradle wrapper `9.3.1`, and requires a JDK 25 toolchain.

From its source checkout, with JDK 25 installed:

```bash
./gradlew -Dorg.gradle.java.installations.paths=/path/to/jdk-25 test buildPlugin
./gradlew -Dorg.gradle.java.installations.paths=/path/to/jdk-25 runIde
```

`buildPlugin` writes an installable ZIP under `build/distributions/`. `runIde` starts a sandbox IDE with the plugin loaded. Set the toolchain path to your own absolute JDK path. Install the ZIP with Settings → Plugins → Install Plugin from Disk.

These are plugin-source build requirements, not requirements for ordinary Spaceport applications. Shipyard integration and publication are managed by the orchestration workspace; availability of a source checkout does not imply a published plugin build.

## See Also

- [Scaffolds Overview](scaffolds-overview.md)
- [Scaffolds Internals](scaffolds-internals.md)
- [Developer Onboarding](developer-onboarding.md)
