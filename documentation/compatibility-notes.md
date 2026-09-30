# Compatibility Notes

## Overview

Spaceport runs on the Java Virtual Machine (JVM) and targets broad compatibility across actively supported Java LTS releases. This document covers Java version requirements, JVM configuration flags, CouchDB compatibility, and general guidance for running Spaceport in development and production environments.


## Java Version Compatibility

### Verified Versions

| Use case | Verified baseline | Evidence |
|---|---|---|
| Framework compilation and tests | Java 8 | Shipyard's Gradle 5.2.1 build and 525 tests |
| Framework runtime | Java 21 | Shipyard HTTP smoke check and Frontier deployment |
| Ground Control plugin compilation | JDK 25 | Plugin toolchain and IntelliJ Platform 2026.2 build configuration; separate from the framework |

The framework targets Java 8 bytecode and embeds Groovy 3.0.25 at revision `3fff144`. A tested runtime baseline does not guarantee every third-party stowaway or application works on it. Verify your application's templates, database operations and reflective dependencies on the JDK you deploy.

## Running on Java 17+

### The `--add-opens` Flag

The Java Platform Module System (JPMS) restricts reflective access to internal APIs. On Java 17+, application dependencies that access these APIs may require explicit package access.

Spaceport's core does not directly require access to encapsulated JDK internals. However, Groovy's dynamic nature and many common Java libraries rely on deep reflection. When your application code or a dependency attempts to access an encapsulated API, you will see a runtime error:

```
java.lang.reflect.InaccessibleObjectException
```

To resolve this, add the `--add-opens` flag when starting Spaceport:

```bash
java --add-opens=java.base/java.lang=ALL-UNNAMED -jar spaceport.jar --start config.spaceport
```

This flag tells the JVM to open the `java.base/java.lang` package for reflective access by all unnamed modules. Add this flag when the reported inaccessible package is `java.lang`; other failures may need a different package. The Java 21 Shipyard smoke check does not require this flag.

Additional `--add-opens` flags may be required depending on which libraries your application uses. If you encounter further `InaccessibleObjectException` errors, the error message will indicate which package needs to be opened.

### Using Non-LTS Feature Releases

Non-LTS feature releases need application-specific verification; they are outside the recorded Shipyard runtime checks. Before deploying on a non-LTS release, perform a quick smoke test:

1. Start the application and check for module system or reflective access warnings in the output.
2. Load a Launchpad template route.
3. Trigger a source module endpoint.
4. Store and retrieve a Document to verify CouchDB connectivity.

If problems appear, fall back to the most recent LTS version.


## CouchDB Compatibility

Spaceport uses Apache CouchDB as its primary data store. Verify that your CouchDB version is compatible with the Spaceport release you are running. Consult the release notes for your specific Spaceport version for tested CouchDB versions.

General guidance:

- CouchDB 2.x and 3.x are the primary targets.
- Ensure CouchDB is accessible from the Spaceport host and that authentication credentials are configured correctly in your manifest file.
- After upgrading CouchDB, verify connectivity by starting Spaceport and confirming it connects without authentication failures.


## JVM Tuning

For most small to medium deployments, the default JVM settings are sufficient. If you notice frequent garbage collection pauses under load or if your source modules maintain large in-memory caches, consider explicit memory sizing:

```bash
java -Xms512m -Xmx1024m -jar spaceport.jar --start config.spaceport
```

Add metrics and monitoring to your application before tuning the JVM. Tune based on observed behavior, not assumptions.


## Verifying Your Runtime Environment

Before deploying to production, confirm your environment:

1. Run `java -version` to verify the vendor and version number.
2. (Optional) Run `echo $JAVA_HOME` to confirm it points to the correct JDK installation.
3. Start Spaceport and confirm in the output that it connects to CouchDB successfully.


## Summary

For maximum production stability, choose **Java 11 or 17**. Test newer feature releases locally, but anchor deployments on an LTS version. When running on Java 17 or later, use the `--add-opens` flag to maintain compatibility with Groovy's reflective features. Keep CouchDB versions aligned with your Spaceport release, and verify the complete startup sequence after any infrastructure changes.


## Related Documentation

- [Spaceport CLI](cli-overview.md) — Managing the application lifecycle
- [Source Modules](source-modules-overview.md) — Building application logic
- [Documents](documents-overview.md) — Database interactions with CouchDB
- [Stowaway JARs](stowaways-overview.md) — Loading external library dependencies


## Verified Build and IDE Tooling Baselines

The framework build at revision `3fff144` uses Java 8 and Gradle 5.2.1, with Groovy 3.0.25. Shipyard verification passed 525 tests and a Java 21 HTTP smoke check; Frontier runs Java 21. These checks do not prove every application dependency or all reflective code paths work on every JDK. The classloader also handles duplicate-class `LinkageError` messages emitted by that runtime.

Ground Control 1.1.0 is a separate IntelliJ plugin targeting platform 2026.2 / build 262. Building it requires JDK 25 and its Gradle 9.3.1 wrapper. This does not raise the framework runtime's Java requirement.
