from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from data_handler import (
    get_totals,
    add_income,
    add_expense,
    set_products,
    get_expense_categories
)

TOKEN = "8070247743:AAEfDoSNT0aMyh3GVZZYQsAc5EsU_yi7Brs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Я бот для управления финансовыми показателями склада.\n\n"
        "Доступные команды:\n"
        "/stats — показать статистику\n"
        "/add_income СУММА — добавить доход\n"
        "/add_expense СУММА КАТЕГОРИЯ — добавить расход\n"
        "/set_products КОЛ-ВО — изменить количество товаров\n"
        "/categories — расходы по категориям\n"
    )
    await update.message.reply_text(text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    income, expenses, profit, products = get_totals()
    text = (
        f"*Текущие показатели*\n\n"
        f"Доходы: *{income}*\n"
        f"Расходы: *{expenses}*\n"
        f"Прибыль: *{profit}*\n"
        f"Товары: *{products}*\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def add_income_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        add_income(amount)
        await update.message.reply_text(f"Доход {amount} ₽ добавлен!")
    except:
        await update.message.reply_text("Использование: /add_income 15000")

async def add_expense_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        category = " ".join(context.args[1:])
        add_expense(amount, category)
        await update.message.reply_text(f"Расход {amount} ₽ добавлен в '{category}'.")
    except:
        await update.message.reply_text("Использование: /add_expense 5000 Аренда")

async def set_products_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(context.args[0])
        set_products(count)
        await update.message.reply_text(f"Товаров теперь: {count}")
    except:
        await update.message.reply_text("Использование: /set_products 120")

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cats = get_expense_categories()

    if not cats:
        await update.message.reply_text("Расходов пока нет.")
        return

    text = "*Расходы по категориям:*\n\n"
    for cat, amount in cats.items():
        text += f"• {cat}: {amount} ₽\n"

    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("add_income", add_income_handler))
    app.add_handler(CommandHandler("add_expense", add_expense_handler))
    app.add_handler(CommandHandler("set_products", set_products_handler))
    app.add_handler(CommandHandler("categories", categories))

    app.run_polling()

if name == "main":
    main()