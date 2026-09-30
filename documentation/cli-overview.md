# CLI Overview

The Spaceport Command-Line Interface (CLI) is the primary way to start, configure, and maintain a Spaceport application. All commands are invoked through the Spaceport JAR file.


## Basic Usage

```bash
java -jar spaceport.jar <command> [arguments]
```

If you have a wrapper script on your `PATH`, you can use:

```bash
spaceport <command> [arguments]
```


## Commands

### --start

Start the Spaceport server using a manifest configuration file.

```bash
java -jar spaceport.jar --start /path/to/config.spaceport
```

This is the primary command for running your application. It performs the following sequence:

1. Reads and parses the YAML manifest file
2. Merges user configuration over built-in defaults (deep merge)
3. Substitutes and types environment values, then validates framework configuration
4. Applies metaclass enhancements to Groovy types
5. Initializes the CouchDB connection
6. Fails if the database is unreachable unless interactive confirmation or `--continue` permits continuing
7. Displays a debug mode warning if `debug: true`
8. Loads stowaway JARs into the classpath
9. Runs ignition scripts once, then scans and compiles source modules
10. Starts the Jetty HTTP server and WebSocket handler


### --start --no-manifest

Start the Spaceport server with default configuration, without a manifest file.

```bash
java -jar spaceport.jar --start --no-manifest
```

This mode uses built-in defaults:

| Setting | Default Value |
|---|---|
| Host address | `127.0.0.1` |
| Port | `10000` |
| Debug mode | `true` |
| Source modules | `modules/*` |
| Static assets | `assets/*` at `/assets/` |
| CouchDB address | `http://127.0.0.1:5984` |
| Logging | Disabled |
| Stowaways | Enabled, from `stowaways/*` |

This is useful for rapid prototyping or when you want to run a minimal application without any configuration overhead.


### Unattended Startup and Migration Options

```bash
java -jar spaceport.jar --start config.spaceport --headless
java -jar spaceport.jar --start config.spaceport --headless --continue
java -jar spaceport.jar --migrate config.spaceport --headless '{"migration":"001-seed.groovy","inputs":{"tenant":"acme"}}'
java -jar spaceport.jar --migrate config.spaceport --headless @migration.json
```

Place the manifest path before `--headless`: its next non-flag argument is consumed as the optional JSON value.

- `--headless` forces non-interactive operation even when a terminal is attached. Prompts fail rather than waiting for input.
- `--continue` explicitly permits startup or migration to proceed when the main database cannot authenticate. Without it, an attached terminal offers a continue/exit choice; unattended execution exits with status `1`.
- Without a terminal (systemd, cron, pipes), output goes to stdout and prompts fail automatically.
- Migration JSON accepts a `migration` filename and an `inputs` object. `@file` reads that JSON from disk. Migration scripts receive `report`, `inputs`, and `interactive` bindings; supplied inputs do not answer `Command` prompts automatically.
- A single migration is selected automatically without a terminal. With multiple migrations, supply its filename. Unknown filenames, malformed JSON, prompt attempts without a terminal, and migration failures exit with status `1`.


### --migrate

Run database migration scripts without fully booting the server.

```bash
java -jar spaceport.jar --migrate /path/to/config.spaceport
java -jar spaceport.jar --migrate --no-manifest
```

The migrate command:

1. Reads the manifest (or uses defaults with `--no-manifest`)
2. Merges configuration over defaults and substitutes environment variables
3. Connects to CouchDB
4. Scans the migrations directory for `.groovy` files
5. Presents an interactive menu to select a migration
6. Executes the selected migration script using a `GroovyScriptEngine`

The migrations directory defaults to `migrations/` relative to the Spaceport root, or can be configured via the `migrations.path` manifest key.


### --db

Open the Spaceport Database Console (not yet implemented).

```bash
java -jar spaceport.jar --db /path/to/config.spaceport
```

This command is reserved for a future interactive database management tool.


### --help

Display usage information and available commands.

```bash
java -jar spaceport.jar --help
```

Prints the Spaceport version, ASCII logo, and a summary of all available commands with their syntax.


### --color

Display all available terminal color combinations.

```bash
java -jar spaceport.jar --color
```

This diagnostic command renders every color and color combination available in the `Command` class color system. Useful for verifying terminal color support or choosing colors for custom output.


## Common Usage Patterns

### Local Development

```bash
# Start with your project config
java -jar spaceport.jar --start config.spaceport

# Or start with zero config for quick testing
java -jar spaceport.jar --start --no-manifest
```

### Running Migrations

```bash
# Run a migration using your project config
java -jar spaceport.jar --migrate config.spaceport
```

### Creating a New Project

Use [Create Spaceport App](https://github.com/spaceport-dev/create-spaceport-app) for AI-assisted setup, clone a starter kit, or create a project manually. See [Scaffolds Overview](scaffolds-overview.md).

```bash
git clone https://github.com/spaceport-dev/create-spaceport-app my-project
cd my-project
```

Follow the repository's documentation-fetch instructions, then its `BOOTSTRAP.md` workflow. Download the framework JAR separately.


### Environment-Specific Startup

```bash
# Development
java -jar spaceport.jar --start config.spaceport

# Staging
java -jar spaceport.jar --start config.staging.spaceport

# Production
java -jar spaceport.jar --start config.production.spaceport
```


## Exit Behavior

- `--help`, `--color`: Exit immediately after output
- `--migrate`: Exit after the interactive process completes (via `System.exit(0)`)
- `--start`: Runs indefinitely until the process is terminated (the Jetty server blocks on `server.join()`)
- `CTRL+C` during interactive commands: Terminal settings are restored before exiting (macOS/Linux only)


## See Also

- [CLI API Reference](cli-api.md) — Full Command class API and color system
- [Scaffolds Overview](scaffolds-overview.md) — Current project creation options
- [Manifest Overview](manifest-overview.md) — Configuration file format and options
