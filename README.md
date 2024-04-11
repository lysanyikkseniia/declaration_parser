# declaration_parser


# Grammar Definition

The grammar for declarations within Kotlin, specifying the syntax allowed for different types of declarations.

```ebnf
declaration ::= classDeclaration
              | objectDeclaration
              | functionDeclaration
              | propertyDeclaration
              | typeAlias
```

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

This creates a simple classifier type `c : S1, ..., Ss`.

## Simple Function Declaration

A simple function declaration consists of four main parts:

- **Name**: `f`
- **Parameter list**: `(p1 : P1[= v1],...,pn : Pn[= vn])`
- **Return type**: `R`
- **Body**: `b`

This has a function type `f : (p1 : P1,...,pn : Pn) → R`.
