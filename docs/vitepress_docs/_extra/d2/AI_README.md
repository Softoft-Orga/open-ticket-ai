# A Comprehensive Guide to the D2 Declarative Diagramming Language for Programmatic Generation

---

# Section 1: Foundational Concepts, Philosophy, and Syntax

This section establishes the theoretical groundwork of the D2 language. It defines the language's core purpose, its
guiding design principles, and the atomic units of its syntax. An understanding of these fundamentals is a prerequisite
for the generation of valid and idiomatic D2 code.

## 1.1. The D2 Philosophy: A Language for Software Engineers

The D2 language is a domain-specific language (DSL) engineered to transform textual descriptions into diagrams. Its
primary and explicit purpose is to serve software engineers in the documentation of software architecture and systems.
This focused application domain informs every aspect of the language's design, from its syntax to its feature set. It is
deliberately not a general-purpose visualization tool; features common in other tools, such as Gantt charts, mind maps,
or Venn diagrams, are explicitly excluded to prevent feature bloat and maintain a sharp focus on its core use case. This
singular focus results in a language that is highly optimized for its intended task, offering specialized constructs for
software concepts. The language is built upon a set of core design principles that dictate its structure and behavior.

### 1.1.1. Design Principle 1: Readability over Brevity

A paramount principle in D2's design is the prioritization of readability and maintainability over syntactic
compactness. The language's syntax is intentionally descriptive and less terse than some alternatives. For example,
defining a cylinder shape is done with the explicit key-value pair `shape: cylinder`, rather than a more cryptic
symbolic representation like `[(...)]`. This choice makes D2 code more self-documenting and easier for humans to
understand and modify over time. This principle extends to the language's structure, which favors consistent key-value
pairs and is supported by a built-in autoformatter (`d2 fmt`) that ensures a canonical style across all projects,
eliminating debates over indentation and spacing. This inherent predictability in the language's structure makes it
well-suited for programmatic generation, as the rules for producing well-formed code are clear and consistent.

### 1.1.2. Design Principle 2: Good Defaults

D2 is designed to produce aesthetically pleasing and functionally useful diagrams with zero or minimal customization.
This is achieved through the provision of high-quality default settings, most notably a set of built-in, professionally
designed color themes. Instead of requiring the user to build up a visual style from a monochrome base, D2 provides a
pleasant and effective visual presentation out of the box. This philosophy simplifies the user's task, allowing them to
focus on the content and structure of the diagram, confident that the resulting visual will be of high quality.

### 1.1.3. Design Principle 3: Warnings over Errors

The D2 compiler is designed to be permissive, prioritizing successful compilation whenever possible. If a script
contains a non-critical issue—such as a reference to a non-existent class or a style attribute that has no effect on a
particular shape—the compiler will issue a warning but will still produce a diagram. This approach contrasts with
stricter languages that would halt compilation with a "stop-the-world" error. The rationale is to provide a smoother and
less frustrating development and debugging workflow, as users are not blocked by minor or transient issues in their
code.

## 1.2. The Lexicon: Identifiers, Strings, and Literals

The lexicon of D2 comprises the basic building blocks of the language: the names used to identify objects, the text used
for labels, and the syntax for comments.

### 1.2.1. Object Keys (Identifiers)

Every object in a D2 diagram is identified by a unique key. This key is the identifier used when forming connections or
applying styles. The rules for keys are flexible:

* **Unquoted Keys**: An unquoted key can consist of alphanumeric characters and underscores (`_`). Notably, unquoted
  keys can also contain spaces; the D2 parser will treat a multi-word sequence as a single identifier (e.g.,
  `API Gateway` is a valid key). Single hyphens are also permitted (e.g., `a-shape`), but care must be taken as a double
  hyphen (`--`) is interpreted as a connection operator, which can lead to parsing ambiguity.
* **Quoted Keys**: To use special characters or avoid ambiguity, keys can be enclosed in double quotes (e.g.,
  `"key-with-special-chars@!"`).

### 1.2.2. Labels and Strings

Labels are the visible text rendered on shapes and connections. D2 supports several string types for defining them:

* **Unquoted Strings**: Suitable for simple, single-line labels that do not contain special characters. The parser
  automatically trims any leading or trailing whitespace from unquoted strings.
* **Quoted Strings**: Double quotes (`"`) must be used for labels that contain special characters or where preservation
  of internal whitespace is significant.
* **Markdown Blocks**: For rich, multi-line labels, D2 supports GitHub-flavored Markdown. A Markdown block is defined
  using a pipe (`|`) followed by `md`, with the content enclosed between the start and a closing pipe (e.g.,
  `label: |md\n# Title\n- Bullet point\n|`). This allows for the inclusion of headers, lists, and other formatting
  directly within a shape's label.
* **Block Strings**: The pipe (`|`) character is common in some programming languages like TypeScript. To accommodate
  this, D2 provides an extended block string syntax. By adding more pipes or other special, non-alphanumeric characters,
  a custom delimiter can be created (e.g., `||ts... ||` or `|@ts... @|`) to prevent the parser from misinterpreting
  language-native characters as the end of the block.

### 1.2.3. Comments

D2 uses Bash-style syntax for comments. The hash symbol (`#`) indicates that the rest of the line is a comment and
should be ignored by the parser. Comments can be placed on their own line or at the end of a line of code. There is no
dedicated syntax for multi-line comment blocks; each line must begin with a `#`.

```d2
# This is a full-line comment.
x -> y # This is an end-of-line comment.
````

## 1.3. The Grammar: Connections and Structural Punctuation

The grammar of D2 defines how the lexical elements are combined to form valid statements. It is based on a small set of
operators and delimiters.

### 1.3.1. Connection Operators

Connection operators are the verbs of the D2 language, defining the relationships between shapes. There are four types:

* `--`: An undirected connection, representing a non-directional relationship.
* `->`: A directed connection, flowing from the left-hand object to the right-hand object.
* `<-`: A directed connection, flowing from the right-hand object to the left-hand object.
* `<->`: A bi-directional connection, indicating a relationship in both directions.

### 1.3.2. Structural Delimiters

These punctuation marks provide the structure for D2 scripts:

* **Colon (`:`)**: The colon is a versatile delimiter used to separate a key from its value. This applies to assigning
  labels (`key: label`), specifying attributes (`shape: cloud`), and separating a connection from its label (
  `x -> y: connects to`).
* **Semicolon (`;`)**: The semicolon acts as a statement separator, allowing for multiple shape declarations to be
  written on a single line for conciseness (e.g., `shape1; shape2; shape3`).
* **Period (`.`)**: The period, or "dot" operator, is used for accessing nested objects and attributes. It allows for
  traversal of the object hierarchy (`container.child`) and for targeting specific style properties (
  `shape.style.fill`).
* **Braces (`{}`)**: Braces are used to define a scope or a block. They are used to group multiple attributes for a
  single object, to define the contents of a container shape, or to create blocks for styling.

-----

# Section 2: Core Primitives: Shapes and Connections

This section details the fundamental "nouns" (shapes) and "verbs" (connections) of a D2 diagram. Mastery of these
primitives is essential for creating any non-trivial diagram. The core concepts of declaration, labeling, and the
distinction between an object's identity and its presentation are central to the language's design.

## 2.1. Declaring and Labeling Shapes

A foundational concept in D2 is the strict separation between an object's key and its label. This separation is what
enables the creation of stable and maintainable diagrams.

* **Key**: The key is the unique, immutable identifier for a shape. It is used in all programmatic references, such as
  forming connections or applying styles. The key may or may not be visually rendered.
* **Label**: The label is the text that is visually displayed on the shape in the final diagram. It is for presentation
  purposes and can be changed without affecting the diagram's underlying structure.

If a label is not explicitly provided for a shape, its key is used as the default label.

**Declaration Syntax:**
A shape can be declared in two ways:

* **Explicit Declaration**: A shape is declared on its own line, often with attributes. This is the required method for
  assigning properties like a specific shape type or style before it is used in a connection.
  ```d2
  # Explicitly declare a shape with key 'pg' and label 'PostgreSQL'
  pg: PostgreSQL
  pg.shape: cylinder # Assign an attribute to the declared shape
  ```
* **Implicit Declaration**: A shape is declared automatically when it is first mentioned in a connection. If shapes `x`
  and `y` have not been previously defined, the statement `x -> y` will create them with default attributes.

The distinction between key and label is critical when forming connections. Connections must always reference the
shape's key. Using a label in a connection definition will result in the creation of a new shape with that label as its
key, rather than connecting to the intended existing shape.

**Example:**

```d2
# Correct way: connect using the key 'db'
db: Production Database
db.shape: cylinder
api -> db: reads from

# Incorrect way: this creates a new shape called "Production Database"
api -> "Production Database"
```

## 2.2. The Shape Catalog

The `shape` attribute determines the geometric form of an object. If not specified, the default shape is `rectangle`. D2
provides a rich catalog of built-in shapes tailored for software and systems diagramming.

| Shape Keyword | D2 Code Example | Visual Representation (Description) | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **rectangle** | `r: Rectangle` | A standard rectangle. The default shape. | General purpose blocks, components, systems. |
| **square** | `s: {shape: square}` | A rectangle with equal width and height. | Icons, simple nodes, states. |
| **page** | `p: {shape: page}` | A rectangle with a folded top-right corner. | Documents, files, reports. |
| **parallelogram** | `p: {shape: parallelogram}` | A skewed rectangle. | Input/output operations. |
| **document** | `d: {shape: document}` | A rectangle with a wavy bottom edge. | Single documents or data files. |
| **cylinder** | `c: {shape: cylinder}` | A 3D-style cylinder. | Databases, data stores. |
| **queue** | `q: {shape: queue}` | A cylinder with an opening on one side. | Message queues, data streams. |
| **package** | `p: {shape: package}` | A 3D-style box, like a software package. | Code packages, modules, components. |
| **step** | `s: {shape: step}` | A rectangle with an arrow shape on the right. | A step in a process or flow. |
| **callout** | `c: {shape: callout}` | A rectangle with a pointer, like a speech bubble. | Annotations, notes, explanations. |
| **stored\_data** | `sd: {shape: stored_data}` | A cylinder with an open top. | Data storage, persistent data. |
| **person** | `p: {shape: person}` | A stylized icon of a person. | Users, actors, roles. |
| **diamond** | `d: {shape: diamond}` | A rhombus shape. | Decisions, conditional logic. |
| **oval** | `o: {shape: oval}` | An ellipse or oval. | Terminators (start/end), topics. |
| **circle** | `c: {shape: circle}` | A perfect circle. | Nodes, states, simple entities. |
| **hexagon** | `h: {shape: hexagon}` | A six-sided polygon. | API endpoints, services. |
| **cloud** | `c: {shape: cloud}` | A cloud shape. | Networks, internet, external systems. |
| **text** | `t: {shape: text}` | Renders only the label text with no border. | Labels, titles, annotations. |
| **code** | `c: {shape: code}` | A container for displaying formatted code. | Code snippets, examples. |
| **image** | `i: {shape: image}` | A container for a standalone image/icon. | Displaying logos, custom graphics. |
| **class** | `c: {shape: class}` | A UML class shape with compartments. | UML class diagrams. |
| **sql\_table** | `t: {shape: sql_table}` | A database table with columns and constraints. | Entity-Relationship Diagrams (ERDs). |

## 2.3. Defining Connections

Connections form the edges of the diagram graph, representing relationships between shapes.

* **Syntax**: The basic syntax is `source_key <operator> target_key`. An optional label can be added after a colon:
  `source_key -> target_key: Label text`.
* **Connection Chaining**: For readability, connections can be chained together in a single line. A label applied at the
  end of a chain applies to all connections in that chain. This is a concise way to represent a series of relationships.
  ```d2
  # The 'request' label applies to both connections
  client -> api_gateway -> backend_service: request
  ```
* **Repeated Connections**: D2 treats each connection declaration as a distinct entity. Declaring the same connection
  multiple times will render multiple, separate lines between the shapes, not override the previous one. This can be
  used to represent multiple distinct interactions between two components.
  ```d2
  # This will draw two separate arrows from 'producer' to 'queue'
  producer -> queue: event A
  producer -> queue: event B
  ```

## 2.4. Customizing Arrowheads

D2 provides extensive control over the appearance of arrowheads on connections, which is crucial for conveying precise
meaning in diagrams like ERDs. Arrowheads are customized within a connection's block using the `source-arrowhead` and
`target-arrowhead` attributes.

The language's design elegance is apparent here: these arrowhead attributes are treated as shapes themselves. This means
they can be assigned a `shape` and styled using the standard `style` keyword, demonstrating a recursive application of
the language's own rules. A label can also be added next to an arrowhead by targeting it with `.label` (e.g.,
`source-arrowhead.label: 1`).

The following table details the available arrowhead shapes and their semantic meaning.

| Arrowhead Keyword | D2 Code Example | Visual Representation (Description) | Semantic Meaning (Typical Use) |
| :--- | :--- | :--- | :--- |
| **triangle** | `target-arrowhead.shape: triangle` | A filled triangular arrowhead (default). | General direction, dependency. |
| **arrow** | `target-arrowhead.shape: arrow` | A pointier, open triangular arrowhead. | Alternative style for direction. |
| **diamond** | `target-arrowhead.shape: diamond` | An open diamond shape. | Aggregation (UML). |
| **circle** | `target-arrowhead.shape: circle` | An open circle. | Unspecified or custom notation. |
| **cf-one** | `target-arrowhead.shape: cf-one` | A single perpendicular line. | Cardinality: Exactly one (Crow's Foot). |
| **cf-one-required** | `target-arrowhead.shape: cf-one-required` | Two perpendicular lines. | Cardinality: One and only one (Crow's Foot). |
| **cf-many** | `target-arrowhead.shape: cf-many` | A three-pronged "crow's foot". | Cardinality: Zero or many (Crow's Foot). |
| **cf-many-required**| `target-arrowhead.shape: cf-many-required`| A line with a crow's foot. | Cardinality: One or many (Crow's Foot). |

**Example of styled arrowheads:**

```d2
# Connection with a filled diamond target arrowhead
composition -> part: {
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}

# ERD connection showing a one-to-many relationship
users -> posts: has {
  source-arrowhead.shape: cf-one-required
  target-arrowhead.shape: cf-many
}
```

-----

# Section 3: Composition, Hierarchy, and Layout

This section transitions from defining individual primitives to organizing them on the canvas. It covers the mechanisms
for grouping shapes into hierarchical structures and the systems that control their final placement, which is a core
benefit of the declarative approach.

## 3.1. Containers: Creating Hierarchy

Containers are shapes that can contain other shapes, allowing for the creation of logical groupings and nested diagrams.
This is fundamental for representing complex systems with multiple levels of abstraction.

**Syntax**: Nesting can be achieved in two primary ways:

* **Dot Notation**: A child object can be declared using the parent's key as a prefix, separated by a period (`.`). This
  can be done in a single line (`parent.child`) or by defining the child within a connection (
  `parent.child -> other.node`).
* **Brace Scope**: Objects defined within the curly braces (`{}`) of a parent shape are automatically considered its
  children.

<!-- end list -->

```d2
# Using brace scope
aws_cloud: {
  ec2_instance
  s3_bucket
}

# Using dot notation
aws_cloud.rds_database

# Connecting nested objects
aws_cloud.ec2_instance -> aws_cloud.rds_database
```

**Container Labels**: Like regular shapes, containers have keys and labels. The label can be defined using two syntaxes:

* **Shorthand**: `container_key: Container Label {... }`
* **`label` Keyword**: `container_key: { label: Container Label; ... }`

**Referencing Parents (`_`)**: A powerful feature for maintaining encapsulation in nested structures is the underscore (
`_`) keyword, which refers to the immediate parent of the current scope. This allows a child to form connections to its
parent's siblings or other external objects without needing to know the full, absolute path. This makes containerized
components more modular and reusable.

```d2
# Without '_', the reference is brittle
# birthdays.presents -> christmas.presents

# With '_', the reference is relative and robust
christmas: {
  presents
}
birthdays: {
  presents

  # Connect this birthday's presents to the Christmas presents
  _.christmas.presents -> presents: regift
}
```

## 3.2. Layout Engines: Controlling the Algorithm

A primary advantage of D2 is its ability to automatically calculate the positions of all diagram elements, freeing the
user from manual arrangement. This is handled by a choice of layout engines, each employing different algorithms and
offering distinct advantages. The selection of a layout engine can significantly impact the final appearance and
readability of a diagram.

The layout engine can be specified via a command-line flag (e.g., `--layout=elk`) or configured within the script using
a `vars` block.

| Engine | Algorithm Type | Key Strengths | Notable Feature Support | Recommended Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Dagre** | Hierarchical (Layered) | Fast performance. Default engine. Based on the widely-used Graphviz DOT algorithm. | Good for standard flowcharts and directed graphs. Does not support connections from ancestors to descendants (e.g., container to its child). | Quick generation of simple to moderately complex hierarchical diagrams. |
| **ELK** | Hierarchical (Layered) | Mature, well-maintained academic project. Often produces more compact and aesthetically pleasing layouts than Dagre. | Supports setting width and height on containers. Better handling of complex edge routing. | High-quality, production-ready diagrams, especially those with complex hierarchies and containers. |
| **TALA** | Custom | New engine designed specifically for software architecture diagrams. Supports novel layout constraints. | Only engine supporting `near` for positioning relative to other objects. Only engine supporting per-container `direction`. Supports `top` and `left` for fixed positioning. | Complex software architecture diagrams requiring specific positional constraints or mixed layout directions. |

The choice of engine is not merely stylistic; it has functional implications. For instance, a diagram that requires a
container to have a specific size must use **ELK**, while a diagram that needs to place a legend relative to a specific
component must use **TALA**. This demonstrates a trade-off between the engines' capabilities, which must be considered
when generating a diagram.

## 3.3. Influencing Layout: Direction and Position

While layout engines handle the complex task of positioning, D2 provides several "escape hatches" that allow the user to
influence or override the automatic layout. This creates a spectrum of control, from gentle suggestions to absolute
positioning.

* **`direction`**: This is a root-level keyword that provides a high-level hint to the layout engine about the primary
  flow of the diagram. Valid values are `up`, `down`, `left`, and `right`. This is the simplest way to change the
  overall orientation of a hierarchical diagram.
* **`near`**: This keyword offers more granular control over positioning. It can place an object at one of nine constant
  points on the canvas (e.g., `top-left`, `bottom-center`). It is commonly used for placing elements like titles and
  legends that should exist outside the main flow of the diagram. With the **TALA** engine, `near` can also be used to
  position an object relative to another object, creating a strong positional relationship. The `near` keyword is also
  used to position labels and icons relative to their parent shape's bounding box.
* **Grid Layout (`grid-rows` & `grid-columns`)**: For situations requiring absolute positional control, D2 provides a
  grid layout system. By defining `grid-rows` and/or `grid-columns` on a container, the user disables the automatic
  layout engine for its contents and instead arranges them in an explicit grid. This is the most powerful escape hatch
  and is essential for diagrams that must conform to a rigid structure, such as architectural diagrams mimicking a UI or
  a physical rack layout.
* **Gaps**: The spacing within the grid can be controlled with `grid-gap`, `vertical-gap`, and `horizontal-gap`.
* **Alignment**: A common technique for achieving complex alignments within a grid is to use invisible elements as
  spacers. By creating a shape and setting its `opacity` to `0`, it can occupy a grid cell without being visible,
  forcing other elements into the desired positions.

The existence of these mechanisms reveals a core design consideration: the tension between automation and manual
control. D2 defaults to full automation but provides a gradient of tools for users to reclaim control as needed,
culminating in the fully manual grid system.

-----

# Section 4: Visual Refinement: Styling, Theming, and Icons

This section covers the aesthetic aspects of D2 diagramming. It details the systems for applying colors, fonts, visual
effects, and icons to transform a basic structural diagram into a polished, production-ready visual artifact.

## 4.1. Applying Styles

D2's styling system is heavily influenced by CSS, using many of the same keywords and value conventions, which lowers
the learning curve for users with web development experience. Styles can be applied to shapes, connections, and even the
diagram's root canvas.

**Syntax**: There are two primary ways to apply styles:

* **`style` Block**: A `style` keyword followed by a block of key-value pairs in braces (`{}`). This is useful for
  applying multiple style properties to a single element at once.

  ```d2
  x -> y: {
    style: {
      stroke: blue
      stroke-dash: 4
      animated: true
    }
  }
  ```

* **Dot Notation**: Individual style properties can be targeted directly using dot notation. This is useful for applying
  a single style or for overriding styles defined elsewhere.

  ```d2
  x.style.fill: lightgrey
  y.style.opacity: 0.8
  ```

**Root Styling**: To style the entire diagram canvas, a `style` block can be defined at the root level of the script.
This is used to set properties like the diagram's background color or add a frame around it.

```d2
# This style block is at the root, not tied to a shape
style: {
  fill: Beige
  stroke: DarkBlue
}

x -> y
```

The following table provides a comprehensive reference for available style properties, their valid values, and their
applicability. This formalizes the rules of the styling system, which is essential for correct programmatic generation.

| Property Keyword | Applies To | Value Type & Range | Description | D2 Code Example |
| :--- | :--- | :--- | :--- | :--- |
| **`opacity`** | Shapes, Connections | Float 0.0 - 1.0 | Sets the transparency. | `x.style.opacity: 0.5` |
| **`stroke`** | Shapes, Connections | Color (name or hex) | Sets the color of the border/line. | `x.style.stroke: "#ff0000"` |
| **`fill`** | Shapes | Color (name or hex) | Sets the interior background color. | `x.style.fill: lightblue` |
| **`fill-pattern`** | Shapes | `dots`, `lines`, `grain` | Applies a texture to the fill. | `x.style.fill-pattern: dots` |
| **`stroke-width`** | Shapes, Connections | Integer 1 - 15 | Sets the thickness of the border/line. | `x.style.stroke-width: 3` |
| **`stroke-dash`** | Shapes, Connections | Integer 0 - 10 | Sets the dash pattern of the line. 0 is solid. | `(x -> y).style.stroke-dash: 5` |
| **`border-radius`** | Shapes | Integer 0 - 20 | Rounds the corners of the shape. | `x.style.border-radius: 10` |
| **`shadow`** | Shapes | `true`, `false` | Adds a drop shadow to the shape. | `x.style.shadow: true` |
| **`3d`** | `rectangle`, `square` | `true`, `false` | Gives the shape a 3D extruded effect. | `x.style.3d: true` |
| **`multiple`** | Shapes | `true`, `false` | Renders a "stack" of shapes. | `x.style.multiple: true` |
| **`double-border`**| `rectangle`, `oval` | `true`, `false` | Draws a second border around the shape. | `x.style.double-border: true` |
| **`font`** | Text Labels | `mono` | Sets the font family. `mono` is currently the main option. | `x.style.font: mono` |
| **`font-size`** | Text Labels | Integer 8 - 100 | Sets the size of the label text. | `x.style.font-size: 24` |
| **`font-color`** | Text Labels | Color (name or hex) | Sets the color of the label text. | `x.style.font-color: navy` |
| **`animated`** | Connections | `true`, `false` | Adds an animation effect to the connection line. | `(x -> y).style.animated: true` |
| **`bold`** | Text Labels | `true`, `false` | Makes the label text bold. | `x.style.bold: true` |
| **`italic`** | Text Labels | `true`, `false` | Makes the label text italic. | `x.style.italic: true` |
| **`underline`** | Text Labels | `true`, `false` | Underlines the label text. | `x.style.underline: true` |
| **`text-transform`**| Text Labels | `uppercase`, `lowercase`, `title` | Changes the case of the label text. | `x.style.text-transform: uppercase` |

## 4.2. Icons and Images

D2 provides first-class support for embedding icons and images into diagrams, which is essential for creating modern,
visually rich software architecture diagrams.

* **`icon` Attribute**: The `icon` attribute is added to a shape's definition to place an icon within it. The value can
  be a URL to a remote image or a relative file path to a local image when using the D2 CLI. Terrastruct, the creators
  of D2, host a free library of common software and cloud architecture icons to facilitate this process.

  ```d2
  # Using a remote icon from the hosted library
  api: {
    icon: [https://icons.terrastruct.com/aws%2FCompute%2FAmazon-EC2_C4-Instance_light-bg.svg](https://icons.terrastruct.com/aws%2FCompute%2FAmazon-EC2_C4-Instance_light-bg.svg)
  }

  # Using a local icon
  my_server: {
    icon: ./icons/server.png
  }
  ```

* **`shape: image`**: To create a shape that consists only of an image, without any surrounding border, fill, or label
  background, the `shape: image` attribute is used. This is ideal for using logos or custom graphics as standalone nodes
  in a diagram.

  ```d2
  github: {
    shape: image
    icon: [https://icons.terrastruct.com/dev/github.svg](https://icons.terrastruct.com/dev/github.svg)
  }
  ```

* **Icon Positioning**: By default, icon placement is automatic. The layout engine typically places icons in the
  top-left corner for containers (to avoid obscuring child elements) and in the center for non-container shapes. For
  manual control, the `near` keyword can be used within the icon's scope (e.g., `icon.near: outside-top-right`) to
  specify a precise position relative to the shape's boundary.

## 4.3. Theming and Global Aesthetics

For high-level control over the look and feel of a diagram, D2 provides themes and global rendering modes.

* **Themes**: D2 ships with a set of numbered, built-in themes that define a cohesive palette of colors, fonts, and
  styles. Applying a theme is the fastest way to give a diagram a professional appearance. Themes can be applied in
  several ways, with CLI flags taking precedence over in-script definitions:

    * **CLI Flag**: `d2 --theme=101 my_diagram.d2`
    * **Environment Variable**: `D2_THEME=101 d2 my_diagram.d2`
    * **In-script `vars` block**: `vars: { d2-config: { theme-id: 101 } }`

* **Sketch Mode**: This is a global rendering option that transforms the entire diagram, giving it a hand-drawn, "
  whiteboard" aesthetic. This can make diagrams feel more informal and approachable. It can be enabled via a CLI flag (
  `--sketch`) or an in-script `vars` definition (`sketch: true`).

* **Dark Mode Responsiveness**: D2 diagrams can be made to automatically adapt to the end-user's operating system
  preference for light or dark mode. This is achieved by specifying a `dark-theme-id` in the `d2-config` variable block.
  When the diagram is viewed in a browser that supports this media query, it will automatically switch between the
  default `theme-id` and the `dark-theme-id`.

The application of visual styles in D2 follows a clear cascading hierarchy of precedence, similar to CSS. An explicitly
set inline style (e.g., `x.style.fill: red`) will always override styles inherited from a class, which in turn override
styles from a theme. This layered system provides both broad, easy-to-apply aesthetics via themes and granular, powerful
control via direct styling.

-----

# Section 5: Advanced Abstraction and Modularity

This section explores the most powerful, programming-like features of the D2 language. These constructs are not merely
for styling or layout; they provide mechanisms for abstraction, reuse, and modularity. They elevate D2 from a simple
diagramming tool to a sophisticated system for creating and maintaining large-scale, complex documentation as code.
These features are interconnected and work in synergy to enable advanced workflows.

## 5.1. `vars`: Variables and Substitutions

The `vars` keyword introduces a special block at the root of a D2 script where variables can be defined. This allows for
the reuse of values like colors, labels, or server names, promoting consistency and making diagrams easier to maintain.

* **Definition and Substitution**: Variables are defined as key-value pairs within the `vars` block. They are then
  referenced elsewhere in the script using the substitution syntax `${variable.name}`.

  ```d2
  vars: {
    primary-color: "#4baae5"
    region: "us-east-1"
  }

  api: API Server in ${region}
  api.style.fill: ${primary-color}
  ```

* **Scoping**: Variables are lexically scoped. A variable defined in an inner scope (e.g., inside a container) is not
  accessible from an outer scope. When a substitution is made, the parser uses the variable definition from the nearest
  enclosing scope.

* **Spread Operator**: For variables that hold an array or a map, the spread operator `...${variable}` can be used to
  inject the contents of the variable into another array or map. This is particularly useful for composing complex
  attribute sets, such as SQL constraints.

  ```d2
  vars: {
    common-constraints:
  }
  users: {
    shape: sql_table
    id: int {constraint: [PK; ...${common-constraints}]}
  }
  ```

* **Configuration**: A special variable, `d2-config`, can be defined within `vars` to set global configuration options
  that would otherwise be passed as CLI flags. This allows a D2 file to be self-contained, specifying its own theme,
  layout engine, and other properties.

  ```d2
  vars: {
    d2-config: {
      theme-id: 4
      layout-engine: elk
      sketch: true
    }
  }
  ```

## 5.2. `classes`: Reusable Attribute Sets

While variables are for reusing single values, `classes` are for reusing entire sets of attributes. The `classes` block
allows you to define a named collection of styles and other properties that can be applied to multiple objects.

* **Definition and Application**: Classes are defined in a root-level `classes` block. They are then applied to an
  object using the `class` attribute.

  ```d2
  classes: {
    database: {
      shape: cylinder
      style.fill: "#44C7B1"
    }
    unhealthy: {
      style.stroke: red
      style.stroke-dash: 4
    }
  }

  pg_db.class: database
  redis_cache.class: [database; unhealthy] # Multiple classes can be applied
  ```

* **Overrides**: The styling cascade applies to classes. Attributes defined directly on an object will always override
  conflicting attributes inherited from its class. In the example above, if `redis_cache` had `style.stroke: orange`
  defined, it would override the red stroke from the `unhealthy` class.

* **Use as Tags**: A significant secondary function of classes is for semantic tagging. When a D2 diagram is rendered to
  SVG, any applied classes are written into the SVG element's `class` attribute. This allows for powerful
  post-processing with external CSS or JavaScript, enabling interactivity or custom styling beyond D2's native
  capabilities.

## 5.3. `globs`: Wildcard Targeting

D2 supports glob patterns, using the asterisk (`*`) as a wildcard to target multiple objects simultaneously. This is an
efficient way to apply styles or create connections for a group of objects without naming each one individually.

```d2
# Define several services
service_a; service_b; service_c

# Style all of them at once using a glob
*.style.fill: yellow

# Connect a gateway to all of them
api_gateway -> *
```

## 5.4. `imports` and the Model-View Pattern

The features of variables, classes, and globs culminate in D2's most advanced capability: building modular and scalable
documentation systems using the model-view pattern. This is enabled by the `imports` keyword and the `suspend`/
`unsuspend` lifecycle.

* **`imports`**: D2 scripts can import other `.d2` files. This allows a diagram's definition to be split across multiple
  files, separating concerns.
* **`suspend` and `unsuspend`**: These keywords, often combined with globs, control the visibility of objects. `suspend`
  removes an object from the rendered diagram, while `unsuspend` makes it visible again.

These mechanisms enable a powerful workflow for **documentation-as-code**:

1. **Model Definition**: A central file, e.g., `models.d2`, is created to define all the components, actors, and systems
   of a software architecture. This file acts as the single source of truth. It uses `vars` and `classes` for
   consistency.
2. **View Creation**: Separate view files, e.g., `user_login_flow.d2` or `data_backup_process.d2`, are created for
   specific diagrams.
3. **Implementation**: Each view file imports the central `models.d2` file. It then begins by suspending everything (
   `*.*.suspend`). Finally, it selectively `unsuspends` only the components and connections that are relevant to that
   specific view.

This pattern decouples the definition of the system's components from their presentation in any single diagram. It
allows for the generation of dozens of focused, easy-to-understand diagrams from a single, maintainable model. This is
the cornerstone of creating documentation that can scale with a complex system and is a clear indicator that D2 is
designed for integration into automated CI/CD pipelines, much like infrastructure-as-code tools.

-----

# Section 6: Specialized Diagram Types

While D2's core syntax is flexible, its true power for software documentation comes from its specialized shape types.
These shapes are not just visual skins; they contain domain-specific parsers that interpret their content using a
unique "mini-DSL." Understanding these specialized syntaxes is critical for leveraging D2's full potential.

## 6.1. `shape: sql_table` - Entity-Relationship Diagrams

D2 has first-class support for creating Entity-Relationship Diagrams (ERDs) using the `sql_table` shape. The parser for
this shape is designed to understand the structure of a database table.

* **Syntax**: The container's key becomes the table name. Inside the block, each key-value pair defines a column. The
  key is the column name, and the first value is its data type.
* **Constraints**: SQL constraints can be added as a secondary value after the data type. D2 recognizes and abbreviates
  `primary_key` to `PK`, `foreign_key` to `FK`, and `unique` to `UNQ`. Multiple constraints can be specified using an
  array.
* **Connections**: Foreign key relationships are visualized by creating standard D2 connections between the specific
  columns of the tables. When using the **ELK** or **TALA** layout engines, these connections will intelligently point
  to the exact row in the table shape.

<!-- end list -->

```d2
users: {
  shape: sql_table
  id: int {constraint: PK}
  username: varchar {constraint: UNQ}
  created_at: timestamp
}

posts: {
  shape: sql_table
  id: int {constraint: PK}
  author_id: int {constraint: FK}
  content: text
}

# Define the foreign key relationship
posts.author_id -> users.id
```

## 6.2. `shape: class` - UML Class Diagrams

For object-oriented design, D2 provides a `class` shape that mimics the structure of a UML class diagram.

* **Syntax**: The container's key is the class name. Inside the block, attributes (fields) and operations (methods) are
  listed. The parser differentiates between them by looking for parentheses (`()`) in the definition, which signifies a
  method.
* **Styling**: Individual fields and methods can be styled. For example, `style.underline` can be used to indicate a
  static method or attribute.

<!-- end list -->

```d2
UserRepository: {
  shape: class
  -db_connection: Connection
  +findById(id: int): User
  +save(user: User): bool
}
```

## 6.3. `shape: sequence_diagram` - Sequence Diagrams

Sequence diagrams are unique in D2 because they are the primary exception to the rule that statement order does not
affect the final layout. For this shape, temporal order is paramount, so the script order directly maps to the vertical
sequence of messages.

* **Syntax**: A container is given `shape: sequence_diagram`. Inside this block, actors are defined implicitly by their
  use in connections. Each connection represents a message passed between actors.
* **Order Matters**: The vertical order of the messages in the final diagram is determined by their order in the D2
  script. This is a fundamental departure from D2's normal declarative model and must be respected when generating
  sequence diagrams.

<!-- end list -->

```d2
auth_flow: {
  shape: sequence_diagram
  user -> frontend: Enters credentials
  frontend -> backend: POST /login
  backend -> database: Verify credentials
  database -> backend: User record
  backend -> frontend: Auth Token
  frontend -> user: Logged in
}
```

## 6.4. Text, Code, and LaTeX

D2 provides powerful capabilities for rendering text, code, and mathematical formulas, which are essential for technical
documentation.

* **`shape: code`**: This shape is used to display syntax-highlighted code snippets. The programming language is
  specified as part of the block string definition (e.g., `|go... |`), and D2 will apply the appropriate highlighting.

  ```go
  example: |go
  func main() {
      fmt.Println("Hello, D2")
  }
  |
  ```

* **LaTeX Support**: For academic papers and technical specifications requiring mathematical notation, D2 can render
  LaTeX. A block is designated as LaTeX using `|latex... |` or `|tex... |`. D2's renderer includes several common LaTeX
  plugins, such as `amsmath` for advanced math environments and `mhchem` for chemical formulas.

  ```latex
  formula: |latex
    E = mc^2
  |
  ```

The existence of these highly specialized shapes underscores D2's commitment to its domain. The `shape` attribute acts
as a switch that can fundamentally alter how the parser interprets the content of a block, activating a mini-DSL
tailored to a specific diagramming need.

-----

# Section 7: Execution Environment and Tooling

This final section details the practical aspects of using D2, including installation, command-line execution, and
integration with the broader development ecosystem. This information is necessary for compiling D2 scripts and
incorporating them into automated workflows.

## 7.1. Installation and Execution

D2 is primarily a command-line tool, designed to be run in a developer's local environment or on a server.

* **Installation**: D2 can be installed through several methods to accommodate different operating systems and
  workflows:

    * **Install Script**: The official `install.sh` script, downloadable from the D2 website, is the recommended method
      for Linux and macOS.
    * **Go Install**: For users with the Go programming language toolchain installed, D2 can be installed from source
      using `go install oss.terrastruct.com/d2@latest`.
    * **Package Managers**: D2 is available in popular package managers like Homebrew for macOS (`brew install d2`) and
      Winget for Windows.

* **CLI Usage**: The `d2` executable is the primary interface for compiling `.d2` files into visual diagrams.

    * **Basic Compilation**: The simplest invocation takes an input file and an output file. The output format is
      inferred from the file extension (`.svg`, `.png`, `.pdf`).
      ```bash
      d2 my_diagram.d2 my_diagram.svg
      ```
    * **Watch Mode**: A key feature for development is watch mode, enabled with the `--watch` or `-w` flag. This command
      starts a local web server that hosts the output SVG. It monitors the input `.d2` file for changes and
      automatically recompiles and live-reloads the diagram in the browser, providing instant feedback.
      ```bash
      d2 --watch my_diagram.d2
      ```
    * **Flags**: The CLI accepts numerous flags to control the output, such as `--theme`, `--layout`, and `--sketch`,
      which correspond to the configuration options discussed in previous sections.

## 7.2. Tooling and Integration

D2 is supported by a growing ecosystem of tools that integrate it into common developer workflows.

* **Official Editor Support**: To facilitate writing D2 code, official extensions are available for popular code
  editors, including Visual Studio Code and Vim. These extensions typically provide syntax highlighting, code snippets,
  and in-editor diagram previews.
* **Online Playground**: The D2 Playground is a hosted web application available on the official D2 website. It provides
  an in-browser editor and renderer, allowing users to quickly experiment with D2 syntax, create diagrams, and share
  them with others via a URL without needing to install anything locally.
* **Language API (`d2oracle`)**: For advanced programmatic use cases, D2 exposes a Go language API named `d2oracle`.
  This library provides access to the language's Abstract Syntax Tree (AST), allowing developers to programmatically
  create, analyze, or modify D2 diagrams in Go code. This is the foundation for building custom tools or automation on
  top of the D2 language.
* **Third-Party Integrations**: D2's simple text-based format and powerful CLI make it easy to integrate with other
  tools. For example, it can be used within knowledge management applications like Obsidian by using a `d2` code fence.
  Its design for server-side execution also makes it a prime candidate for integration into Continuous
  Integration/Continuous Delivery (CI/CD) pipelines, where it can be used to automatically generate and update system
  architecture diagrams whenever the underlying code or infrastructure changes.

-----

# Section 8: Conclusion

This guide provides a comprehensive specification of the D2 Declarative Diagramming language, structured for
programmatic understanding and generation. The analysis reveals that D2 is not merely a tool for drawing pictures but a
sophisticated DSL engineered with a clear philosophy and a singular focus on documenting software systems. For an AI to
achieve mastery in generating D2 code, it must internalize several core concepts that define the language's structure
and intent.

First, the **declarative paradigm** is paramount. The AI's primary task is to describe the *what*—the shapes and their
relationships—not the *how* or *where*. The layout engines are responsible for placement, and the AI should trust them
by default, only resorting to positional overrides like `grid` when the user's intent explicitly demands a fixed,
non-algorithmic layout.

Second, the **separation of key and label** is a fundamental architectural choice that ensures diagram stability. The AI
must learn to generate stable, unique keys for programmatic reference while treating labels as mutable,
presentation-layer text. This prevents structural breakage when visual text is updated.

Third, D2's visual output is governed by a **cascading system of styles**. The AI should understand the hierarchy of
precedence: from broad themes, to reusable classes, to specific inline style attributes. This knowledge is crucial for
applying visual changes with the correct level of specificity and for predicting the final appearance of a diagram.

Finally, the most advanced features—**`vars`, `classes`, `globs`, `imports`, and `suspend`/`unsuspend`**—are not
isolated tools but an interconnected suite for enabling a model-view architecture. The AI should recognize that the
ultimate goal of these features is to support a scalable, documentation-as-code workflow. Generating idiomatic D2 for
complex systems involves thinking in terms of a central, reusable model from which multiple, focused views are derived.

By internalizing these principles—its declarative nature, the key/label distinction, the styling cascade, and the
model-view pattern—an AI can move beyond simple syntactic correctness to generate diagrams that are not only valid but
also idiomatic, maintainable, and aligned with the core philosophy of the D2 language.

-----

# A Technical Specification for Generating UML Class Diagrams in D2

## 6.2 `shape: class` — A Definitive Guide to UML Class Diagrams

This section provides a comprehensive specification for generating Unified Modeling Language (UML) Class Diagrams using
the D2 declarative language. It is designed to serve as a canonical reference, particularly for programmatic generation
systems. The analysis moves from the foundational syntax of the `class` shape to the systematic composition of complex
semantic relationships, establishing definitive D2 patterns for standard UML concepts.

The core principle for modeling UML in D2 is the use of the specialized `shape: class` primitive.[1] Assigning this
shape to a container acts as a directive that activates a domain-specific "mini-DSL" parser. This parser interprets the
contents of the container block according to the specific rules of UML class members, which are distinct from the
standard D2 object and connection syntax. Mastery of this specialized shape and its associated compositional patterns is
essential for creating accurate and semantically rich object-oriented models.

### 6.2.1 Core Class Definition: Syntax and Parsing Rules

The definition of a class structure—its attributes, operations, and their visibility—is the fundamental building block
of any class diagram. D2 provides a precise and consistent syntax for these elements.

#### Fundamental Declaration

The process begins by declaring a D2 object (a container) and assigning it the `shape: class` attribute. This
declaration is the entry point that instructs the D2 compiler to use the specialized UML class parser for the contents
within the object's curly braces `{}`.[2]

**Syntax:**

```d2
# Declares a UML class named 'UserRepository'
UserRepository: {
  shape: class
  # Members are defined here
}
```

#### Member Definition Parsing Logic

Within a `shape: class` block, the parser uses a simple yet absolute rule to differentiate between attributes (fields)
and operations (methods). This distinction is the single most important parsing logic to internalize for correct member
generation. The determining factor is the **presence of parentheses `()`** in a member's key.[2]

* **Attributes (Fields)**: A key defined *without* parentheses is parsed as an attribute. The canonical syntax is
  `attributeName: Type`. The `Type` portion is treated by the parser as an uninterpreted string literal. This provides
  the flexibility to define simple types (`int`), complex generic types, or fully-qualified type names (`"string"`,
  `io.RuneReader`).[2]

  **Syntax:**

  ```d2
  # An attribute 'id' of type 'int'
  id: int

  # An attribute 'items' of a complex string array type
  items: "string"[]
  ```

* **Operations (Methods)**: A key that *includes* parentheses is parsed as an operation. The canonical syntax is
  `operationName(parameters): returnType`. As with attributes, the `parameters` and `returnType` are uninterpreted
  string literals, allowing for any signature complexity. If the colon and return type are omitted, the operation's
  return type is implicitly considered `void`.[2]

  **Syntax:**

  ```d2
  # An operation 'findById' with one parameter, returning a 'User' type
  findById(id: int): User

  # An operation 'save' with no explicit return type (void)
  save(user: User)
  ```

#### Visibility Prefixes

D2 uses standard UML prefixes to denote the visibility of class members. These prefixes are placed at the beginning of
the member's key.[4] The supported visibilities are:

* `+` (public): The member is accessible from any other class.
* `-` (private): The member is accessible only from within the class itself.
* `#` (protected): The member is accessible from within the class and by its subclasses.
* (none): If no prefix is provided, the visibility defaults to public.

**Code Example:**

```d2
D2Parser: {
  shape: class

  # Public visibility (explicit and default)
  +reader: io.RuneReader
  readerPos: d2ast.Position

  # Private visibility
  -lookahead: "rune"

  # Protected visibility (see note below)
  \#lookaheadPos: d2ast.Position
}
```

A critical instruction for programmatic generation involves the **protected visibility marker**. The D2 language parser
processes the entire script for comments, which are denoted by the hash symbol (`#`), before any specialized shape
parsers are invoked.[1] An unescaped `#` at the beginning of a member definition would cause the parser to interpret the
entire line as a comment, discarding it before it ever reaches the `shape: class` parser. To prevent this, the hash
symbol for protected members **must be escaped with a backslash (`\`)**. This ensures the literal `#` character is
passed as part of the key to the class parser, which then correctly interprets it as the protected visibility marker.
This is a crucial, non-obvious exception that must be handled to prevent syntax errors.[2]

### 6.2.2 Modeling UML Relationships: The Compositional Method

A core design aspect of D2 is that it does not provide high-level, single-keyword abstractions for each type of UML
relationship (e.g., a hypothetical `relationship: inheritance` keyword). Instead, D2 requires the diagram author to *
*compose** these complex semantic concepts from a small set of orthogonal, low-level primitives. The primary primitives
used are:

* **Connection Operators**: The fundamental line type, either undirected (`--`) or directed (`->`, `<-`, `<->`).
* **Arrowhead Shapes**: The geometric shape of the connection's endpoint, defined via `source-arrowhead` and
  `target-arrowhead`.
* **Connection Styles**: Visual modifiers like line style (`stroke-dash`) and fill (`filled`).

A generating system's task is not to find a one-to-one mapping for a UML relationship, but to learn the correct **"
recipe"** of D2 primitives for each relationship type.

The following table and subsections define the canonical D2 recipes for all standard UML class relationships.

| UML Relationship | Semantic Meaning | D2 Connection | `target-arrowhead.shape` | Required Styles |
| :--- | :--- | :--- | :--- | :--- |
| **Association** | A structural link between peers. | `Source -> Target` | `triangle` (default) | `style.filled: true` (default) |
| **Dependency** | A "using" relationship; changes to the supplier may affect the client. | `Client -> Supplier` | `arrow` or `triangle` | `style.stroke-dash: 4` |
| **Generalization** | An "is-a" relationship (inheritance). | `Subclass -> Superclass` | `triangle` | `style.filled: false` |
| **Realization** | An "implements" relationship (interface). | `Class -> Interface` | `triangle` | `style.stroke-dash: 4`, `style.filled: false`|
| **Aggregation** | A "has-a" relationship where the part can exist independently. | `Part -> Whole` | `diamond` | `style.filled: false` |
| **Composition** | A strong "has-a" relationship where the part cannot exist independently.| `Part -> Whole` | `diamond` | `style.filled: true` |

#### Association

Association is the most general structural relationship between classes. It is represented by a solid line. A directed
arrow (`->`) should be used to imply navigability from the source class to the target class.[4]

**D2 Recipe:**

```d2
# An association where Customer can navigate to Order
Customer -> Order: places
```

#### Dependency

A dependency indicates that one element (the client) depends on another (the supplier). In UML, this is conventionally
shown as a dashed line with a standard open arrowhead.[4]

**D2 Recipe:** A directed connection (`->`) is styled with `stroke-dash`. A value of `4` is a common choice for a
visible dash pattern.

```d2
ReportGenerator -> PDFLibrary: uses {
  style: {
    stroke-dash: 4
  }
}
```

#### Generalization (Inheritance)

Generalization represents an "is-a" relationship, commonly known as inheritance. The UML standard notation is a solid
line with a large, hollow (unfilled) triangle arrowhead that points from the subclass (the child) to the superclass (the
parent).[4] While some D2 examples may show simpler representations, the addition of the "unfilled triangle arrowhead"
in version 0.6.2 established the capability for a semantically correct visualization.[8] This recipe should be
considered the canonical and correct form.

**D2 Recipe:**

```d2
# SavingsAccount "is-a" Account
SavingAccount -> Account: {
  target-arrowhead: {
    shape: triangle
    style.filled: false
  }
}
```

#### Realization (Interface Implementation)

Realization signifies that a classifier (the client) implements the contract specified by an interface (the supplier).
The UML standard is a dashed line with a large, hollow triangle arrowhead, pointing from the implementing class to the
interface.[9] This D2 recipe is a logical synthesis of the established patterns for Dependency (dashed line) and
Generalization (hollow triangle arrowhead), as no single document explicitly provides this pattern.

**D2 Recipe:**

```d2
# S3Uploader "implements" IFileUploader
S3Uploader -> IFileUploader: {
  style: {
    stroke-dash: 4
  }
  target-arrowhead: {
    shape: triangle
    style.filled: false
  }
}
```

#### Aggregation

Aggregation is a "has-a" or "part-of" relationship where the part can exist independently of the whole. The UML standard
is a solid line with a hollow (unfilled) diamond at the end connected to the "whole" class (the aggregate).[4]

**D2 Recipe:**

```d2
# A Department "has-a" Teacher, but a Teacher can exist without a Department
Teacher -> Department: {
  target-arrowhead: {
    shape: diamond
    style.filled: false
  }
}
```

#### Composition

Composition is a strong form of aggregation where the part cannot exist independently of the whole; its lifecycle is
tied to the whole. The UML standard is a solid line with a filled diamond at the end connected to the "whole" class (the
composite).[4] D2 elegantly models this distinction from aggregation by simply toggling a boolean style property.

**D2 Recipe:**

```d2
# An Order "has" OrderLines, which cannot exist without the Order
OrderLine -> Order: {
  target-arrowhead: {
    shape: diamond
    style.filled: true
  }
}
```

### 6.2.3 Advanced Relationship Annotations: Multiplicity and Role Names

D2 employs a highly idiomatic and non-obvious pattern for annotating the ends of a connection. Instead of providing
structured attributes like `multiplicity="1..*"` or `role="client"`, it leverages the fact that `source-arrowhead` and
`target-arrowhead` are themselves objects that can have labels. The multiplicity and role names are assigned as simple
string values to these implicit label properties.

#### Multiplicity

The cardinality of a relationship (e.g., `1`, `0..*`, `1..*`) is defined by assigning the multiplicity string directly
as the value for the `source-arrowhead` or `target-arrowhead` key. This acts as a powerful shorthand for setting the
label of the arrowhead object.[2] The multiplicity notations themselves are uninterpreted strings.

**D2 Syntax:**

```d2
# A Customer can have 0 or more Orders.
# An Order belongs to exactly 1 Customer.
Customer -> Order: places {
  source-arrowhead: "1"
  target-arrowhead: "0..*"
}
```

This shorthand syntax (`source-arrowhead: "1"`) is the idiomatic form found in documentation and is equivalent to the
more verbose `source-arrowhead: { label: "1" }`. Programmatic generators should prefer the shorthand for conciseness.

#### Role Names and Association Labels

A clear distinction must be made between the different labels on a connection:

* **Association Name**: This is the primary label on the connection itself, defined after the colon (e.g.,
  `Customer -> Order: places`). It names the relationship.
* **Role Names**: These are labels applied specifically to the arrowheads to clarify the role played by the class at
  that end of the association.

While not explicitly documented, the most robust way to specify a role name is to use the more verbose `.label` syntax
on the arrowhead object. For cases requiring both multiplicity and a role name, they can be combined into a single
string.

**D2 Syntax Example:**

```d2
# An Order is composed of 1 or more OrderItems (the 'items' role)
OrderItem -> Order: {
  source-arrowhead: "1..* items"
  target-arrowhead: "1"
  #... composition arrowhead shape
}
```

### 6.2.4 Advanced Class Annotations: Modifiers and Stereotypes

D2 provides no first-class language support for UML concepts like stereotypes or abstract/static modifiers. These are
considered presentation-layer concerns. A generating system must learn to represent these semantic concepts by adhering
to established UML visual conventions and using D2's general-purpose features like string formatting and styling.

#### Stereotypes (`<<interface>>`, `<<abstract>>`)

The standard UML representation for a stereotype is the stereotype name enclosed in guillemets (`<< >>`).

**D2 Implementation:** The stereotype is prepended to the class's label string, often with a newline character (`\n`)
for better visual separation. For an abstract class, it is conventional to also style the class name in italics.

```d2
# An interface with a stereotype
IAuthenticationService: "<<interface>>\nIAuthenticationService" {
  shape: class
  # It is also conventional to italicize the label for interfaces and abstract classes
  style.italic: true
}

# An abstract class with a stereotype
AbstractRepository: {
  shape: class
  label: "<<abstract>>\nAbstractRepository"
  style.italic: true
}
```

#### Static and Abstract Member Modifiers

In UML, static members are conventionally underlined, and abstract members are italicized.[4] D2 provides the style
properties `style.underline: true` and `style.italic: true`.[14]

However, a significant limitation exists: the D2 `shape: class` parser does not currently support applying styles to
individual members within the class block. All styling examples in the documentation apply to the entire shape
container.[14]

Therefore, a generating AI must be explicitly instructed to avoid generating invalid code that attempts to style
individual members. The correct approach is to acknowledge this limitation and use textual documentation as a
workaround.

**Instruction for Programmatic Generation:** To denote a static or abstract member, the semantic information cannot be
directly visualized on a per-member basis using underlining or italics. This information should be documented textually,
either in an associated Markdown block within the diagram or as a comment in the D2 source code.

### 6.2.5 Synthesis: A Comprehensive Example and Generation Strategy

This final section integrates all preceding concepts into a single, comprehensive example and provides a set of
high-level strategic rules for programmatic generation.

#### Full Example: E-Commerce System

The following D2 script models a simple e-commerce system. It serves as a "golden" reference, demonstrating the correct,
canonical application of all concepts covered in this guide.

```d2
#
# A comprehensive UML Class Diagram example in D2
#

# --- 1. Class Definitions ---
IPaymentGateway: "<<interface>>\nIPaymentGateway" {
  shape: class
  style.italic: true
  processPayment(amount: float): bool
}

StripeProcessor: {
  shape: class
  -apiKey: string
  +processPayment(amount: float): bool
}

Customer: {
  shape: class
  -id: string
  +name: string
  +billingAddress: Address
}

Order: {
  shape: class
  -orderId: string
  -orderDate: Date
  +totalAmount: float
  +ship()
}

OrderItem: {
  shape: class
  +productId: string
  +quantity: int
  +price: float
}

Address: {
  shape: class
  +street: string
  +city: string
  +zipCode: string
}

# --- 2. Relationship Definitions ---

# Realization: StripeProcessor implements the IPaymentGateway interface
StripeProcessor -> IPaymentGateway: {
  style.stroke-dash: 4
  target-arrowhead: {
    shape: triangle
    style.filled: false
  }
}

# Composition: An Order is composed of OrderItems.
# The OrderItem cannot exist without the Order.
OrderItem -> Order: {
  source-arrowhead: "1..*"
  target-arrowhead: {
    label: "1"
    shape: diamond
    style.filled: true
  }
}

# Aggregation: An Order has a shipping Address.
# The Address can exist independently of the Order.
Address -> Order: "has shipping address" {
  source-arrowhead: "1"
  target-arrowhead: {
    label: "1"
    shape: diamond
    style.filled: false
  }
}

# Association: A Customer places Orders.
Customer -> Order: places {
  source-arrowhead: "1"
  target-arrowhead: "0..*"
}

# Dependency: The Order class depends on the payment gateway to process payments.
Order -> IPaymentGateway: uses {
  style.stroke-dash: 4
}
```

#### Strategic Recommendations for AI Generation

To generate D2 code that is not just syntactically correct but also idiomatic, readable, and maintainable, a
programmatic system should adhere to the following high-level rules:

1. **Abstract with `vars` and `classes`**: For large or complex diagrams, use D2's abstraction mechanisms. Define common
   data types or configuration in a `vars` block (e.g., `vars: { id_type: string }`) for reuse via substitution (
   `${id_type}`). Use the `classes` block to define reusable attribute sets, which is ideal for creating styles for
   stereotypes. This promotes the Don't Repeat Yourself (DRY) principle and enhances maintainability.[16]
   ```d2
   classes: {
     interface: {
       style.italic: true
       # Other common interface styles
     }
   }
   IPaymentGateway.class: interface
   ```
2. **Structure for Readability**: Generate D2 scripts in logical blocks. A recommended structure is to first define all
   `shape: class` objects and their members, and then define all of the connection-based relationships between them.
   This separation of concerns greatly enhances human readability and aligns with a model-view approach to
   documentation.
3. **Adhere to Canonical Forms**: The generating system must always produce the canonical relationship representations
   as defined in the "UML Relationship to D2 Syntax Mapping" table in section 6.2.2. This ensures consistency and
   semantic accuracy across all generated diagrams, even if simpler or alternative syntaxes might exist in older
   documentation.
4. **Handle Parser Exceptions Proactively**: The system must include a specific rule to handle the `#` escaping
   requirement for protected members. This is a common and non-obvious point of failure. The generation logic should
   automatically prepend a backslash (`\`) to any member key that begins with a `#` to ensure it is parsed correctly.

-----

# Advanced Composition in D2: A Technical Reference on Layers, Boards, and Linking for AI-Driven Diagram Generation

## The Philosophy of Composition in D2: Boards vs. Containers

The D2 declarative diagramming language provides two distinct yet complementary mechanisms for grouping and organizing
diagram elements: **containers** and **boards**. A comprehensive understanding of their fundamental differences in
structure, scope, and purpose is paramount for the programmatic generation of complex, maintainable, and interactive
architectural diagrams. While both serve to manage complexity, they operate on different conceptual levels. **Containers
** provide hierarchical organization on a single visual canvas, whereas **boards** enable the creation of multiple,
distinct canvases that can be navigated to represent different views or levels of abstraction.

### Defining the Container: Hierarchical Grouping on a Single Canvas

A **container** in D2 is a shape that logically and visually groups other shapes and connections within the same diagram
canvas. It functions as a namespacing and organizational tool, establishing a parent-child relationship between
elements. The primary purpose of a container is to structure a single, coherent diagram by delineating subsystems,
components, or other logical boundaries. All elements within a container, and the container itself, are rendered
together on the same output canvas.

D2 offers two syntactically equivalent methods for defining containers, providing flexibility for the author or
generating system.

The first and most direct method is **dot notation**. By using a dot (`.`) in a shape's identifier, a parent-child
relationship is established. If the parent container does not exist, it is created automatically. This method is concise
and particularly useful for declaring a child and its container in a single line.

```d2
# Using dot notation to create containers and children.
# This single line creates a container 'aws' and a child 'server' within it.
aws.server

# Connections can also implicitly create containers.
# This creates a container 'gcp' with a child 'database' and connects it to 'aws.server'.
aws.server -> gcp.database
```

The second method is the **nested map syntax**. This approach uses curly braces (`{}`) to define a container and enclose
its children. This style is often more structured and readable for defining multiple children within the same container,
as it visually represents the hierarchy through indentation.

```d2
# Using nested map syntax for a more structured definition.
aws: {
  # 'server' is a child of the 'aws' container.
  server

  # Containers can be nested.
  networking: {
    vpc
    load_balancer
  }
}

# Connections to nested children must use the full path.
user -> aws.networking.load_balancer
```

Regardless of the syntax used, the scoping model for containers is strictly hierarchical and confined to the single
board on which they are defined. To reference an object within a container from outside of it, one must specify its full
path from the root of the board, using dot notation (e.g., `container.child.grandchild`). This predictable namespacing
is essential for preventing ambiguity in large diagrams. The primary use case for containers is to represent the static,
logical structure of a system where all components are part of a single, unified view, such as detailing the internal
services of a microservice or the resources within a specific cloud provider account.

### Defining the Board: A Separate, Navigable Canvas

In contrast to a container, a **board** represents an entirely separate, top-level canvas. A single `.d2` file can
contain a composition of multiple boards, creating what is effectively a multi-page or multi-layered interactive
diagram. This feature is one of D2's most powerful capabilities for managing extreme complexity, allowing architects to
split vast systems into a series of individually simple, interconnected diagrams.

Boards are not defined using standard shape syntax but rather through three special reserved keywords: **`layers`**, *
*`scenarios`**, and **`steps`**. Each of these keywords introduces a block that contains a map of new board definitions.
The choice of keyword is critical as it determines the inheritance model of the new boards, which dictates how their
content and scope relate to their parent board.

```d2
# A root board with a single shape.
# This is the default, top-level board.
x -> y

# The 'layers' keyword introduces a new set of boards.
layers: {
  # 'board_one' is a new, separate canvas.
  board_one: {
    a -> b
  }

  # 'board_two' is another new, separate canvas.
  board_two: {
    1 -> 2
  }
}
```

The fundamental distinction of a board is that it begins as a separate canvas. For example, a board defined within the
`layers` block starts as a completely blank slate, representing a new level of abstraction where different objects are
depicted. Navigation between these distinct canvases is not implicit; it must be explicitly enabled through the use of
the `link` attribute, which makes a shape in one board a clickable hyperlink to another board.

The principal use case for boards is to deconstruct a complex system into manageable, hierarchical views. A high-level
architectural diagram can serve as the root board, with each major component being a clickable shape that links to
another board providing a detailed, low-level view of that component's internals. This approach, often referred to as "
drilling down," keeps each individual diagram clean and focused while preserving the interconnectedness of the overall
system.

### Key Distinction for Programmatic Generation

For an AI system tasked with generating D2 code, the distinction between containers and boards is the primary
architectural decision in composition. The choice hinges on the relationship between the elements being grouped and the
desired user experience.

- **Use a container** when the goal is to show a component as part of a larger whole on a single, static canvas. This is
  for visual organization and namespacing within one view. The relationship is one of containment.
- **Use a board** when the goal is to hide complexity behind a clickable element, revealing a new, detailed diagram upon
  interaction. This is for managing complexity across multiple views or levels of abstraction. The relationship is one
  of navigation.

The syntax reflects this distinction. Accessing a container's child is done via a static path in a connection (
`container.child`), while navigating to a board requires an interactive `link` attribute (`link: layers.board_name`).
The compiler and rendering tools, particularly interactive environments like D2 Studio or the `--watch` mode, are built
around this concept of navigable, multi-board diagrams. An AI must be programmed with this core principle to generate
diagrams that are not only syntactically correct but also structurally and conceptually sound, effectively leveraging
D2's most powerful compositional features.

## A Deep Dive into Board Types and Inheritance Models

The D2 language provides three distinct keywords for defining new boards—**`layers`**, **`scenarios`**, and **`steps`**.
The choice among these is not arbitrary; it is a critical design decision that dictates the **inheritance model** for
the newly created boards. Each keyword establishes a different relationship between a child board and its parent,
controlling whether shapes, connections, styles, and variables are carried over. For an AI generating diagrams,
selecting the correct board type is essential for producing views that accurately reflect the intended relationship,
whether it be a drill-down, an alternative state, or a sequential step.

### `layers`: Navigating Levels of Abstraction (No Inheritance)

The **`layers`** keyword is used to define boards that represent different levels of abstraction. Conceptually, each
board within a `layers` block is a completely independent, blank canvas. This type of board follows a **no-inheritance
model**. It does not inherit any shapes, connections, styles, or variables from its parent board. This is by design, as
each layer is intended to represent a different set of objects and relationships, corresponding to a different level of
detail.

The syntax involves defining a `layers` map, where each key is the name of a new layer board and its value is the D2
code defining that board's content.

```d2
# Root board (Layer 0 - Highest level of abstraction)
System_Overview: {
  label: "Global E-Commerce Platform"
  shape: cloud

  # This shape links to a board in the next layer, providing more detail.
  link: layers.regional_breakdown
}

# The 'layers' block defines the next level of abstraction.
layers: {
  # The 'regional_breakdown' board starts completely empty.
  # It does not inherit "System_Overview" or any of its styles.
  regional_breakdown: {
    direction: right

    NA_Region: North America
    EU_Region: Europe
    APAC_Region: Asia-Pacific

    NA_Region <-> EU_Region
    EU_Region <-> APAC_Region

    # A shape within this layer can link to a further nested layer.
    NA_Region: {
      link: layers.na_details
    }

    # Layers can be nested to create deeper levels of abstraction.
    layers: {
      na_details: {
        # This board is also a blank canvas, independent of 'regional_breakdown'.
        USA_Datacenter -> Canada_Datacenter
      }
    }
  }
}
```

The primary use case for `layers` is to create **"drill-down"** diagrams. The top-level board presents a simplified,
high-level overview of a system. Components on this board can then be made interactive, linking to separate layer boards
that reveal their internal complexity. This process can be nested indefinitely, allowing an architect to guide a viewer
from a 10,000-foot view down to the most granular details without overwhelming them with information on a single canvas.
The official D2 documentation provides a salient example of this, showing TikTok's data storage architecture, where each
click reveals a deeper, more specific layer of the infrastructure.

### `scenarios`: Illustrating Alternative Views (Base Layer Inheritance)

The **`scenarios`** keyword is used to define boards that represent alternative views or states of a single system.
Unlike `layers`, a board defined within a `scenarios` block follows a **base layer inheritance model**. This means it
inherits all objects, connections, styles, and variables from its parent (the base layer).

Once inherited, the scenario board can add new elements or, critically, reference existing elements from the base layer
to modify their properties. This allows for the creation of different "what-if" situations or state representations
without needing to redefine the entire diagram for each variation.

```d2
# Base Layer (Root board) - Represents the normal operational state.
direction: right

web_server: { style.fill: lightgreen }
app_server: { style.fill: lightgreen }
database: { shape: cylinder; style.fill: lightgreen }

web_server -> app_server
app_server -> database

# The 'scenarios' block defines alternative views of the base layer.
scenarios: {
  # The 'disaster_recovery_mode' board inherits all three shapes and both connections.
  disaster_recovery_mode: {
    # Modify existing objects inherited from the base layer.
    web_server.style.opacity: 0.3
    app_server.style.opacity: 0.3
    database.style.fill: orange

    # Add new objects and connections that only exist in this scenario.
    backup_db: {
      label: "Backup DB (Active)"
      shape: cylinder
      style.fill: lightgreen
    }
    app_server -> backup_db: Failover
    database -> backup_db: Replicating { style.stroke-dash: 2 }
  }
}
```

The quintessential use case for `scenarios` is to illustrate different states of the same set of components. The
official documentation demonstrates this by showing a "Normal deployment" diagram and then defining a "Hotfix
deployment" scenario that reuses the base components but modifies connections and styles to show a different workflow.
Other applications include visualizing system states like "Healthy," "Under Load," or "Failure Condition," where the
core architecture remains the same, but specific elements change color, new connections appear, or monitoring systems
become active.

### `steps`: Creating Sequential Narratives (Previous Step Inheritance)

The **`steps`** keyword is designed for creating sequential or animated diagrams. Boards defined within a `steps` block
follow a **previous step inheritance model**. Each board in the sequence inherits the complete state (all objects,
connections, styles) of the board that immediately precedes it in the definition order. This creates a cumulative or
evolutionary effect, where the diagram is built up progressively.

The primary application of `steps` is for export to animated formats, such as animated SVG. When rendered, each step
becomes a frame in the animation, providing a powerful way to visualize a process flow, a sequence of events, or the
gradual construction of a complex system.

```d2
# Step 1 (Implicitly the root board)
User: { shape: person }

steps: {
  # Step 2 inherits 'User' from Step 1.
  request_sent: {
    API_Gateway
    User -> API_Gateway: "1. Submit Request"
  }

  # Step 3 inherits everything from Step 2 ('User', 'API_Gateway', and the connection).
  authentication: {
    Auth_Service
    API_Gateway -> Auth_Service: "2. Validate Token"
  }

  # Step 4 inherits everything from Step 3.
  final_response: {
    Auth_Service -> User: "3. Success"
  }
}
```

When the above D2 code is compiled with an animation-aware exporter, it will produce a four-frame sequence:

1. **Frame 1**: Shows only the User.
2. **Frame 2**: Adds the API\_Gateway and the first connection.
3. **Frame 3**: Adds the Auth\_Service and the second connection.
4. **Frame 4**: Adds the final connection back to the User.

This allows for the creation of dynamic, explanatory narratives that are far more expressive than static diagrams for
illustrating time-ordered processes.

### The Defining Characteristic: Inheritance

The choice between **`layers`**, **`scenarios`**, and **`steps`** is fundamentally a decision about the desired *
*inheritance model**, which in turn dictates the scope and content of each generated board. An AI generating diagrams
must be equipped with a clear decision-making framework based on these models.

The logic can be summarized as follows:

- If the new view is a **"zoom-in"** to a new and distinct set of details, requiring a blank canvas, the AI should use *
  *`layers`**.
- If the new view is a **"different version"** of the current system, showing an alternative state of the same
  components, the AI should use **`scenarios`**.
- If the new view is the **"next stage"** in a sequence, building upon the previous state, the AI should use **`steps`
  **.

By internalizing this mapping of conceptual relationships to D2 keywords, a programmatic system can move beyond
generating simple, flat diagrams and begin to produce sophisticated, multi-board compositions that leverage the full
expressive power of the language.

## The Mechanics of Inter-Board Navigation: The `link` Attribute

The **`link`** attribute is the sole and essential mechanism in D2 for creating navigation between boards and to
external resources. It transforms a static shape into an interactive element. When a diagram containing links is
rendered as an SVG or viewed in an interactive environment like D2 Studio, these shapes become clickable hyperlinks. For
a programmatic system, mastering the syntax and behavior of the `link` attribute is critical for assembling a collection
of individual boards into a cohesive, navigable, and context-rich composition.

### Internal Linking: Connecting the Composition

Internal links are used to create navigational pathways between different boards within the same D2 file. This is the
feature that enables the "drill-down" and multi-view capabilities of D2 compositions.

The standard syntax for an internal link requires specifying the path to the target board, which is constructed as
`<board_type>.<board_name>`, where `<board_type>` is one of `layers`, `scenarios`, or `steps`.

```d2
# A shape 'api_overview' is defined on the root board.
# Its 'link' attribute points to the 'api_details' board within the 'layers' map.
api_overview: {
  label: "API Gateway (Click to see details)"
  link: layers.api_details
}

layers: {
  # This is the target board for the link.
  api_details: {
    direction: right
    rate_limiter -> authenticator -> router
  }
}
```

A common edge case arises when board names contain special characters, such as a dot (`.`), a space, or a hyphen. The D2
parser might misinterpret these characters. To ensure the board name is treated as a single, literal identifier, it *
*must be enclosed in double quotes** within the link path.

```d2
# A shape linking to a board with a complex name.
report_summary: {
  link: layers."Q1 2024 Performance Report"
}

layers: {
  # The board name must be quoted here as well to match the link.
  "Q1 2024 Performance Report": {
    label: "Q1 Performance was strong."
  }
}
```

### Hierarchical Linking: The Parent Reference (`_`)

D2 provides a powerful shorthand for navigating up the board hierarchy: the underscore (`_`) character. When used as a
value within a `link` attribute, the underscore acts as a reference to the **parent board**, not the parent container.
This allows for the creation of relative "back" or "up" links without needing to know the absolute name of the parent
board, making templates and reusable components more robust.

This reference can be chained. `_` refers to the immediate parent board, `_._` refers to the grandparent board, and so
on.

```d2
layers: {
  level1: {
    label: "Level 1: System"
    go_deeper: { link: layers.level2 }

    layers: {
      level2: {
        label: "Level 2: Subsystem"
        go_even_deeper: { link: layers.level3 }

        # This link navigates back to the 'level1' board.
        go_back_to_level1: { link: _ }

        layers: {
          level3: {
            label: "Level 3: Component"

            # This link navigates up two levels to the root board.
            go_to_root: { link: _._ }
          }
        }
      }
    }
  }
}
```

It is crucial to recognize the overloaded nature of the underscore (`_`) symbol. Its meaning is **context-dependent**.

- Inside a `link` attribute's value, `_` refers to the **parent board**.
- Outside a `link` attribute (e.g., in a connection path), `_` refers to the **parent container**.

An AI parser or generator must implement logic to correctly interpret this symbol based on its syntactic context. When
parsing or generating code, the system must first check if it is operating within the value of a `link` key. If so, `_`
resolves to the parent in the board hierarchy. Otherwise, it resolves to the parent in the container hierarchy. Failure
to distinguish this will lead to incorrect connections or broken navigation.

### External Linking: Connecting to the Web

The `link` attribute is also used to create standard hyperlinks to external URLs, connecting the diagram to web pages,
documentation, or other online resources. When rendered to SVG, the shape becomes a clickable `<a>` tag that opens the
specified URL, typically in a new browser tab.

While the official documentation does not provide a direct, simple code example for external links, it does provide a
critical clue in its discussion of interactive features. It warns that a URL fragment character (`#`) will be treated as
a comment if it is unquoted. This strongly implies that URLs should be enclosed in double quotes to be parsed correctly
and safely, especially when they contain special characters like `#`, `?`, `&`, or `=`. Therefore, the established best
practice is to **always quote external URLs**.

```d2
# A shape linking to the main D2 documentation website.
# Quoting is the safest practice even for simple URLs.
d2_docs: {
  label: "D2 Official Docs"
  link: "[https://d2lang.com/tour/intro](https://d2lang.com/tour/intro)"
}

# A shape linking to a specific section of a page.
# The '#' would create a comment if the URL were not quoted.
link_syntax_docs: {
  label: "Link Syntax Section"
  link: "[https://d2lang.com/tour/interactive#links](https://d2lang.com/tour/interactive#links)"
}

# A shape linking to a YouTube video with query parameters.
# The '?' and '&' would cause parsing errors if unquoted.
tutorial_video: {
  label: "Watch Tutorial"
  link: "[https://www.youtube.com/watch?v=example](https://www.youtube.com/watch?v=example)"
}
```

By correctly applying these three forms of the `link` attribute—internal, parent-relative, and external—a programmatic
system can construct diagrams that are not just static images but are rich, interactive, and deeply integrated with
their surrounding context, whether that context is other parts of the diagram or the wider web.

## Advanced Topics and Best Practices for Programmatic Generation

To elevate an AI's capability from generating simple diagrams to orchestrating complex, multi-board compositions, it
must master a set of advanced D2 features. These include managing scope and style propagation, modularizing code with
imports, leveraging the programmatic API for direct manipulation, and controlling the final render output. These topics
represent the bridge from basic syntax to sophisticated, production-quality diagram-as-code workflows.

### Scoping and Style Propagation Across Boards

Predictable and consistent visual styling is a hallmark of professional diagrams. In D2, the scoping of variables and
styles is intrinsically tied to the board's inheritance model, which must be understood to achieve this consistency.

The rules governing scope can be summarized as follows:

- **Intra-Board Scoping**: Within any single board, the scope is holistic. A variable or style defined anywhere within a
  board's block is accessible everywhere else in that same block. Notably, an object can reference a variable that is
  textually defined after it, a feature that simplifies declaration order.
- **Inter-Board Scoping**: The propagation of styles and variables between boards is determined by the compositional
  keyword used:
    - **`layers`**: Creates a new, hermetically sealed scope. Styles and variables from the parent board are **not**
      inherited. Each layer starts fresh.
    - **`scenarios`**: Inherits the parent's entire scope. All variables and styles from the base layer are available in
      the scenario and can be overridden or supplemented with new definitions.
    - **`steps`**: Inherits the scope of the immediately preceding step. This creates a cumulative scope where
      definitions from earlier steps are carried forward and can be built upon.

A robust and scalable workflow for managing styles across a large, multi-board diagram involves a combination of `vars`,
`imports`, and a clear understanding of these inheritance rules. Organizations often require a consistent visual
identity across all their diagrams. The most effective way to achieve this programmatically is to define a central style
guide file. For example, an AI could generate or maintain a `styles.d2` file containing all approved brand colors, font
sizes, and common shape styles as variables.

The AI's generation logic would then be as follows:

1. In the root board of the main diagram file, insert an `import` statement to load the central `styles.d2` file.
2. For any boards defined using `scenarios` or `steps`, the styles will be automatically inherited, ensuring
   consistency.
3. For any boards defined using `layers`, which do not inherit, the AI must be instructed to add the same `import`
   statement at the beginning of each layer's definition block to ensure they also receive the standard styling. This
   disciplined approach ensures that even in a complex, multi-layered composition, a consistent visual theme is
   maintained.

### Modularization with `imports`

The **`import`** keyword is D2's mechanism for code modularization. It allows one D2 file to include the contents of
another, promoting reusability, simplifying maintenance, and enabling collaborative, domain-driven design workflows.

The syntax is `import_name: @path/to/file.d2`, where `import_name` is a local alias for the imported file's contents.

For an AI-driven system, this feature is invaluable. The AI can be designed to manage a library of reusable diagram
components. These could include:

- A `c4-models.d2` file defining the standard C4 model shapes and styles.
- An `aws-icons.d2` file containing styled definitions for common AWS services.
- A `company-legend.d2` file that defines a standard diagram legend using the `d2-legend` variable.

When tasked with creating a new diagram, the AI's generation process would not create every element from scratch.
Instead, it would construct a root file that primarily consists of `import` statements for the required modules and then
defines the specific connections between the imported components. This approach aligns with the software engineering
principle of Don't Repeat Yourself (DRY) and makes the generated diagrams significantly more maintainable. A change to
the company's color palette, for example, would only require updating the central `styles.d2` file, and all diagrams
that import it would be updated automatically upon their next render.

### Programmatic Generation via the D2 Oracle API

For the most direct and powerful control over diagram creation, D2 provides a Go-language API known as **`d2oracle`**.
This API allows a program to build or modify a diagram's Abstract Syntax Tree (AST) directly in memory, bypassing the
need to write and parse raw D2 text files. This is the ideal interface for a sophisticated AI generation system.

The `d2oracle` functions for creating and modifying diagram elements (e.g., `Create`, `Set`, `Move`) are designed to be
multi-board aware. They achieve this through the `boardPath` parameter, which is the programmatic mechanism for
targeting a specific board within a composition.

The `boardPath` is a slice of strings (`[]string` in Go) that specifies the hierarchical path to the target board. For
instance, to target a board defined in D2 as `layers.virginia.databases`, the corresponding `boardPath` would be
`[]string{"layers", "virginia", "databases"}`. The root board is targeted by passing `nil` as the `boardPath`.

A conceptual Go code example illustrates how an AI would use this API:

```go
// This conceptual Go code demonstrates the use of d2oracle for multi-board manipulation.
package main

import (
    "strings"
    "[github.com/terrastruct/d2/d2compiler](https://github.com/terrastruct/d2/d2compiler)"
    "[github.com/terrastruct/d2/d2oracle](https://github.com/terrastruct/d2/d2oracle)"
)

func main() {
    // 1. Start with a D2 file that defines a multi-board structure.
    d2Script := `
        layers: {
            details: {
                // This board is initially empty.
            }
        }
    `
    g, _, _ := d2compiler.Compile("", strings.NewReader(d2Script), nil)

    // 2. Define the path to the target board where we want to add a shape.
    // This path corresponds to 'layers.details'.
    boardPath := []string{"layers", "details"}

    // 3. Use d2oracle.Create to add a new shape to the specified board.
    g, _, _ = d2oracle.Create(g, boardPath, "new_shape_on_details_board")

    // 4. Use d2oracle.Set to modify the style of the newly created shape on that same board.
    // The fourth parameter (tag) is nil for non-language-tagged values.
    // The fifth parameter (value) is the style value.
    g, _ = d2oracle.Set(g, boardPath, "new_shape_on_details_board.style.fill", nil, "blue")

    // The graph 'g' now contains the modified structure in its AST,
    // ready to be rendered or further manipulated.
}
```

The `d2oracle` API, with its `boardPath` addressing system, provides the lowest-level and most flexible interface for an
AI. It allows for precise, atomic modifications to any part of a complex, multi-board diagram directly at the AST level.

### Rendering and Exporting Multi-Board Diagrams

Once a `.d2` file containing a multi-board composition is generated, the D2 command-line interface (CLI) provides
essential flags to control how it is rendered.

The most important flag for compositions is **`--target`**. This flag allows the user to render a single, specific board
from a file that may contain dozens of them. This is highly efficient, as it avoids rendering the entire composition
when only one view is needed.

The syntax for the `--target` flag is path-based:

- Render only the root board: `d2 --target='' my_diagram.d2 out.svg`
- Render a specific nested board: `d2 --target='layers.details' my_diagram.d2 out.svg`
- Render a board and all of its children: By appending `.*` to the path, you can render a specific board along with all
  of its descendant boards (sub-layers, scenarios, etc.). This is useful for exporting a specific branch of a large
  hierarchy. `d2 --target='layers.details.*' my_diagram.d2 out.svg`

For development and debugging, the **`--watch`** (or **`-w`**) flag is indispensable. It starts a local web server that
live-reloads the rendered SVG whenever the source `.d2` file changes. Crucially, this watch mode fully supports
multi-board diagrams, correctly handling link navigation between boards in the browser, providing an interactive way to
test and validate a composition. An AI system could leverage this during a development phase to provide its human
operators with an interactive preview of the generated diagrams.

### Comprehensive Syntax Reference Tables

To facilitate programmatic generation and ensure syntactical correctness, the following tables provide a structured and
comprehensive summary of D2's advanced compositional features. These references are designed to be machine-readable and
serve as a definitive guide for an AI's internal knowledge base.

#### Table 5.1: Board Type Comparison Matrix

This matrix provides a direct mapping from the intended compositional behavior to the correct D2 keyword. It distills
the conceptual differences between `layers`, `scenarios`, and `steps` into a concise lookup table, enabling an AI to
make the appropriate syntactical choice based on functional requirements.

| Feature | `layers` | `scenarios` | `steps` |
| :--- | :--- | :--- | :--- |
| **Defining Keyword** | `layers` | `scenarios` | `steps` |
| **Inheritance Model** | None (Starts as a blank board) | Inherits from the single base layer | Inherits from the immediate previous step |
| **Primary Use Case** | Levels of abstraction, "drill-down" | Alternative views, "what-if" analysis | Sequential flows, animations |
| **Scope** | New, isolated scope | Inherited, modifiable scope | Cumulative, inherited scope |
| **Syntax Example** | `layers: { name: {...} }` | `scenarios: { name: {...} }` | `steps: { name: {...} }` |

#### Table 5.2: `link` Attribute Syntax Reference

This table provides a complete and unambiguous reference for all valid syntaxes of the `link` attribute. It explicitly
addresses the context-dependent behavior of the `_` symbol and documents the best-practice syntax for external URLs,
resolving potential ambiguities and preventing common parsing errors.

| Link Type | Description | Syntax Example |
| :--- | :--- | :--- |
| **Internal (Standard)** | Links to a board with a simple, alphanumeric name. | `link: layers.details` |
| **Internal (Complex Name)**| Links to a board whose name contains spaces, dots, or other special characters. The name must be quoted. | `link: scenarios."Failure Mode"` |
| **Parent Board (Single Level)**| Links to the immediate parent board in the nested board hierarchy. | `link: _` |
| **Parent Board (Multi-Level)**| Links multiple levels up the board hierarchy by chaining the parent reference. | `link: _._` (navigates 2 levels up) |
| **External URL** | Creates a hyperlink to an external website. The URL should be quoted to prevent misinterpretation of special characters (`#`, `?`, `&`). | `link: "https://d2lang.com"` |

#### Table 5.3: CLI Flags for Compositional Control

This table equips an AI system with the necessary command-line arguments to control the rendering and export of the
multi-board diagrams it generates. This completes the end-to-end programmatic workflow, from code generation to final
artifact production.

| Flag | Alias | Description | Syntax Example |
| :--- | :--- | :--- | :--- |
| `--target` | | Renders only the specified board from a multi-board file. An empty string targets the root. A `.*` suffix includes all children. | `d2 --target='layers.details' in.d2 out.svg` |
| `--watch` | `-w` | Starts a live-reload server that supports interactive multi-board navigation, ideal for development. | `d2 --watch my_diagram.d2` |
| `--layout` | `-l` | Specifies the layout engine to use (e.g., `dagre`, `elk`, `tala`). Different engines can produce visually distinct results. | `d2 --layout=elk my_diagram.d2` |
| `--theme` | `-t` | Applies a pre-defined theme ID to the diagram for consistent styling. | `d2 --theme=101 my_diagram.d2` |
| `--timeout` | | Sets the maximum execution time in seconds, which is crucial for preventing hangs when rendering very large or complex compositions. | `d2 --timeout=300 my_diagram.d2` |

### Conclusions

The D2 language's compositional features—specifically **`layers`**, **`scenarios`**, and **`steps`**—provide a powerful
and expressive framework for managing the complexity of modern system architecture diagrams. These are not mere grouping
mechanisms but are fundamental constructs that create distinct, navigable boards, each with a well-defined inheritance
model and scope.

- **The Core Architectural Choice**: The foundational distinction between a **container** (for hierarchical grouping on
  a single canvas) and a **board** (for creating a separate, navigable canvas) is the most critical concept for
  programmatic generation. An AI must be instructed to choose a container for representing composition within a single
  view and a board for representing navigation between different views or levels of abstraction.
- **Inheritance as the Defining Factor**: The selection among `layers`, `scenarios`, and `steps` is determined entirely
  by the desired inheritance behavior. `Layers` offer isolation for detailing different levels of abstraction.
  `Scenarios` offer inheritance from a base layer to show alternative states of the same system. `Steps` offer
  cumulative inheritance to build sequential narratives. This clear separation of concerns provides a logical decision
  tree for an AI to select the appropriate keyword.
- **The `link` Attribute as the Navigational Glue**: The `link` attribute is the exclusive mechanism for creating
  interactivity. Its syntax, while flexible, contains important nuances. The context-dependent behavior of the parent
  reference (`_`) and the necessity of quoting external URLs are critical rules that must be encoded into any generation
  system to ensure correctness and avoid parsing errors.
- **A Complete Programmatic Workflow**: A truly sophisticated AI-driven system should leverage the full D2 ecosystem.
  This involves managing a library of reusable components via `imports`, applying consistent branding with `vars` and
  `themes`, and, for maximum control, directly manipulating the diagram's Abstract Syntax Tree using the `d2oracle` Go
  API. The final output can then be precisely controlled using CLI flags like `--target`.

In conclusion, by providing an AI with a deep, structured understanding of these compositional primitives and their
associated syntax, it becomes possible to automate the creation of diagrams that are not only visually accurate but are
also interactive, maintainable, and capable of representing system complexity at multiple, interconnected levels. This
moves beyond simple text-to-image conversion and into the realm of true, model-driven, and interactive system
visualization.
