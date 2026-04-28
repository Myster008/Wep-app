from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = InlineKeyboardButton(
        text="🎮 O'yin o'ynash",
        web_app=WebAppInfo(url="https://myster008.github.io/Wep-app/")
    )
    markup = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(
        "Salom! Tic-Tac-Toe o'ynashga tayyormisiz?",
        reply_markup=markup
    )

app = Application.builder().token("8394583141:AAFxJJNqApna-CShFnE3A-jfR7uIjli03SE").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()