import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
app.title = "Обзор склада"

kpis = {
    "Вместимость": {"value": "491,898", "изменение": "-28.11%", "color": "#ff7f50"},
    "Количество товаров в каждой поставке": {"value": "794.91", "изменение": "-10.17%", "color": "#ff7f50"},
    "Пропускная способность": {"value": "15,030", "изменение": "-22.70%", "color": "#ff7f50"},
    "Количество жалоб": {"value": "11.07%", "изменение": "-22.06%", "color": "#32cd32"},
    "Показатель надежности доставки": {"value": "86.65%", "изменение": "+7.20%", "color": "#32cd32"},
}

complaints_data = [59, 16, 18, 7]
complaints_labels = ["Недостающие детали", "Поврежденная упаковка", "Отложенные", "Другое"]
complaints_colors = ["#00ffff", "#7fff00", "#ff7f50", "#ffff00"]

delivery_reliability_data = {
    "Нынешний месяц": [0.82, 0.83, 0.85, 0.84, 0.86, 0.87, 0.88, 0.90, 0.91, 0.89, 0.88],
    "Прошлый месяц": [0.88, 0.87, 0.85, 0.83, 0.82, 0.80, 0.79, 0.78, 0.79, 0.80, 0.81],
}

complaint_rate_data = {
    "Нынешний месяц": [0.15, 0.14, 0.14, 0.13, 0.13, 0.12, 0.11, 0.10, 0.09, 0.08, 0.09],
    "Прошлый месяц": [0.13, 0.14, 0.15, 0.16, 0.15, 0.14, 0.14, 0.15, 0.14, 0.13, 0.14],
}

new_complaints = [
    {"date": "2025-12-18", "color": "#ffff00", "text": "Товар был доставлен в неправильном порядке. Впоследствии было трудно найти нужные запчасти."},
    {"date": "2025-12-15", "color": "#7fff00", "text": "Упаковка была повреждена с одной стороны. Содержимое было в порядке."},
    {"date": "2025-12-15", "color": "#ff7f50", "text": "Доставка была нужна в субботу."},
    {"date": "2025-12-13", "color": "#00ffff", "text": "Не забудьте, пожалуйста, про вино. Оно нам очень нужно. :)"},
    {"date": "2025-12-07", "color": "#ff7f50", "text": "Только половина заказа была доставлена вовремя."},
    {"date": "2025-11-26", "color": "#00ffff", "text": "Пожалуйста, следите за мелочами. 2 из 3 позиций были не укомплектованы."},
    {"date": "2025-11-19", "color": "#00ffff", "text": "Было доставлено только 4 из 8 вин."},
    {"date": "2025-11-14", "color": "#7fff00", "text": "Сломанная коробка из-под вина и одна разбитая бутылка."},
    {"date": "2025-11-02", "color": "#00ffff", "text": "Яблоки не были доставлены."},
    {"date": "2025-10-29", "color": "#00ffff", "text": "2 из 3 предметов оказались неполными."},
]

def create_kpi_block():
    rows = []
    for key, val in kpis.items():
        rows.append(
            html.Div(style={"padding": "5px 0"}, children=[
                html.Div(key, style={"fontWeight": "500"}),
                html.Div([
                    html.Span(val[&quot;value"], style={"fontSize": "24px", "fontWeight": "600"}),
                    html.Small(val["change"], style={"color": val["color"], "marginLeft": "10px", "fontSize": "12px"})
                ])
            ])
        )
    return rows

def create_new_complaints():
    items = []
    for c in new_complaints:
        items.append(
            html.Div(style={"borderBottom": "1px solid #555", "padding": "6px 0"}, children=[
                html.Div([
                    html.Span(style={"backgroundColor": c["color"], "borderRadius": "50%", "display": "inline-block",
                                    "width": "12px", "height": "12px", "marginRight": "8px"}),
                    html.Span(c["text"]),
                ], style={"color": "white", "fontSize": "13px"}),
                html.Small(c["date"], style={"color": "#888", "fontSize": "10px", "display": "block", "marginTop": "3px"}),
            ])
        )
    return items

app.layout = html.Div(style={"fontFamily": "Arial", "backgroundColor": "#00aabb", "padding": "20px"}, children=[
    html.H2("Обзор склада", style={"color": "white"}),

    html.Div(style={"display": "flex", "gap": "15px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": "#008c9e", "padding": "15px", "flex": "1 1 300px"}, children=[
            html.H4("Эффективность месяца", style={"color": "white"}),
            html.Small("201910", style={"color": "#ddd"}),
            html.Div(create_kpi_block())
        ]),

        html.Div(style={"backgroundColor": "#333f48", "padding": "15px", "flex": "1 1 350px"}, children=[
            html.H4("Причины жалоб", style={"color": "white"}),
            html.Small("Последние 100 жалоб", style={"color": "#aaa"}),
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Pie(labels=complaints_labels, values=complaints_data, marker={"colors": complaints_colors}, hole=0)],
                    layout=go.Layout(margin=dict(l=0, r=0, t=30, b=0), legend={"font": {"color":"white"}})
                ),
                config={"displayModeBar": False},
            )
        ]),

        html.Div(style={"backgroundColor": "#333f48", "padding": "10px", "flex": "1 1 300px", "overflowY": "auto", "maxHeight": "400px"}, children=[
            html.H4("Новые жалобы", style={"color": "white"}),
            *create_new_complaints()
        ]),
    ]),

    html.Div(style={"display": "flex", "gap": "15px", "marginTop": "20px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": "#008c9e", "padding": "15px", "flex": "1 1 350px"}, children=[
            html.Div([
                html.H4("Показатель надежности доставки", style={"color": "white", "display": "inline-block"}),
                html.Small("Нынешний месяц", style={"color": "#7c94a9", "marginLeft": "10px"}),
                html.Small("Прошлый месяц", style={"color": "#7c94a9", "marginLeft": "20px"}),
                html.Small("85.54%", style={"float": "right", "color": "white"}),
                html.Small("В среднем 30 дней", style={"float": "right", "marginRight": "40px", "color": "#7c94a9"})
            ]),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Scatter(y=delivery_reliability_data["Нынешний месяц"], mode="lines", line=dict(color="white")),
                        go.Scatter(y=delivery_reliability_data["Прошлый месяц"], mode="lines", line=dict(color="#7c94a9")),
                    ],
                    layout=go.Layout(plot_bgcolor="#008c9e", paper_bgcolor="#008c9e",
                                     margin=dict(l=40, r=20, t=20, b=30),
                                     xaxis=dict(showgrid=False, zeroline=False),
                                     yaxis=dict(range=[0.78, 0.9], gridcolor="#004d56"))
                ),
                config={"displayModeBar": False},
            )
        ]),

        html.Div(style={"backgroundColor": "#008c9e", "padding": "15px", "flex": "1 1 350px"}, children=[
            html.Div([
                html.H4("Количество жалоб", style={"color": "white", "display": "inline-block"}),
                html.Small("Нынешний месяц", style={"color": "#7c94a9", "marginLeft": "10px"}),
                html.Small("Прошлый месяц", style={"color": "#7c94a9", "marginLeft": "20px"}),
                html.Small("11.77%", style={"float": "right", "color": "white"}),
                html.Small("В среднем 30 дней", style={"float": "right", "marginRight": "40px", "color": "#7c94a9"})
            ]),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Scatter(y=complaint_rate_data["Нынешний месяц"], mode="lines", line=dict(color="white")),
                        go.Scatter(y=complaint_rate_data["Прошлый месяц"], mode="lines", line=dict(color="#7c94a9")),
                    ],
                    layout=go.Layout(plot_bgcolor="#008c9e", paper_bgcolor="#008c9e",
                                     margin=dict(l=40, r=20, t=20, b=30),
                                     xaxis=dict(showgrid=False, zeroline=False),
                                     yaxis=dict(range=[0.08, 0.18], gridcolor="#004d56"))
                ),
                config={"displayModeBar": False},
            )
        ]),
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
