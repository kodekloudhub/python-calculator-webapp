"""
Simple Calculator web app with Azure App Configuration driving:
  - Dynamic configuration: 'Calculator:Title' (page heading), refreshed at runtime without redeploy.
  - Feature flag: 'AdvancedOperations' (enables the modulo and power operators).

The App Configuration connection string is read from AZURE_APPCONFIG_CONNECTION_STRING.
If it is not set (e.g. running locally without App Configuration), the app falls back to
sensible defaults so it still runs and the unit tests still pass.
"""
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ── Azure App Configuration (optional) ────────────────────────────────────────
_config = None
_feature_manager = None

def _init_app_configuration():
    """Load dynamic configuration and feature flags from Azure App Configuration."""
    global _config, _feature_manager
    conn = os.environ.get("AZURE_APPCONFIG_CONNECTION_STRING")
    if not conn:
        return
    try:
        from azure.appconfiguration.provider import load, WatchKey
        from featuremanagement import FeatureManager

        _config = load(
            connection_string=conn,
            feature_flag_enabled=True,
            refresh_on=[WatchKey("sentinel")],   # change 'sentinel' in App Config to push updates
            refresh_interval=10,
        )
        _feature_manager = FeatureManager(_config)
    except Exception as exc:  # pragma: no cover - depends on external service
        app.logger.warning("App Configuration unavailable, using defaults: %s", exc)


def get_title():
    if _config is not None:
        try:
            _config.refresh()
            return _config.get("Calculator:Title", "Simple Calculator")
        except Exception:  # pragma: no cover
            pass
    return os.environ.get("CALCULATOR_TITLE", "Simple Calculator")


def advanced_enabled():
    if _feature_manager is not None:
        try:
            return bool(_feature_manager.is_enabled("AdvancedOperations"))
        except Exception:  # pragma: no cover
            pass
    return os.environ.get("ADVANCED_OPERATIONS", "false").lower() == "true"


HTML = """
<!doctype html>
<html lang="en">
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 520px; margin: 40px auto; background: #f7f9fa; }
        h2 { color: #2A5676; }
        input, select { padding: 6px; margin-right: 4px; }
        button { padding: 6px 16px; }
        .error { color: #b10000; }
        .badge { font-size: 12px; color: #fff; background:#6a3df6; padding:2px 8px; border-radius:8px; }
    </style>
</head>
<body>
    <h2>{{ title }} {% if advanced %}<span class="badge">Advanced</span>{% endif %}</h2>
    <form method="post">
      <input name="a" type="number" step="any" required placeholder="First number">
      <select name="op">
        <option value="+">+</option>
        <option value="-">−</option>
        <option value="*">×</option>
        <option value="/">÷</option>
        {% if advanced %}
        <option value="%">mod</option>
        <option value="**">pow</option>
        {% endif %}
      </select>
      <input name="b" type="number" step="any" required placeholder="Second number">
      <button type="submit">Calculate</button>
    </form>
    {% if result is not none %}
      {% if error %}
        <p class="error">Error: <strong>{{ result }}</strong></p>
      {% else %}
        <p>Result: <strong>{{ result }}</strong></p>
      {% endif %}
    {% endif %}
</body>
</html>
"""


def calculate(a, b, op, advanced):
    valid = {"+", "-", "*", "/"}
    if advanced:
        valid |= {"%", "**"}
    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return "Inputs must be valid numbers", True
    if op not in valid:
        return "Unknown operation", True
    if op in ("/", "%") and b == 0:
        return "Division by zero is not allowed", True
    try:
        if op == "+":
            return str(a + b), False
        if op == "-":
            return str(a - b), False
        if op == "*":
            return str(a * b), False
        if op == "/":
            return str(a / b), False
        if op == "%":
            return str(a % b), False
        if op == "**":
            return str(a ** b), False
    except Exception:
        return "Internal calculation error", True
    return "Unhandled operation", True


@app.route("/", methods=["GET", "POST"])
def calc():
    result = None
    error = False
    advanced = advanced_enabled()
    if request.method == "POST":
        result, error = calculate(
            request.form.get("a"), request.form.get("b"), request.form.get("op"), advanced
        )
    return render_template_string(HTML, result=result, error=error, title=get_title(), advanced=advanced)


_init_app_configuration()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
