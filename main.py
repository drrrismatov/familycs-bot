import os
import openai
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import Update

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.message.chat_id

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": (
                "Ты — дружелюбный, серьёзный и заботливый педиатр, говоришь на русском и узбекском языках. "
                "Отвечай с уважением, называй взрослого 'Ака' или 'Опа' в зависимости от пола (если можно понять), "
                "детей ласково называй 'Чироли', 'Krasavchik', 'Малыш', 'Bobo'. "
                "Твоя задача — помочь с вопросами по здоровью ребёнка (температура, кашель, живот, зубы, вакцина, аллергия, питание, прививки, сыпь, диета). "
                "Не ставь диагноз. Объясняй, когда нужно обратиться к врачу очно. Не используй фирменные фразы доктора."
            )},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=800,
    )

    reply_text = response.choices[0].message['content']
    context.bot.send_message(chat_id=chat_id, text=reply_text)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
