# js-to-json-logic

This is a Python library that parses a JavaScript expression and
converts it into a JsonLogic-compatible object.

This is useful for cases where you want to allow users to input
logical expressions in a familiar syntax, but you want to evaluate
them using JsonLogic.

This library is inspired by the JavaScript library
[js-to-json-logic](https://github.com/krismuniz/js-to-json-logic).

## Usage

```python
from json_logic import jsonLogic
from js_to_json_logic import transform_js

rule = transform_js("a > 5 && b < 10")
result = jsonLogic(rule, {"a": 6, "b": 8})

print(result)  # True
```

## Supported JavaScript Syntax

| Type                    | Example                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| Literals                | `42`, `"hello"`, `true`, `false`, `null`                                |
| Identifiers             | `a`, `b`, `myObject.property`                                           |
| Template literals       | `` `Hello, ${name}!` ``                                                 |
| Arrays                  | `[1, 2, 3]`, `[1, 2, ...rest]`                                          |
| Unary operations        | `!a`, `!!b`, `-x`, `+x`                                                 |
| Conditionals            | `a > 5`, `b < 10`, `c >= 15`                                            |
| Arithmetic              | `a + b`, `a - b`, `a * b`, `a / b`, `a % b`                             |
| Equality and inequality | `a == 5`, `b !== 10`, `c === 15`, `d !== 20`                            |
| Logical expressions     | `a && b`, `a \|\| b`                                                    |
| If statements           | `if (a > 10) { "large" } else if (a > 5) { "medium" } else { "small" }` |
| Ternaries               | `a > 5 ? "yes" : "no"`                                                  |
| Call expressions        | `myFunction(a, b)`                                                      |
| Regex literals          | `/^abc$/gi`                                                             |
| Arrow functions         | `x => x > 5`                                                            |

## License

This project is licensed under the terms of the MIT license.
