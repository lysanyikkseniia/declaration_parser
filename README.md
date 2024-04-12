# Declaration Parser for Kotlin language

Parser is consistent to grammar for declarations within Kotlin according to [specification](https://kotlinlang.org/spec/syntax-and-grammar.html#grammar-rule-declaration) and supports: `classDeclaration`, `objectDeclaration`, `functionDeclaration`, `propertyDeclaration`, `typeAlias`.

Parser assumes file to be correctly formatted according to the grammar.

There is support for syntactically nested declarations.

Body as in example (not conventional). 

# Class Declaration

Source: https://kotlinlang.org/spec/declarations.html#class-declaration

## Simple Class Declaration

A simple class declaration consists of the following parts:

- **Name**: `c`
- **Optional primary constructor declaration**: `ptor`
- **Optional supertype specifiers**: `S1, ..., Ss`
- **Optional body** `b`, which may include the following:
  - Secondary constructor declarations: `stor1,...,storc`
  - Instance initialization blocks: `init1, ..., initi`
  - Property declarations: `prop1, ..., propp`
  - Function declarations: `md1, ..., mdm`
  - Companion object declaration: `companionObj`
  - Nested classifier declarations: `nested`

### CFG for Class declaration in Kotlin

look for 'class'

- `classDeclaration:`
  - `[modifiers]`
  - `('class' | (['fun' {NL}] 'interface'))`
  - `{NL}`
  - `simpleIdentifier`
  - `[{NL} typeParameters]`
  - `[{NL} primaryConstructor]`
  - `[{NL} ':' {NL} delegationSpecifiers]`
  - `[{NL} typeConstraints]`
  - `[( {NL} classBody ) | ( {NL} enumClassBody )]`

# Object Declaration

look for 'object'

- `objectDeclaration:`
  - `[modifiers]`
  - `'object'`
  - `{NL}`
  - `simpleIdentifier`
  - `[{NL} ':' {NL} delegationSpecifiers]`
  - `[{NL} classBody]`

# Function Declaration

Source: https://kotlinlang.org/spec/declarations.html#function-declaration

### Simple example

A simple function declaration consists of four main parts:

- **Name**: `f`
- **Parameter list**: `(p1 : P1[= v1],...,pn : Pn[= vn])`
- **Return type**: `R`
- **Body**: `b`

### CFG for function declaration in Kotlin

**Function Declaration**

look for 'fun'

- `functionDeclaration:`
  - `[modifiers] 'fun'`
  - `[[NL] typeParameters]`
  - `[[NL] receiverType [NL] '.']`
  - `simpleIdentifier`
  - `functionValueParameters`
  - `[[NL] ':' [NL] type]`
  - `[[NL] typeConstraints]`
  - `[[NL] functionBody]`

**Function Body**

- `functionBody:`
  - `block`
  - `| ('=' [NL] expression)`


# Property Declaration

look for 'val' or 'var'

- `propertyDeclaration:`
  - `[modifiers]`
  - `('val' | 'var')`
  - `[{NL} typeParameters]`
  - `[{NL} receiverType {NL} '.']`
  - `({NL} (multiVariableDeclaration | variableDeclaration))`
  - `[{NL} typeConstraints]`
  - `[{NL} (('=' {NL} expression) | propertyDelegate)]`
  - `[{NL} ';']`
  - `{NL}`
  - `(([getter] [{NL} [semi] setter]) | ([setter] [{NL} [semi] getter]))`


# Type Alias

look for 'typealias'

- `typeAlias:`
  - `[modifiers]`
  - `'typealias'`
  - `{NL}`
  - `simpleIdentifier`
  - `[{NL} typeParameters]`
  - `{NL}`
  - `'='`
  - `{NL}`
  - `type`
