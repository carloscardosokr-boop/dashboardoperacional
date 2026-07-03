from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template, request, redirect, flash
import plotly.express as px

app = Flask(__name__)
app.secret_key = "change-me-for-production"

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_PATH = DATA_DIR / "registro.json"
SIGLAS_PATH = DATA_DIR / "siglas.json"


def ensure_data_file() -> None:
    if not DATA_PATH.exists():
        DATA_PATH.write_text("[]", encoding="utf-8")


def ensure_siglas_file() -> None:
    if not SIGLAS_PATH.exists():
        SIGLAS_PATH.write_text("{}", encoding="utf-8")


def load_siglas() -> dict:
    ensure_siglas_file()
    try:
        with SIGLAS_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {key.upper(): value for key, value in data.items() if isinstance(value, dict)}


def get_sigla_info(sigla: str) -> dict | None:
    if not sigla:
        return None
    siglas = load_siglas()
    return siglas.get(sigla.strip().upper())


def parse_number(value, default=0.0):
    if value is None:
        return default

    text = str(value).strip()
    if not text:
        return default

    text = text.replace(" ", "")
    text = text.replace("R$", "").replace("r$", "").replace("$", "")
    if text.count(",") > 0 and text.count(".") > 0:
        text = text.replace(".", "").replace(",", ".")
    elif text.count(",") > 0:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return default


def parse_int(value, default=0):
    try:
        return int(parse_number(value, default))
    except (TypeError, ValueError):
        return default


def parse_float(value, default=0.0):
    return parse_number(value, default)


def format_brl(value, decimals=2):
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0

    formatted = f"{number:,.{decimals}f}"
    brasil = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {brasil}"


def format_number(value, decimals=2):
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0

    formatted = f"{number:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_int(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = 0
    formatted = f"{number:,}"
    return formatted.replace(",", ".")


TYPE_LABELS = {
    "cte": "CT-e",
    "frete": "Frete",
    "peso": "Peso",
    "mercadoria": "Mercadoria",
}


DEFAULT_METRIC = "frete"


def get_metric_value(registro: dict, metric: str) -> float:
    if metric == "cte":
        return parse_int(registro.get(metric, 0))
    return parse_float(registro.get(metric, 0.0))


def format_metric_text(value: float, metric: str) -> str:
    if metric in {"frete", "mercadoria"}:
        return format_brl(value)
    if metric == "peso":
        return format_number(value, 0)
    return format_int(value)


@app.template_filter("format_brl")
def format_brl_filter(value):
    return format_brl(value)


@app.template_filter("format_number")
def format_number_filter(value, decimals=2):
    return format_number(value, decimals)


@app.template_filter("format_int")
def format_int_filter(value):
    return format_int(value)


def load_registros() -> list[dict]:
    ensure_data_file()
    try:
        with DATA_PATH.open("r", encoding="utf-8") as handle:
            registros = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(registros, list):
        return []

    normalized = []
    for registro in registros:
        normalized.append({
            "id": parse_int(registro.get("id", 0)),
            "mes": str(registro.get("mes", "")) if registro.get("mes") is not None else "",
            "filial": str(registro.get("filial", "")) if registro.get("filial") is not None else "",
            "cte": parse_int(registro.get("cte", 0)),
            "peso": parse_float(registro.get("peso", 0.0)),
            "mercadoria": parse_float(registro.get("mercadoria", 0.0)),
            "frete": parse_float(registro.get("frete", 0.0)),
            "cidade": str(registro.get("cidade", "")) if registro.get("cidade") is not None else "",
            "uf": str(registro.get("uf", "")) if registro.get("uf") is not None else "",
            "tipo": str(registro.get("tipo", "FILIAL")) if registro.get("tipo") is not None else "FILIAL",
        })
    return normalized


def save_registros(registros: list[dict]) -> None:
    ensure_data_file()
    with DATA_PATH.open("w", encoding="utf-8") as handle:
        json.dump(registros, handle, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    registros = sorted(load_registros(), key=lambda item: item["id"], reverse=True)
    return render_template(
        "index.html",
        registros=registros,
    )


@app.route("/salvar", methods=["POST"])
def salvar():
    registros = load_registros()
    proximo_id = max((registro["id"] for registro in registros), default=0) + 1

    filial = request.form.get("filial", "").strip().upper()
    sigla_info = get_sigla_info(filial)
    if sigla_info is None:
        flash(f"Sigla '{filial}' não encontrada no banco de dados.", "danger")
        return render_template(
            "index.html",
            registros=registros,
            registro_edicao={
                "mes": request.form.get("mes", ""),
                "filial": filial,
                "cte": request.form.get("cte", ""),
                "peso": request.form.get("peso", ""),
                "mercadoria": request.form.get("mercadoria", ""),
                "frete": request.form.get("frete", ""),
                "cidade": "",
                "uf": "",
            },
        )

    registro = {
        "id": proximo_id,
        "mes": request.form.get("mes", "").strip(),
        "filial": filial,
        "cte": parse_int(request.form.get("cte")),
        "peso": parse_float(request.form.get("peso")),
        "mercadoria": parse_float(request.form.get("mercadoria")),
        "frete": parse_float(request.form.get("frete")),
        "cidade": sigla_info.get("cidade", ""),
        "uf": sigla_info.get("uf", ""),
        "tipo": sigla_info.get("tipo", "FILIAL"),
    }

    registros.append(registro)
    save_registros(registros)
    return redirect("/")


@app.route("/editar/<int:registro_id>")
def editar(registro_id):
    registros = sorted(load_registros(), key=lambda item: item["id"], reverse=True)
    registro_edicao = next((registro for registro in registros if registro["id"] == registro_id), None)
    if registro_edicao is None:
        return redirect("/")

    return render_template(
        "index.html",
        registros=registros,
        registro_edicao=registro_edicao,
    )


@app.route("/atualizar/<int:registro_id>", methods=["POST"])
def atualizar(registro_id):
    registros = load_registros()
    filial = request.form.get("filial", "").strip().upper()
    sigla_info = get_sigla_info(filial)
    if sigla_info is None:
        flash(f"Sigla '{filial}' não encontrada no banco de dados.", "danger")
        registro_edicao = {
            "id": registro_id,
            "mes": request.form.get("mes", ""),
            "filial": filial,
            "cte": request.form.get("cte", ""),
            "peso": request.form.get("peso", ""),
            "mercadoria": request.form.get("mercadoria", ""),
            "frete": request.form.get("frete", ""),
            "cidade": "",
            "uf": "",
        }
        return render_template(
            "index.html",
            registros=registros,
            registro_edicao=registro_edicao,
        )

    for registro in registros:
        if registro["id"] == registro_id:
            registro["mes"] = request.form.get("mes", "").strip()
            registro["filial"] = filial
            registro["cte"] = parse_int(request.form.get("cte"))
            registro["peso"] = parse_float(request.form.get("peso"))
            registro["mercadoria"] = parse_float(request.form.get("mercadoria"))
            registro["frete"] = parse_float(request.form.get("frete"))
            registro["cidade"] = sigla_info.get("cidade", "")
            registro["uf"] = sigla_info.get("uf", "")
            registro["tipo"] = sigla_info.get("tipo", "FILIAL")
            break

    save_registros(registros)
    return redirect("/")


@app.route("/excluir/<int:registro_id>")
def excluir(registro_id):
    registros = [registro for registro in load_registros() if registro["id"] != registro_id]
    save_registros(registros)
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    registros = load_registros()
    month_order = [
        "JANEIRO", "FEVEREIRO", "MARÇO", "MARCO", "ABRIL", "MAIO",
        "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO",
    ]
    meses_disponiveis = sorted(
        {registro["mes"] for registro in registros if registro["mes"]},
        key=lambda mes: month_order.index(mes) if mes in month_order else len(month_order),
    )
    tipos = [
        {"value": key, "label": label}
        for key, label in TYPE_LABELS.items()
    ]

    meses_selecionados = request.args.getlist("mes")
    tipo_selecionado = request.args.get("tipo", DEFAULT_METRIC)

    if not meses_selecionados or "todos" in meses_selecionados:
        meses_selecionados = meses_disponiveis

    registros = [registro for registro in registros if registro["mes"] in meses_selecionados]

    total_cte = sum(registro["cte"] for registro in registros)
    total_frete = sum(registro["frete"] for registro in registros)
    total_peso = sum(registro["peso"] for registro in registros)
    total_mercadoria = sum(registro["mercadoria"] for registro in registros)

    plot_records = []
    for registro in registros:
        valor = get_metric_value(registro, tipo_selecionado)
        plot_records.append({
            "filial": registro["filial"],
            "mes": registro["mes"],
            "valor": valor,
            "cte": registro["cte"],
            "peso": registro["peso"],
            "mercadoria": registro["mercadoria"],
            "frete": registro["frete"],
            "cte_text": format_int(registro["cte"]),
            "peso_text": format_number(registro["peso"], 0),
            "mercadoria_text": format_brl(registro["mercadoria"]),
            "frete_text": format_brl(registro["frete"]),
        })

    text_values = [format_metric_text(item["valor"], tipo_selecionado) for item in plot_records]

    grafico = ""
    if plot_records:
        selected_months_label = ", ".join(meses_selecionados)
        fig = px.bar(
            data_frame=plot_records,
            x="filial",
            y="valor",
            color="mes",
            barmode="group",
            template="plotly_white",
            title=f"{TYPE_LABELS.get(tipo_selecionado, 'Valor')} por Filial — {selected_months_label}",
            labels={"filial": "Filial", "valor": TYPE_LABELS.get(tipo_selecionado, "Valor"), "mes": "Mês"},
            hover_data=[],
        )
        fig.update_traces(
            text=text_values,
            textposition="outside",
            texttemplate="%{text}",
            cliponaxis=False,
            marker_line_width=1,
            textfont_size=10,
            customdata=[
                [
                    item["mes"],
                    item["cte_text"],
                    item["peso_text"],
                    item["mercadoria_text"],
                    item["frete_text"],
                ]
                for item in plot_records
            ],
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Mês: %{customdata[0]}<br>"
                "CT-e: %{customdata[1]}<br>"
                "Peso: %{customdata[2]} kg<br>"
                "Mercadoria: %{customdata[3]}<br>"
                "Frete: %{customdata[4]}<extra></extra>"
            ),
        )

        fig.update_layout(
            bargap=0.22,
            bargroupgap=0.12,
            margin={"l": 40, "r": 20, "t": 70, "b": 110},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            uniformtext_minsize=8,
            uniformtext_mode="hide",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Arial", size=11),
        )
        fig.update_xaxes(tickangle=0, automargin=True, showgrid=False)
        fig.update_yaxes(gridcolor="#f0f0f0", zerolinecolor="#d6d6d6")
        grafico = fig.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        grafico=grafico,
        total_cte=total_cte,
        total_frete=total_frete,
        total_peso=total_peso,
        total_mercadoria=total_mercadoria,
        meses_disponiveis=meses_disponiveis,
        meses_selecionados=meses_selecionados,
        tipo_selecionado=tipo_selecionado,
        tipos=tipos,
        tipo_label=TYPE_LABELS.get(tipo_selecionado, "Valor"),
        registros=registros,
    )


if __name__ == "__main__":
    app.run(debug=True)