from json_logic import jsonLogic
from . import transform_js, JSError


def test_simple_equality():
    rule = transform_js("a == 1")
    result = jsonLogic(rule, {"a": 1})
    assert result is True


def test_boolean_literal__true():
    assert transform_js("true") is True


def test_boolean_literal__false():
    assert transform_js("false") is False


def test_string_literal():
    assert transform_js('"Hello, world!"') == "Hello, world!"


def test_template_literal():
    rule = transform_js("`Hello, ${name}!`")
    result = jsonLogic(rule, {"name": "Alice"})
    assert result == "Hello, Alice!"


def test_numeric_literal__integer():
    assert transform_js("42") == 42


def test_numeric_literal__float():
    assert transform_js("3.14") == 3.14


def test_numeric_literal__negative():
    assert transform_js("-10292.64") == -10292.64


def test_numeric_literal__binary():
    assert transform_js("0b01011010") == 0b01011010


def test_numeric_literal__hexadecimal():
    assert transform_js("0xFF00FF") == 0xFF00FF


def test_object_expression():
    assert transform_js('({"name": "Alice", "age": 30})') == {
        "name": "Alice",
        "age": 30,
    }


def test_array_expression():
    assert transform_js("[1, 2, 3]") == [1, 2, 3]


def test_array_expression_with_spread():
    rule = transform_js("[1, ...myArr, 4]")
    result = jsonLogic(rule, {"myArr": [2, 3]})
    assert result == [1, 2, 3, 4]


def test_null_literal():
    assert transform_js("null") is None


def test_identifier__simple():
    assert transform_js("a") == {"var": "a"}


def test_identifier__nested():
    assert transform_js("a.b.c") == {"var": "a.b.c"}


def test_comparison_expression__lt():
    assert transform_js("a < 10") == {"<": [{"var": "a"}, 10]}


def test_comparison_expression__lte():
    assert transform_js("a <= 10") == {"<=": [{"var": "a"}, 10]}


def test_comparison_expression__gt():
    assert transform_js("a > 10") == {">": [{"var": "a"}, 10]}


def test_comparison_expression__gte():
    assert transform_js("a >= 10") == {">=": [{"var": "a"}, 10]}


def test_comparison_expression__double_equal():
    assert transform_js("a == 10") == {"==": [{"var": "a"}, 10]}


def test_comparison_expression__not_double_equal():
    assert transform_js("a != 10") == {"!=": [{"var": "a"}, 10]}


def test_comparison_expression__triple_equal():
    assert transform_js("a === 10") == {"===": [{"var": "a"}, 10]}


def test_comparison_expression__not_triple_equal():
    assert transform_js("a !== 10") == {"!==": [{"var": "a"}, 10]}


def test_arithmetic__plus():
    assert transform_js("a + 10") == {"+": [{"var": "a"}, 10]}


def test_arithmetic__minus():
    assert transform_js("a - 10") == {"-": [{"var": "a"}, 10]}


def test_arithmetic__mult():
    assert transform_js("a * 10") == {"*": [{"var": "a"}, 10]}


def test_arithmetic__div():
    assert transform_js("a / 10") == {"/": [{"var": "a"}, 10]}


def test_arithmetic__mod():
    assert transform_js("a % 10") == {"%": [{"var": "a"}, 10]}


def test_call_expression():
    assert transform_js("max(a, b)") == {"max": [{"var": "a"}, {"var": "b"}]}


def test_unary_expression__negation():
    assert transform_js("!a") == {"!": [{"var": "a"}]}


def test_unary_expression__double_negation():
    assert transform_js("!!a") == {"!": [{"!": [{"var": "a"}]}]}


def test_unary_expression__minus():
    assert transform_js("-a") == {"-": [{"var": "a"}]}


def test_unary_expression__plus():
    assert transform_js("+a") == {"+": [{"var": "a"}]}


def test_ternary_expression():
    assert transform_js("a > 10 ? 'big' : 'small'") == {
        "if": [{">": [{"var": "a"}, 10]}, "big", "small"]
    }


def test_regex_literal():
    assert transform_js("/abc/i") == ["abc", "i"]


def test_if_statement():
    rule = transform_js(
        "if (a > 10) { 'big' } else if (a > 5) { 'medium' } else { 'small' }"
    )
    assert rule == {
        "if": [
            {">": [{"var": "a"}, 10]},
            "big",
            {"if": [{">": [{"var": "a"}, 5]}, "medium", "small"]},
        ]
    }


def test_call_expression_with_callback():
    rule = transform_js("map(arr, x => x * 2)")
    assert rule == {
        "map": [
            {"var": "arr"},
            {"*": [{"var": "x"}, 2]},
        ]
    }


def test_arrow_function():
    rule = transform_js("(a, b) => a + b")
    assert rule == {"+": [{"var": "a"}, {"var": "b"}]}


def test_logical__and():
    assert transform_js("a && b") == {"and": [{"var": "a"}, {"var": "b"}]}


def test_logical__or():
    assert transform_js("a || b") == {"or": [{"var": "a"}, {"var": "b"}]}


def test_complex__logical_expression():
    rule = transform_js("(a > 10 && b < 5) || c == 'hello'")
    assert rule == {
        "or": [
            {
                "and": [
                    {">": [{"var": "a"}, 10]},
                    {"<": [{"var": "b"}, 5]},
                ]
            },
            {"==": [{"var": "c"}, "hello"]},
        ]
    }
    assert jsonLogic(rule, {"a": 15, "b": 3, "c": "moon"}) is True


def test_invalid_syntax():
    try:
        transform_js("a +")
    except Exception as e:
        assert isinstance(e, JSError)
    else:
        assert False, "Expected a JSError to be raised"
