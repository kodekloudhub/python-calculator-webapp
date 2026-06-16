"""
Simple Calculator web app with optional Azure App Configuration.

When AZURE_APPCONFIG_CONNECTION_STRING points at an App Configuration store, the app reads:
  - Dynamic configuration: 'Calculator:Settings:Banner' -- a banner message shown above the
    calculator, refreshed at runtime (watched 'sentinel' key) without redeploying.
  - Feature flag: 'SalesWeekend' -- when enabled, shows a promotional banner; when disabled it
    disappears. Toggled in the App Configuration Feature Manager, no code change/redeploy.

Without App Configuration the app runs with safe defaults (no banners), so it works anywhere
and the unit/functional tests still pass.
"""
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ── Azure App Configuration (optional) ─────────────────────────────────────────
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
            feature_flag_refresh_enabled=True,     # refresh feature flags at runtime, not just at startup
            refresh_on=[WatchKey("sentinel")],     # change 'sentinel' in App Config to push config updates
            refresh_interval=10,
        )
        _feature_manager = FeatureManager(_config)
    except Exception as exc:  # pragma: no cover - depends on external service
        app.logger.warning("App Configuration unavailable, using defaults: %s", exc)


def get_banner():
    if _config is not None:
        try:
            _config.refresh()
            return _config.get("Calculator:Settings:Banner", "")
        except Exception:  # pragma: no cover
            pass
    return os.environ.get("CALCULATOR_BANNER", "")


def sales_weekend_enabled():
    if _feature_manager is not None:
        try:
            _config.refresh()   # pick up feature-flag changes at runtime (no-op within refresh_interval)
            return bool(_feature_manager.is_enabled("SalesWeekend"))
        except Exception:  # pragma: no cover
            pass
    return False


HTML = """
<!doctype html>
<html lang="en">
<head>
    <title>Simple Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 520px; margin: 40px auto; background: #f7f9fa; }
        h2 { color: #2A5676; }
        input, select { padding: 6px; margin-right: 4px; }
        button { padding: 6px 16px; }
        .error { color: #b10000; }
        .banner { padding:10px 14px; border-radius:8px; margin-bottom:16px; }
        .banner-info { background:#e7f0fb; color:#1c4e80; border:1px solid #b9d4f3; }
        .banner-sale { background:#fff2d8; color:#8a5a00; border:1px solid #f3d79b; font-weight:bold; }
    </style>
</head>
<body>
    <h2>Simple Calculator</h2>
    {% if banner %}<div class="banner banner-info">{{ banner }}</div>{% endif %}
    {% if sales %}<div class="banner banner-sale">ALL CALCULATIONS ARE FREE THIS WEEKEND!</div>{% endif %}
    <form method="post">
      <input name="a" type="number" step="any" required placeholder="First number">
      <select name="op">
        <option value="+">+</option>
        <option value="-">&minus;</option>
        <option value="*">&times;</option>
        <option value="/">&divide;</option>
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


def calculate(a, b, op):
    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return "Inputs must be valid numbers", True
    if op not in {"+", "-", "*", "/"}:
        return "Unknown operation", True
    if op == "/" and b == 0:
        return "Division by zero is not allowed", True
    if op == "+":
        return str(a + b), False
    if op == "-":
        return str(a - b), False
    if op == "*":
        return str(a * b), False
    return str(a / b), False


@app.route("/", methods=["GET", "POST"])
def calc():
    result = None
    error = False
    if request.method == "POST":
        result, error = calculate(
            request.form.get("a"), request.form.get("b"), request.form.get("op")
        )
    return render_template_string(
        HTML, result=result, error=error, banner=get_banner(), sales=sales_weekend_enabled()
    )


_init_app_configuration()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
