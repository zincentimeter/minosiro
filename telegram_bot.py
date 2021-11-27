import logging
from pathlib import Path
from urllib.parse import urlparse

from telegram import (
    Update,
    ForceReply,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    Dispatcher,
    Filters,
    MessageHandler,
)

from lib.util import yaml
from lib.file import path, file

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class Command():

    def start(update : Update, context: CallbackContext) -> None:
        '''Send a message when the command /start is issued.'''
        user = update.effective_user
        update.message.reply_markdown_v2(
            text=f'Hi, {user.mention_markdown_v2()}\.',
            reply_markup=ForceReply(selective=True)
        )

    def attachment_download(update : Update, context : CallbackContext) -> int:
        '''Store attachment'''        
        user = update.message.from_user

        logger.info("User %s (id=%d) requested archiving files.",
                    user.first_name, user.id)

        if (user.id != admin_id):
            update.message.reply_text(
                f'Hi! {user.first_name}. I\'m sorry but this function is'
                f'under testing and not available to you.')
            return
        update.message.reply_text(fr'Archiving to local storage...')

        file_handler = update.message.document.get_file()
        byte_content = file_handler.download_as_bytearray()
        suffix_with_dot = Path(urlparse(file_handler.file_path).path).suffix
        local_dir = path.get_type_path(
            file_type='raw_data',**minosiro_conf['directory'])
        file_instance = file.File.create_from_bytes(
            byte_content, suffix_with_dot, local_dir)

        update.message.reply_text(
            f'Done. Your file is archived.\n'
            f'Saved to: {local_dir},\n'
            f'SHA256: {file_instance.sha256}.')

def handler_config(dispatcher : Dispatcher):
    dispatcher.add_handler(
        CommandHandler(command='start',callback=Command.start)
    )
    dispatcher.add_handler(
        CommandHandler(command='help',callback=Command.help)
    )
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.text & ~Filters.command,
            callback=Command.echo
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.attachment,
            callback=Command.attachment_download
        )
    )

if (__name__ == '__main__'):
    tg_conf = yaml.yaml_file_to_dict('conf/telegram.yaml')
    minosiro_conf = yaml.yaml_file_to_dict('conf/minosiro.yaml')

    token = tg_conf.get('bot_token', None)
    admin_id = tg_conf.get('bot_admin_id', None)
    proxy = minosiro_conf.get('proxy', None)

    updater = Updater(
        token=token,
        request_kwargs={'proxy_url':proxy['https']}
    )
    dispatcher = updater.dispatcher

    handler_config(dispatcher)
    print('@minosiro_bot is online!')
    updater.start_polling()
    updater.idle()