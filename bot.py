# verificare versiune biblioteca telegram
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(rf"Hi {user.mention_html()}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    mesaj_de_ajutor = """ Aici poti vedea:

    1. Vreamea in orce oras, 
                           de ex: vremea la chisinau
                           sau: /vremea la chisinau
    2. Curs valutar Euro, Dolari si Lei MD, 
                           de ex: curs cump 20 USD 
                           sau: /curs vanz 35 EUR 
    3. Informatii despre film, 
                           de ex: depre film avatar 2
                           sau: /film matrix 1999
    """
    await update.message.reply_text(mesaj_de_ajutor)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print(update.message.text)

    if "vremea" in str(update.message.text):
        from pogoda import oras

        print("Found!")
        oras1 = update.message.text.replace("vremea la", "")
        print(oras1)
        messaj = oras(oras1)
        await update.message.reply_text(messaj)
    elif "curs" in str(update.message.text):
        from curs import convert_to, tabela_valuta

        print("Found!")
        curs1 = update.message.text.replace("curs", "")
        if curs1 == "":
            await update.message.reply_text("Error: Introduceti curs")
            return
        print(curs1)
        if curs1:
            messaj = convert_to(curs1)
        else:
            messaj = """
            Scimb valutar USD si EUR
            mod de utilizare:
            curs cump 20 USD,
            curs vanz 35 EUR
            """ + str(
                tabela_valuta()
            )
        await update.message.reply_text(messaj)
    elif "film" in str(update.message.text):
        from film import film

        print("Found!")
        film1 = update.message.text.replace("film", "")
        if film1 == "":
            await update.message.reply_text("Error: Introduceti film")
            return
        print(film1)
        await update.message.reply_text("Caut pe IMDB informatii despre film...")
        messaj = film(film1)
        print(messaj)
        await update.message.reply_text(messaj)
    else:
        print("Not found!")
        await update.message.reply_text(update.message.text)


async def vremea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from pogoda import oras

    oras1 = update.message.text.replace("/vremea la ", "")
    if oras1 == "/vremea":
        await update.message.reply_text("Error: Introduceti oras")
        return
    print(oras1)
    messaj = oras(oras1)
    print(messaj)
    await update.message.reply_text(messaj)
    # await update.message.reply_text("Vremea buna")


async def film(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from film import film

    film1 = update.message.text.replace("/film", "")
    if film1 == "":
        await update.message.reply_text("Error: Introduceti film")
        return
    print(film1)
    await update.message.reply_text("Caut pe IMDB informatii despre film...")
    messaj = film(film1)
    print(messaj)
    await update.message.reply_text(messaj)


async def curs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from curs import convert_to, tabela_valuta

    curs1 = update.message.text.replace("/curs", "")
    print(curs1)
    if curs1:
        messaj = convert_to(curs1)
        print(messaj)
    else:
        messaj = """
        Scimb valutar USD si EUR
        mod de utilizare:
        /curs cump 20 USD,
        /curs vanz 35 EUR
        """ + str(
            tabela_valuta()
        )
        print("Curs de azi la MICB")
    await update.message.reply_text(messaj)


def main() -> None:
    from api_keys import get_api_key

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(get_api_key("tg")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vremea", vremea))
    application.add_handler(CommandHandler("film", film))
    application.add_handler(CommandHandler("curs", curs))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
    # print(oras("Chisinau"))
    # temperatura(oras("Chisinau"))
