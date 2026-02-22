"""Check that basic features work; used during the release process."""

from js_to_json_logic import transform_js

rule = transform_js("a > 3 && b < 5")
if rule == {"and": [{">": [{"var": "a"}, 3]}, {"<": [{"var": "b"}, 5]}]}:
    print("Smoke test passed!")
else:
    raise RuntimeError("Smoke test failed: unexpected output")
