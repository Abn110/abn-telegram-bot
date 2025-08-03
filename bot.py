from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '7336115061:AAHFpMMTlh3OviqMpdMj_zzummPuvs8_tos'
CHANNEL_USERNAME = '@FCBarcelonaenn'

def is_user_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {'chat_id': CHANNEL_USERNAME, 'user_id': user_id}
    response = requests.get(url, params=params)
    data = response.json()
    if not data.get("ok"):
        return False
    status = data["result"]["status"]
    return status in ["member", "administrator", "creator"]

def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    if not is_user_subscribed(user.id):
        try:
            message.delete()
            context.bot.send_message(
                chat_id=chat.id,
                text=f"🚫 @{user.username or user.first_name}, you must join our channel to chat here: {CHANNEL_USERNAME}",
                reply_to_message_id=message.message_id,
            )
        except Exception as e:
            logger.error(f"Failed to delete message or notify user: {e}")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.group & Filters.text & (~Filters.command), handle_message))
    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
``
