# Declaration Parser for Kotlin Language

## Overview
This is a CLI tool implemented in Python for parsing declarations in Kotlin files. Parser assumes file to be correctly formatted and do not include errors.

The parser recognizes and categorizes declarations of classes, functions, type aliases and objects. Functions within classes and objects, as well as top-level functions are correctly identified with their names, parameters, and return types. There is support for syntactically nested declarations within functions.

Parser is consistent to grammar for declarations within Kotlin according to [specification](https://kotlinlang.org/spec/syntax-and-grammar.html#grammar-rule-declaration) supporting `classDeclaration`, `objectDeclaration`, `functionDeclaration`, `propertyDeclaration`, `typeAlias`.

## Usage
To use the Declaration Parser, include it as a part of your project and direct it to parse individual Kotlin files. The parser will output a structured representation of all declarations found within the file, categorized by type. This output can then be utilized for further processing or analysis.

### Example

When running the following command the script will process the Kotlin file data/example1.kt and save the output to a JSON file named output1.json.

```bash
python main.py data/example1.kt output.json
```

For the following Kotlin file:

```Kotlin
fun fizzBuzz(n: Int) {
    fun getFizzBuzzString(number: Int): String {
        return when {
            number % 3 == 0 && number % 5 == 0 -> "FizzBuzz"
            number % 3 == 0 -> "Fizz"
            number % 5 == 0 -> "Buzz"
            else -> number.toString()
        }
    }

    for (i in 1..n) {
        println(getFizzBuzzString(i))
    }
}
```

The parsed output is as follows:

```json
{"declarations": [{"type": "function", "name": "fizzBuzz", "parameters": [{"name": "n", "type": "Int"}], "returnType": "Unit", "body": "fun fizzBuzz(n: Int) { fun getFizzBuzzString(number: Int): String { return when { number % 3 == 0 && number % 5 == 0 -> \"FizzBuzz\" number % 3 == 0 -> \"Fizz\" number % 5 == 0 -> \"Buzz\" else -> number.toString() } } for (i in 1..n) { println(getFizzBuzzString(i)) } }", "declarations": [{"type": "function", "name": "getFizzBuzzString", "parameters": [{"name": "number", "type": "Int"}], "returnType": "String", "body": "fun getFizzBuzzString(number: Int): String { return when { number % 3 == 0 && number % 5 == 0 -> \"FizzBuzz\" number % 3 == 0 -> \"Fizz\" number % 5 == 0 -> \"Buzz\" else -> number.toString() }}"}]}]}
```

## Potential improvements

1. Support for nesting in objects and classes.
2. Support for modifiers of functions.

