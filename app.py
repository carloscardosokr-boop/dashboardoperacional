from __future__ import annotations

from pathlib import Path
from flask import Flask, send_from_directory, render_template, abort

app = Flask(__name__, template_folder="templates", static_folder="output")


@app.route("/")
def index():
    # Prefer a generated static index in output, fallback to a template named index.html
    out_index = Path(app.static_folder) / "index.html"
    if out_index.exists():
        return send_from_directory(app.static_folder, "index.html")
    try:
        return render_template("index.html")
    except Exception:
        # Try to serve any file named cybermap_sao_paulo.html if present
        fallback = Path(app.static_folder) / "cybermap_sao_paulo.html"
        if fallback.exists():
            return send_from_directory(app.static_folder, "cybermap_sao_paulo.html")
        abort(404)


@app.route("/out/<path:filename>")
def output_file(filename: str):
    return send_from_directory(app.static_folder, filename)


@app.route("/tmpl/<path:tpl>")
def render_tpl(tpl: str):
    # Render a template from the templates folder (use carefully)
    try:
        return render_template(tpl)
    except Exception:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
