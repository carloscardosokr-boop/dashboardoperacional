#!/usr/bin/env python3
"""
Renderiza templates Jinja2 para HTML estático.

Exemplos:
  python render_templates.py templates/registro.html --output output/registro.html --context data/registros.json
  python render_templates.py --all --outdir output --context data/registros.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_context(path: str | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"Context file not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def build_env() -> Environment:
    search_paths = [str(Path.cwd()), str(Path.cwd() / "templates"), str(Path.cwd() / "ui")]
    return Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=select_autoescape(["html", "xml"]),
    )


def render_template(env: Environment, template_path: Path, context: Dict[str, Any], out_path: Path) -> None:
    template_name = template_path.name
    tmpl = env.get_template(template_name)
    html = tmpl.render(**context)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print("Gerado:", out_path)


def find_templates(dir: Path) -> list[Path]:
    if not dir.exists():
        return []
    return [p for p in dir.rglob("*.html") if p.is_file()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Jinja2 templates to static HTML")
    parser.add_argument("template", nargs="?", help="Template file to render (arquivo .html). If omitted use --all")
    parser.add_argument("--all", action="store_true", help="Render all templates in ./templates or ./ui")
    parser.add_argument("--context", help="JSON file with context to pass to the template (ex.: data/registros.json)")
    parser.add_argument("--outdir", default="output", help="Output directory")
    parser.add_argument("--output", help="Output file path (when rendering a single template)")
    args = parser.parse_args()

    env = build_env()
    context = load_context(args.context) if args.context else {}

    outdir = Path(args.outdir)

    if args.all:
        templates = find_templates(Path("templates")) or find_templates(Path("ui")) or find_templates(Path.cwd())
        if not templates:
            print("Nenhum template encontrado em ./templates, ./ui ou no diretório atual.")
            raise SystemExit(1)
        for t in templates:
            out_path = outdir / t.name
            render_template(env, t, context, out_path)
        return

    if not args.template:
        parser.print_help()
        raise SystemExit(1)

    tpl = Path(args.template)
    if not tpl.exists():
        # try to find by name in the template search paths
        candidates = [Path("templates") / tpl.name, Path("ui") / tpl.name, Path(tpl.name)]
        found = next((c for c in candidates if c.exists()), None)
        if not found:
            raise SystemExit(f"Template não encontrado: {tpl}")
        tpl = found

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = outdir / tpl.name

    render_template(env, tpl, context, out_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # pragma: no cover - runner
        print("Erro:", e)
        sys.exit(1)
