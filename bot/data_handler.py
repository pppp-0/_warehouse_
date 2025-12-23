# bot/data_handler.py

import pandas as pd
from datetime import datetime
from pathlib import Path

CSV_PATH = Path(file).resolve().parent.parent / "data" / "education_finance.csv"


def load_csv():
    """Загружает CSV и приводит колонки к нужному виду."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV не найден: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    print("DEBUG: реальные заголовки CSV:", df.columns.tolist())

    rename_map = {}

    if "Доход" in df.columns:
        rename_map["Доход"] = "Доходы"

    if "Расход" in df.columns:
        rename_map["Расход"] = "Расходы"

    if "Студенты" in df.columns:
        rename_map["Студенты"] = "Товары"

    if rename_map:
        df = df.rename(columns=rename_map)

    required = ["Доходы", "Расходы", "Категория", "Товары"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Не найдена обязательная колонка '{col}' в CSV.")

    df["Доходы"] = pd.to_numeric(df["Доходы"], errors="coerce").fillna(0)
    df["Расходы"] = pd.to_numeric(df["Расходы"], errors="coerce").fillna(0)
    df["Товары"] = pd.to_numeric(df["Товары"], errors="coerce").fillna(0).astype(int)

    if "Прибыль" not in df.columns:
        df["Прибыль"] = df["Доходы"] - df["Расходы"]
    else:
        df["Прибыль"] = pd.to_numeric(df["Прибыль"], errors="coerce").fillna(0)

    if "Дата" in df.columns:
        df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")

    return df


def save_csv(df):
    """Сохраняет CSV в файл."""
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")


def get_totals():
    df = load_csv()
    return (
        df["Доходы"].sum(),
        df["Расходы"].sum(),
        df["Прибыль"].sum(),
        df["Товары"].sum()
    )


def add_income(amount):
    df = load_csv()
    new_row = {
        "Дата": datetime.now().strftime("%Y-%m-%d"),
        "Категория": "Добавление дохода",
        "Доходы": float(amount),
        "Расходы": 0,
        "Товары": 0,
        "Прибыль": float(amount),
    }
    df.loc[len(df)] = new_row
    save_csv(df)


def add_expense(amount, category):
    df = load_csv()
    new_row = {
        "Дата": datetime.now().strftime("%Y-%m-%d"),
        "Категория": category,
        "Доходы": 0,
        "Расходы": float(amount),
        "Товары": 0,
        "Прибыль": -float(amount),
    }
    df.loc[len(df)] = new_row
    save_csv(df)


def set_products(count):
    df = load_csv()
    new_row = {
        "Дата": datetime.now().strftime("%Y-%m-%d"),
        "Категория": "Товары",
        "Доходы": 0,
        "Расходы": 0,
        "Товары": int(count),
        "Прибыль": 0,
    }
    df.loc[len(df)] = new_row
    save_csv(df)


def get_expense_categories():
    df = load_csv()
    return df.groupby("Категория")["Расходы"].sum().to_dict()