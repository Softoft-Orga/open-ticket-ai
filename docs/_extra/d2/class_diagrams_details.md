A Technical Specification for Generating UML Class Diagrams in D26.2 shape: class — A Definitive Guide to UML Class
DiagramsThis section provides a comprehensive specification for generating Unified Modeling Language (UML) Class
Diagrams using the D2 declarative language. It is designed to serve as a canonical reference, particularly for
programmatic generation systems. The analysis moves from the foundational syntax of the class shape to the systematic
composition of complex semantic relationships, establishing definitive D2 patterns for standard UML concepts.The core
principle for modeling UML in D2 is the use of the specialized shape: class primitive.1 Assigning this shape to a
container acts as a directive that activates a domain-specific "mini-DSL" parser. This parser interprets the contents of
the container block according to the specific rules of UML class members, which are distinct from the standard D2 object
and connection syntax. Mastery of this specialized shape and its associated compositional patterns is essential for
creating accurate and semantically rich object-oriented models.6.2.1 Core Class Definition: Syntax and Parsing RulesThe
definition of a class structure—its attributes, operations, and their visibility—is the fundamental building block of
any class diagram. D2 provides a precise and consistent syntax for these elements.Fundamental DeclarationThe process
begins by declaring a D2 object (a container) and assigning it the shape: class attribute. This declaration is the entry
point that instructs the D2 compiler to use the specialized UML class parser for the contents within the object's curly
braces {}.2Syntax:Code snippet# Declares a UML class named 'UserRepository'
UserRepository: {
shape: class

# Members are defined here

}
Member Definition Parsing LogicWithin a shape: class block, the parser uses a simple yet absolute rule to differentiate
between attributes (fields) and operations (methods). This distinction is the single most important parsing logic to
internalize for correct member generation. The determining factor is the presence of parentheses () in a member's
key.2Attributes (Fields): A key defined without parentheses is parsed as an attribute. The canonical syntax is
attributeName: Type. The Type portion is treated by the parser as an uninterpreted string literal. This provides the
flexibility to define simple types (int), complex generic types, or fully-qualified type names ("string", io.RuneReader)
.2Syntax:Code snippet# An attribute 'id' of type 'int'
id: int

# An attribute 'items' of a complex string array type

items: "string"
Operations (Methods): A key that includes parentheses is parsed as an operation. The canonical syntax is operationName(
parameters): returnType. As with attributes, the parameters and returnType are uninterpreted string literals, allowing
for any signature complexity. If the colon and return type are omitted, the operation's return type is implicitly
considered void.2Syntax:Code snippet# An operation 'findById' with one parameter, returning a 'User' type
findById(id: int): User

# An operation 'save' with no explicit return type (void)

save(user: User)
Visibility PrefixesD2 uses standard UML prefixes to denote the visibility of class members. These prefixes are placed at
the beginning of the member's key.4 The supported visibilities are:+ (public): The member is accessible from any other
class.- (private): The member is accessible only from within the class itself.# (protected): The member is accessible
from within the class and by its subclasses.(none): If no prefix is provided, the visibility defaults to public.Code
Example:Code snippetD2Parser: {
shape: class

# Public visibility (explicit and default)

+reader: io.RuneReader
readerPos: d2ast.Position

# Private visibility

-lookahead: "rune"

# Protected visibility (see note below)

\#lookaheadPos: d2ast.Position
}
A critical instruction for programmatic generation involves the protected visibility marker. The D2 language parser
processes the entire script for comments, which are denoted by the hash symbol (#), before any specialized shape parsers
are invoked.1 An unescaped # at the beginning of a member definition would cause the parser to interpret the entire line
as a comment, discarding it before it ever reaches the shape: class parser. To prevent this, the hash symbol for
protected members must be escaped with a backslash (\). This ensures the literal # character is passed as part of the
key to the class parser, which then correctly interprets it as the protected visibility marker. This is a crucial,
non-obvious exception that must be handled to prevent syntax errors.26.2.2 Modeling UML Relationships: The Compositional
MethodA core design aspect of D2 is that it does not provide high-level, single-keyword abstractions for each type of
UML relationship (e.g., a hypothetical relationship: inheritance keyword). Instead, D2 requires the diagram author to
compose these complex semantic concepts from a small set of orthogonal, low-level primitives. The primary primitives
used are:Connection Operators: The fundamental line type, either undirected (--) or directed (->, <-, <->).Arrowhead
Shapes: The geometric shape of the connection's endpoint, defined via source-arrowhead and target-arrowhead.Connection
Styles: Visual modifiers like line style (stroke-dash) and fill (filled).A generating system's task is not to find a
one-to-one mapping for a UML relationship, but to learn the correct "recipe" of D2 primitives for each relationship
type.The following table and subsections define the canonical D2 recipes for all standard UML class relationships.UML
RelationshipSemantic MeaningD2 Connectiontarget-arrowhead.shapeRequired StylesAssociationA structural link between
peers.Source -> Targettriangle (default)style.filled: true (default)DependencyA "using" relationship; changes to the
supplier may affect the client.Client -> Supplierarrow or trianglestyle.stroke-dash: 4GeneralizationAn "is-a"
relationship (inheritance).Subclass -> Superclasstrianglestyle.filled: falseRealizationAn "implements" relationship (
interface).Class -> Interfacetrianglestyle.stroke-dash: 4, style.filled: falseAggregationA "has-a" relationship where
the part can exist independently.Part -> Wholediamondstyle.filled: falseCompositionA strong "has-a" relationship where
the part cannot exist independently.Part -> Wholediamondstyle.filled: trueAssociationAssociation is the most general
structural relationship between classes. It is represented by a solid line. A directed arrow (->) should be used to
imply navigability from the source class to the target class.4D2 Recipe:Code snippet# An association where Customer can
navigate to Order
Customer -> Order: places
DependencyA dependency indicates that one element (the client) depends on another (the supplier). In UML, this is
conventionally shown as a dashed line with a standard open arrowhead.4D2 Recipe: A directed connection (->) is styled
with stroke-dash. A value of 4 is a common choice for a visible dash pattern.Code snippetReportGenerator -> PDFLibrary:
uses {
style: {
stroke-dash: 4
}
}
Generalization (Inheritance)Generalization represents an "is-a" relationship, commonly known as inheritance. The UML
standard notation is a solid line with a large, hollow (unfilled) triangle arrowhead that points from the subclass (the
child) to the superclass (the parent).4 While some D2 examples may show simpler representations, the addition of the "
unfilled triangle arrowhead" in version 0.6.2 established the capability for a semantically correct visualization.8 This
recipe should be considered the canonical and correct form.D2 Recipe:Code snippet# SavingsAccount "is-a" Account
SavingAccount -> Account: {
target-arrowhead: {
shape: triangle
style.filled: false
}
}
Realization (Interface Implementation)Realization signifies that a classifier (the client) implements the contract
specified by an interface (the supplier). The UML standard is a dashed line with a large, hollow triangle arrowhead,
pointing from the implementing class to the interface.9 This D2 recipe is a logical synthesis of the established
patterns for Dependency (dashed line) and Generalization (hollow triangle arrowhead), as no single document explicitly
provides this pattern.D2 Recipe:Code snippet# S3Uploader "implements" IFileUploader
S3Uploader -> IFileUploader: {
style: {
stroke-dash: 4
}
target-arrowhead: {
shape: triangle
style.filled: false
}
}
AggregationAggregation is a "has-a" or "part-of" relationship where the part can exist independently of the whole. The
UML standard is a solid line with a hollow (unfilled) diamond at the end connected to the "whole" class (the aggregate)
.4D2 Recipe:Code snippet# A Department "has-a" Teacher, but a Teacher can exist without a Department
Teacher -> Department: {
target-arrowhead: {
shape: diamond
style.filled: false
}
}
CompositionComposition is a strong form of aggregation where the part cannot exist independently of the whole; its
lifecycle is tied to the whole. The UML standard is a solid line with a filled diamond at the end connected to the "
whole" class (the composite).4 D2 elegantly models this distinction from aggregation by simply toggling a boolean style
property.D2 Recipe:Code snippet# An Order "has" OrderLines, which cannot exist without the Order
OrderLine -> Order: {
target-arrowhead: {
shape: diamond
style.filled: true
}
}
6.2.3 Advanced Relationship Annotations: Multiplicity and Role NamesD2 employs a highly idiomatic and non-obvious
pattern for annotating the ends of a connection. Instead of providing structured attributes like multiplicity="1..*" or
role="client", it leverages the fact that source-arrowhead and target-arrowhead are themselves objects that can have
labels. The multiplicity and role names are assigned as simple string values to these implicit label
properties.MultiplicityThe cardinality of a relationship (e.g., 1, 0..*, 1..*) is defined by assigning the multiplicity
string directly as the value for the source-arrowhead or target-arrowhead key. This acts as a powerful shorthand for
setting the label of the arrowhead object.2 The multiplicity notations themselves are uninterpreted strings.D2 Syntax:
Code snippet# A Customer can have 0 or more Orders.

# An Order belongs to exactly 1 Customer.

Customer -> Order: places {
source-arrowhead: "1"
target-arrowhead: "0..*"
}
This shorthand syntax (source-arrowhead: "1") is the idiomatic form found in documentation and is equivalent to the more
verbose source-arrowhead: { label: "1" }. Programmatic generators should prefer the shorthand for conciseness.Role Names
and Association LabelsA clear distinction must be made between the different labels on a connection:Association Name:
This is the primary label on the connection itself, defined after the colon (e.g., Customer -> Order: places). It names
the relationship.Role Names: These are labels applied specifically to the arrowheads to clarify the role played by the
class at that end of the association.While not explicitly documented, the most robust way to specify a role name is to
use the more verbose .label syntax on the arrowhead object. For cases requiring both multiplicity and a role name, they
can be combined into a single string.D2 Syntax Example:Code snippet# An Order is composed of 1 or more OrderItems (the '
items' role)
OrderItem -> Order: {
source-arrowhead: "1..* items"
target-arrowhead: "1"
#... composition arrowhead shape
}
6.2.4 Advanced Class Annotations: Modifiers and StereotypesD2 provides no first-class language support for UML concepts
like stereotypes or abstract/static modifiers. These are considered presentation-layer concerns. A generating system
must learn to represent these semantic concepts by adhering to established UML visual conventions and using D2's
general-purpose features like string formatting and styling.Stereotypes (<<interface>>, <<abstract>>)The standard UML
representation for a stereotype is the stereotype name enclosed in guillemets (<< >>).D2 Implementation: The stereotype
is prepended to the class's label string, often with a newline character (\n) for better visual separation. For an
abstract class, it is conventional to also style the class name in italics.Code snippet# An interface with a stereotype
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
Static and Abstract Member ModifiersIn UML, static members are conventionally underlined, and abstract members are
italicized.4 D2 provides the style properties style.underline: true and style.italic: true.14However, a significant
limitation exists: the D2 shape: class parser does not currently support applying styles to individual members within
the class block. All styling examples in the documentation apply to the entire shape container.14Therefore, a generating
AI must be explicitly instructed to avoid generating invalid code that attempts to style individual members. The correct
approach is to acknowledge this limitation and use textual documentation as a workaround.Instruction for Programmatic
Generation: To denote a static or abstract member, the semantic information cannot be directly visualized on a
per-member basis using underlining or italics. This information should be documented textually, either in an associated
Markdown block within the diagram or as a comment in the D2 source code.6.2.5 Synthesis: A Comprehensive Example and
Generation StrategyThis final section integrates all preceding concepts into a single, comprehensive example and
provides a set of high-level strategic rules for programmatic generation.Full Example: E-Commerce SystemThe following D2
script models a simple e-commerce system. It serves as a "golden" reference, demonstrating the correct, canonical
application of all concepts covered in this guide.Code snippet#

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
target-arrowhead: "1"
target-arrowhead.shape: diamond
target-arrowhead.style.filled: true
}

# Aggregation: An Order has a shipping Address.

# The Address can exist independently of the Order.

Address -> Order: has shipping address {
source-arrowhead: "1"
target-arrowhead: "1"
target-arrowhead.shape: diamond
target-arrowhead.style.filled: false
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
Strategic Recommendations for AI GenerationTo generate D2 code that is not just syntactically correct but also
idiomatic, readable, and maintainable, a programmatic system should adhere to the following high-level rules:Abstract
with vars and classes: For large or complex diagrams, use D2's abstraction mechanisms. Define common data types or
configuration in a vars block (e.g., vars: { id_type: string }) for reuse via substitution (${id_type}). Use the classes
block to define reusable attribute sets, which is ideal for creating styles for stereotypes. This promotes the Don't
Repeat Yourself (DRY) principle and enhances maintainability.16Code snippetclasses: {
interface: {
style.italic: true

# Other common interface styles

}
}
IPaymentGateway.class: interface
Structure for Readability: Generate D2 scripts in logical blocks. A recommended structure is to first define all shape:
class objects and their members, and then define all of the connection-based relationships between them. This separation
of concerns greatly enhances human readability and aligns with a model-view approach to documentation.Adhere to
Canonical Forms: The generating system must always produce the canonical relationship representations as defined in
the "UML Relationship to D2 Syntax Mapping" table in section 6.2.2. This ensures consistency and semantic accuracy
across all generated diagrams, even if simpler or alternative syntaxes might exist in older documentation.Handle Parser
Exceptions Proactively: The system must include a specific rule to handle the \# escaping requirement for protected
members. This is a common and non-obvious point of failure. The generation logic should automatically prepend a
backslash (\) to any member key that begins with a # to ensure it is parsed correctly.
