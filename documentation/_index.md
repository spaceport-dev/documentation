# Spaceport Documentation

**Spaceport** is a full-stack web application framework built on Groovy, Jetty, and CouchDB. It is designed for rapid development of interactive, real-time web applications with a minimal technology footprint — one language, one codebase, no build step.

## Start here

- [Set up your development environment](developer-onboarding.md).
- [Build Tic-Tac-Toe](tutorial-tic-tac-toe.md) or a [Meeting Room Booker](tutorial-meeting-room.md).
- [See routing, Cargo, and templates work together](guide-todo.md) in the Todo walkthrough.
- [Browse every topic and API reference](_toc.md).

### Try the live examples

[Play Tic-Tac-Toe](https://frontier.spaceport.sh/tictactoe) ·
[Book a meeting room](https://frontier.spaceport.sh/meeting-room) ·
[Try the Todo list](https://frontier.spaceport.sh/todo/)

### Choose a starter

[Port Echo](https://github.com/spaceport-dev/port-echo) provides a minimal scaffold.
[Port Mercury](https://github.com/spaceport-dev/port-mercury) provides a starting point for single-tenant applications.
[Create Spaceport App](https://github.com/spaceport-dev/create-spaceport-app) guides you through setup with an AI coding assistant.

<span id="rapid-iteration"></span>

## A Taste of Spaceport

See a complete Todo list in two files, then run the example below.

Build dynamic web applications using [Source Modules](source-modules-overview.md) to organize your backend logic and
[Routing](routing-overview.md) to handle HTTP requests. Spaceport's [Alert-driven Event System](alerts-overview.md) connects these pieces
together, letting you define endpoints, business logic, and data flows in one cohesive codebase. Changes to your
Groovy modules take effect immediately—no rebuilds required—so you can iterate as fast as you can type.

```groovy
/// modules/Todo.groovy

import spaceport.computer.alerts.Alert
import spaceport.computer.alerts.results.*
import spaceport.computer.memory.virtual.*
import spaceport.launchpad.Launchpad

class Todo {

    // Use Alerts to hook into routing events, even with dynamic parameters
    @Alert('~on /todo/(.*) hit')
    static _index(HttpResult r) {
        // Middleware encouraged
        r.context.data.'todo-list' = Cargo.fromStore('todo-lists').get(r.matches[0])
        // Render UI with Launchpad's HTML-first templates
        new Launchpad().assemble(['ui.ghtml']).launch(r)
    }

    // Endpoints don't have to serve fancy templates
    @Alert('on /api/todo/get-all hit')
    static _getAll(HttpResult r) {
        // Provide a quick JSON API endpoint
        r.writeToClient(Cargo.fromStore('todo-lists').toPrettyJSON())
    }
}
```

Build interactive UIs with [Launchpad](launchpad-overview.md)'s HTML-first templates that embed Groovy directly in your markup.
[Cargo](cargo-overview.md) provides a universal data container for common frontend/backend patterns, while Launchpad's
`.ghtml` templates offer reactive data binding—when server state changes, your UI updates automatically.
[Server Actions](transmissions-overview.md) connect DOM events to server-side logic, and [Class Enhancements](class-enhancements-overview.md)
like `.clean()`, `.quote()`, and `.if()` handle common template tasks like sanitizing input, escaping strings,
and conditional rendering. Build real-time interactivity without the boilerplate, while keeping full control to
add custom JavaScript when you need it.

```HTML
/// launchpad/parts/ui.ghtml

<%@ page import="spaceport.computer.memory.virtual.Cargo" %>
<script src="https://cdn.jsdelivr.net/gh/spaceport-dev/hud-core.js@latest/hud-core.js" defer></script>

<body>
/// Use the context provided by the router
<% def list = data.'todo-list' as Cargo %>

/// Reactively render the list
${{ list.combine { def item -> """
<div class="item ${ 'done'.if { item.done }}">

    /// Server actions provide seamless interactivity
    <span on-click=${ _{ item.toggle('done') }}>
    ${ item.done ? '✓' : '○' }
    </span>

    /// Conditional attributes, client transmissions, and input cleaning
    /// provide a safe and dynamic user experience
    <input ${ 'disabled'.if { item.done }}
    on-blur=${ _{ t -> item.text = t.value.clean() }}
    value=${ item.getString('text').quote() }>
</div>
""" }
}}

<button on-click="${ _{ list.setNext() }}">Add New</button>
</body>
```

**[Run this Todo list →](https://frontier.spaceport.sh/todo/)**

This combined example shows how Spaceport's systems work together: [Cargo](cargo-overview.md) simplifies state, [Server Actions](transmissions-overview.md)
handle events like `on-click` and `on-blur`, and [Class Enhancements](class-enhancements-overview.md) provide utilities like
`.clean()`, `.quote()`, `.if()`, and `.combine()` for cleaner templates. The [Alert system](alerts-overview.md) wires routes to
handlers, while [Launchpad](launchpad-overview.md)'s reactive block `${{ }}` syntax makes your UI reactive to server changes. Beyond what's shown
here, Spaceport also provides [Documents](documents-overview.md) for database persistence, [Server Elements](server-elements-overview.md) for
reusable components, [Docking Sessions & Client Management](sessions-overview.md) for authentication, and more.
Ready to dive in? Start with [Getting Started](developer-onboarding.md) or jump straight to building your first app with
the [Tic-Tac-Toe Tutorial](tutorial-tic-tac-toe.md).


## Philosophy

Spaceport is built around three core ideas:

**Convention over configuration.** Place a Groovy file in a source module directory and Spaceport discovers it automatically. Name a template file, reference it from a route handler, and it renders. There is no annotation processor to run, no dependency injection container to configure, and no build pipeline to maintain. In debug mode, changes take effect immediately — save the file and reload the page.

**Everything is an Alert.** Most frameworks use separate mechanisms for HTTP routing, WebSocket messaging, lifecycle hooks, and custom events. Spaceport unifies all of these under a single publish-subscribe system called Alerts. An HTTP GET request, a document being saved to the database, and the application finishing startup are all events that you handle with the same `@Alert` annotation on a static method. One pattern covers every kind of event your application needs to respond to.

**Server-side reactivity.** Traditional server-rendered applications require a full page reload to reflect state changes. Client-heavy SPAs push all rendering to the browser. Spaceport offers a third path: templates run on the server with full access to your database and business logic, and when server-side data changes, the framework pushes targeted DOM updates to the client over WebSocket. You get the simplicity of server rendering with the responsiveness of a reactive frontend — without maintaining a separate API layer or client-side state management system.

## Key Features

| Feature | What It Does |
|---|---|
| **[Alerts](alerts-overview.md)** | Unified event system for HTTP routes, WebSocket messages, document lifecycle hooks, and custom events. One `@Alert` annotation handles them all. |
| **[Launchpad](launchpad-overview.md)** | Server-side templating engine with `.ghtml` templates. Supports reactive bindings (`${{ }}`) that auto-update the client DOM when server data changes, and server actions (`_{ }`) that bind DOM events to server-side Groovy closures. |
| **[Documents](documents-overview.md)** | ORM-style interface for CouchDB. Define document types as Groovy classes with typed fields, views, and lifecycle hooks. |
| **[Cargo](cargo-overview.md)** | Reactive data containers that bridge server state and client UI. Session-scoped, document-backed, or standalone. Changes to Cargo data trigger automatic UI updates through Launchpad bindings. |
| **[Server Elements](server-elements-overview.md)** | Reusable full-stack components defined as `.ghtml` files with their own templates, server actions, and encapsulated state. |
| **[HUD-Core](hud-core-overview.md)** | Lightweight client-side JavaScript library (~23KB) that manages WebSocket connections, event binding for server actions, and DOM patching for reactive updates. |
| **[Source Modules](source-modules-overview.md)** | Hot-reloadable Groovy classes that contain your application logic. Drop a `.groovy` file into a module directory and Spaceport compiles and loads it automatically. |
| **[Transmissions](transmissions-overview.md)** | The client-to-server data pipeline for server actions — carries form fields, element values, and event data from the browser to your Groovy closures. |

## Technology Stack

Spaceport builds on a foundation of mature, open-source components:

- **Groovy** — Dynamic JVM language with seamless Java interop. Provides the expressiveness needed for concise templates and route handlers while giving you access to the entire Java ecosystem.
- **Jetty** — High-performance, production-grade web server and WebSocket engine. Handles HTTP and WebSocket communication.
- **CouchDB** — Document-oriented NoSQL database with built-in replication, a RESTful API, and a schema-flexible JSON document model. Spaceport's Documents system provides an ORM-like layer on top of CouchDB.

On the frontend, Spaceport works with standard HTML, CSS, and vanilla JavaScript. The HUD-Core library is the only client-side dependency, and it is optional if you do not use reactive bindings or server actions.

## Prerequisites

- **Java 8 SE or higher** — Amazon Corretto 11 (LTS) or Azul Zulu 11 (LTS) recommended. See [Compatibility Notes](compatibility-notes.md) for version-specific configuration.
- **CouchDB 2.0 or higher** — Version 3.5.x or later recommended.

## Quick Start

Download Spaceport and start the server:

```bash
curl -L https://frontier.spaceport.sh/builds/spaceport-latest.jar -o spaceport.jar
java -jar spaceport.jar --start config.spaceport
```

Or use `--no-manifest` to start with default configuration:

```bash
java -jar spaceport.jar --no-manifest
```

## How This Documentation Is Organized

Each major topic in this documentation is covered at up to four levels of depth:

1. **Overview** — What the feature is, why it exists, and when to use it. Written in prose with minimal code examples. Start here when learning a new topic.
2. **API Reference** — Complete method signatures, parameter descriptions, return types, and configuration options. Consult this while actively building.
3. **Internals** — How the feature works under the hood. Class relationships, data flow, threading model, and lifecycle details. For contributors and advanced users.
4. **Examples** — Real-world code patterns drawn from production Spaceport applications. Recipes, common patterns, and gotchas.

Not every topic has all four tiers. Smaller topics may only have an overview and API reference.

## Where to Start

If you are **new to Spaceport**, follow this path:

1. **[Developer Onboarding](developer-onboarding.md)** — Set up Java, CouchDB, and your development environment.
2. **[Groovy Luminary Certification](groovy-luminary.md)** — Learn Groovy basics and how they apply to Spaceport (especially if you are coming from Java or JavaScript).
3. **[Tutorial: Tic-Tac-Toe](tutorial-tic-tac-toe.md)** or **[Tutorial: Meeting Room Booker](tutorial-meeting-room.md)** — Build a complete application from scratch in two files.
4. **[Alerts Overview](alerts-overview.md)** and **[Launchpad Overview](launchpad-overview.md)** — Understand the two systems that every Spaceport application uses.

If you are **already building** and need a reference, go to the **[Table of Contents](_toc.md)** and find the API reference for the feature you are working with.

If you want to **understand how Spaceport works internally**, read the internals documents for each major subsystem, starting with [Alerts Internals](alerts-internals.md) and [Source Modules Internals](source-modules-internals.md).
