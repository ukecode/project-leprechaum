import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from lep_amqp import lep_amqp
from decouple import config

CLOUDAMQP_URL = config('CLOUDAMQP_URL')
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Oi, Sou um robo :)!, para maiores informacoes /help')

def help_command(update, context):
    user = update.message.from_user
    update.message.reply_text(f'Certo, {user.first_name}. \n '
                            'Sou um robo que faz downloads torrent direto para um servidor a partir de um AMQP (RabbitMQ!)!\n\n'
                            f'Para configurar seu id: {user.id}\n'
                            f'Para configurar sua queue: {user.username.lower()}')


def echo(update, context):
    # TODO: User ID Variavel de ambiente
    SECRET_ID = config('SECRET_ID')
    user = update.message.from_user
    if(user.id == int(SECRET_ID)):
        message = update.message.text
        amqp = lep_amqp(CLOUDAMQP_URL, user.username.lower())
        amqp.send_one(message, user.username.lower())
        update.message.reply_text("Seu Download foi enviado :)")
    else:
        update.message.reply_text("Nao te reconheco. Sinto muito \n"
                                "Sua mensagem nao foi processada!")


def main():
    """Start the bot."""
    # TODO: token variavel de ambiente
    TOKEN = config('TOKEN')
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://leprechaum-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
