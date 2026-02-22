from esprima import parseScript


def _convert_operator(op):
    match op:
        case "&&":
            return "and"
        case "||":
            return "or"
        case _:
            return op


def _array_has_spread_element(array_node):
    for element in array_node.elements:
        if element.type == "SpreadElement":
            return True
    return False


def _parse_node(node, parent=None):
    match node.type:
        case "ExpressionStatement":
            return _parse_node(node.expression)
        case "BlockStatement":
            if len(node.body) == 1:
                return _parse_node(node.body[0])
            else:
                return [_parse_node(stmt) for stmt in node.body]
        case "IfStatement":
            test = _parse_node(node.test)
            consequent = _parse_node(node.consequent)
            alternate = _parse_node(node.alternate) if node.alternate else None
            if alternate is not None:
                return {"if": [test, consequent, alternate]}
            else:
                return {"if": [test, consequent]}
        case "BinaryExpression" | "LogicalExpression":
            new_node = {}
            op = _convert_operator(node.operator)
            new_node[op] = [_parse_node(node.left), _parse_node(node.right)]
            return new_node
        case "MemberExpression":
            object_node = _parse_node(node.object, parent=node)
            property_node = _parse_node(node.property, parent=node)
            val = f"{object_node}.{property_node}"
            return val if parent is not None else {"var": val}
        case "CallExpression":
            callee = _parse_node(node.callee, parent=node)
            args = [_parse_node(arg) for arg in node.arguments]
            new_node = {}
            new_node[callee] = args
            return new_node
        case "ArrayExpression":
            if _array_has_spread_element(node):
                new_node = {"merge": []}
                for element in node.elements:
                    if element.type == "SpreadElement":
                        new_node["merge"].append(_parse_node(element.argument))
                    else:
                        new_node["merge"].append(_parse_node(element))
                return new_node
            else:
                return [_parse_node(element) for element in node.elements]
        case "ObjectExpression":
            new_node = {}
            for prop in node.properties:
                key = prop.key.name if prop.key.type == "Identifier" else prop.key.value
                value = _parse_node(prop.value)
                new_node[key] = value
            return new_node
        case "UnaryExpression":
            if (
                node.operator == "-"
                and node.argument.type == "Literal"
                and isinstance(node.argument.value, (int, float))
            ):
                return -node.argument.value
            else:
                op = _convert_operator(node.operator)
                argument = _parse_node(node.argument)
                return {op: [argument]}
        case "ConditionalExpression":
            test = _parse_node(node.test)
            consequent = _parse_node(node.consequent)
            alternate = _parse_node(node.alternate)
            return {"if": [test, consequent, alternate]}
        case "ArrowFunctionExpression":
            return _parse_node(node.body)
        case "TemplateLiteral":
            parts = []
            for i, quasi in enumerate(node.quasis):
                if quasi.tail is True and quasi.value.cooked == "":
                    continue
                parts.append(quasi.value.cooked)
                if i < len(node.expressions):
                    parts.append(_parse_node(node.expressions[i]))
            return {"cat": parts}
        case "Identifier":
            name = node.name
            return name if parent is not None else {"var": name}
        case "Literal":
            if node.regex is not None:
                return [node.regex.pattern, node.regex.flags]
            return node.value
        case _:
            raise NotImplementedError(f"Unsupported node type: {node.type}")


class JSError(Exception):
    pass


def transform_js(js: str):
    """Transforms a JavaScript expression into a JsonLogic rule object."""
    try:
        ast = parseScript(js)
    except Exception as e:
        raise JSError(f"{e}")
    if len(ast.body) != 1:
        raise JSError("expected exactly one expression")

    starting_node = ast.body[0]
    return _parse_node(starting_node)
