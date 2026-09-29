# Rapid iteration: a Todo application

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

This combined example shows how Spaceport's systems work together: [Cargo](cargo-overview.md) simplifies state, [Server Actions](transmissions-overview.md) 
handle events like `on-click` and `on-blur`, and [Class Enhancements](class-enhancements-overview.md) provide utilities like 
`.clean()`, `.quote()`, `.if()`, and `.combine()` for cleaner templates. The [Alert system](alerts-overview.md) wires routes to 
handlers, while [Launchpad](launchpad-overview.md)'s reactive block `${{ }}` syntax makes your UI reactive to server changes. Beyond what's shown 
here, Spaceport also provides [Documents](documents-overview.md) for database persistence, [Server Elements](server-elements-overview.md) for 
reusable components, [Docking Sessions & Client Management](sessions-overview.md) for authentication, and more. 
Ready to dive in? Start with [Getting Started](developer-onboarding.md) or jump straight to building your first app with 
the [Tic-Tac-Toe Tutorial](tutorial-tic-tac-toe.md).

[Try the live Todo demo](https://frontier.spaceport.sh/todo/).
