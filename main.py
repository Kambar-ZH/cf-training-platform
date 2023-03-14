import logging
import json
import models 

from tools import generator, text, table
from modules.codeforces import api

from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def generate_problem_appointers(update, context):
    """Send table of appointers ans solvers when the command /generate is issued."""

    with open('json_data.json') as json_file:
        json_data = json.load(json_file)

        appointers = json_data
        solvers = generator.dearrangement(json_data)

        table_data = [["Назначает", "Решает", "Требуемый рейтинг задачи"]]

        for i in range(len(appointers)):
            user = api.get_user(solvers[i]["handle"])
            solver_rating = user['result'][0]['rating']
            min_problem_rating = int(int((solver_rating + 200) / 100) * 100)
            max_problem_rating = int(min_problem_rating + 100)
            table_data.append([
                appointers[i]["handle"], 
                solvers[i]["handle"], 
                f'{min_problem_rating}-{max_problem_rating}',
            ])

        update.message.reply_text(
            text.monospace(table.build(rows=table_data)), 
            parse_mode=ParseMode.MARKDOWN,
        )


def add_user(update, context):
    """Save users codeforces handle when the command /add_user is issued."""

    with open('json_data.json') as json_file:
        data = json.load(json_file)

        user_handle = update.message.text.replace('/add_user', '').strip(' ')

        if len(user_handle) == 0:
            update.message.reply_text('Ошибка. handle пользователя не может быть пустым')
            return

        exists = api.validate_user_not_exist(user_handle=user_handle)
        if not exists:
            update.message.reply_text('Ошибка. Данный пользователь не был найден в кодфорсе')
            return
        
        user = models.User(handle=user_handle)
        data.append(user)

        with open('json_data.json', 'w') as outfile:
            json.dump(data, outfile)

        update.message.reply_text(f'{user_handle} был добавлен в список участников')


def error(update, context):
    """Log Errors caused by Updates."""
    
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    """Start the bot."""

    TOKEN = "1752339795:AAFomsaP4I3hr2Xh6QYi3s09Yyps6nEGGM4"

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("add_user", add_user))
    dp.add_handler(CommandHandler("generate", generate_problem_appointers))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()