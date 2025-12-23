import os
from pathlib import Path
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import pandas as pd


BASE_DIR = Path(file).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "education_finance.csv"


def load_local_csv():
    """Загрузка CSV из data/, корректная работа в PyCharm и терминале."""
    print("Dashboard читает файл:", CSV_PATH)

    if not CSV_PATH.exists():
        print("ОШИБКА: CSV файл не найден!")
        return None

    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    # Приводим дату
    if "Дата" in df.columns:
        df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")

    if "Прибыль" not in df.columns:
        df["Прибыль"] = df["Доходы"] - df["Расходы"]
    else:
        df["Прибыль"] = pd.to_numeric(df["Прибыль"], errors="coerce").fillna(0)

    return df

app = Dash(name)

app.layout = html.Div([

    html.H1(
        "Финансовая аналитика продаж",
        style={"textAlign": "center", "color": "#2C3E50"}
    ),

    html.Div([
        html.Div(id="kpi-income", className="kpi-box"),
        html.Div(id="kpi-expense", className="kpi-box"),
        html.Div(id="kpi-profit", className="kpi-box"),
    ], style={"display": "flex", "justifyContent": "space-around"}),

    html.Br(),

    html.Div([
        html.Label("Выберите период анализа"),
        dcc.Dropdown(
            id="period-select",
            options=[
                {"label": "2024 год", "value": "2024"},
                {"label": "2025 год", "value": "2025"},
                {"label": "Все данные", "value": "all"},
            ],
            value="all",
            style={"width": "300px"}
        )
    ], style={"marginLeft": "30px"}),

    html.Br(),

    html.Div([
        dcc.Graph(id="line-chart"),
        dcc.Graph(id="pie-chart"),
        dcc.Graph(id="hist-chart"),
        dcc.Graph(id="scatter-chart"),
    ]),

    html.H2("Таблица финансовых показателей"),
    dash_table.DataTable(
        id="data-table",
        page_size=10,
        style_table={"width": "90%", "margin": "auto"},
        style_cell={"textAlign": "center"},
        style_header={
            "backgroundColor": "#3498DB",
            "fontWeight": "bold",
            "color": "white"
        }
    ),

    dcc.Interval(
        id="interval-component",
        interval=5 * 1000,
        n_intervals=0
    )
])

@app.callback(
    [
        Output("line-chart", "figure"),
        Output("pie-chart", "figure"),
        Output("hist-chart", "figure"),
        Output("scatter-chart", "figure"),
        Output("data-table", "data"),
        Output("data-table", "columns"),
        Output("kpi-income", "children"),
        Output("kpi-expense", "children"),
        Output("kpi-profit", "children"),
    ],
    [
        Input("period-select", "value"),
        Input("interval-component", "n_intervals")
    ]
)
def update_dashboard(period, _update_signal):

    df = load_local_csv()
    if df is None:
        return [{}] * 9

    if period != "all" and "Дата" in df.columns:
        df = df[df["Дата"].dt.year == int(period)]

    total_income = df["Доходы"].sum()
    total_expense = df["Расходы"].sum()
    total_profit = df["Прибыль"].sum()

    kpi_income = html.Div([
        html.H3("Доходы"),
        html.H1(f"{total_income:,} ₽")
    ], style={"background": "#2ECC71", "padding": "20px", "borderRadius": "10px", "color": "white"})

    kpi_expense = html.Div([
        html.H3("Расходы"),
        html.H1(f"{total_expense:,} ₽")
    ], style={"background": "#E74C3C", "padding": "20px", "borderRadius": "10px", "color": "white"})
    
    kpi_profit = html.Div([
        html.H3("Прибыль"),
        html.H1(f"{total_profit:,} ₽")
    ], style={"background": "#3498DB", "padding": "20px", "borderRadius": "10px", "color": "white"})

    fig_line = px.line(
        df,
        x="Дата",
        y=["Доходы", "Расходы"],
        title="Динамика доходов и расходов"
    )

    fig_pie = px.pie(
        df,
        values="Расходы",
        names="Категория",
        title="Структура расходов по категориям"
    )

    fig_hist = px.bar(
        df,
        x="Дата",
        y="Прибыль",
        title="Прибыль по месяцам"
    )

    fig_scatter = px.scatter(
        df,
        x="Товары",
        y="Прибыль",
        title="Корреляция: Товары vs Прибыль"
    )

    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("records")

    return (
        fig_line, fig_pie, fig_hist, fig_scatter,
        data, columns, kpi_income, kpi_expense, kpi_profit
    )

if name == "main":
    app.run(debug=True, port=8050)