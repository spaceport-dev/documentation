# Ignition Scripts Overview

Ignition scripts are implemented startup hooks for one-time initialization in each process. `IgnitionStore.scan()` runs after stowaway JARs load and before source modules compile in `--start`. Migrations also run ignition after stowaways, without the normal source-module scan.

## Write an Ignition Script

Create `ignition/01-setup.groovy`:

```groovy
import spaceport.computer.alerts.Alert
import spaceport.computer.alerts.results.Result

class Setup {
    @Alert('on ignition')
    static void run(Result result) {
        // Perform idempotent startup initialization here.
    }
}
```

Hooks must be public static methods accepting a `Result`. Non-static hooks are logged and skipped. Script compilation or hook failures abort initialization; restart can run them again, so make persistent changes idempotent.

## Paths and Ordering

```yaml
ignition:
  paths:
    - ignition
    - setup
```

The default is `['ignition']`. Relative paths resolve from `spaceport root`; absolute paths are supported, and a trailing `/*` is stripped. Scanning is non-recursive. Missing directories are skipped. All `.groovy` files across configured directories are sorted by filename, compiled, then their annotated hooks are invoked in file order. Use filename prefixes when order matters; annotation priority does not control this direct invocation.

## Lifecycle and Available Code

Scripts share a dedicated classloader parented by the framework/stowaway classloader. They can use framework APIs and loaded stowaways, but must not rely on source modules having compiled. The scanner is one-shot and ignition does not hot reload. Hooks are invoked directly by the ignition scanner, rather than by normal route alert dispatch.

Use [Migrations](migrations-overview.md) for separately selected database procedures, and [Source Modules](source-modules-overview.md) for application routes and hot-reloaded code.
