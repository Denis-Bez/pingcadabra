from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    TypeHandler,
    filters
    )

from settings.application import application
from handlers import callback


# --- Type handlers ---
application.add_handler(TypeHandler(Update, callback.typehandler), -1)


# --- Conversation Handlers ---
manual_checking = ConversationHandler(
        entry_points=[CommandHandler("start", callback.start)],
        states={

            'MAIN_CHOOSING': 
            [
                CommandHandler('start', callback.start),
                CallbackQueryHandler(
                    callback.manual_checking, pattern="^manual_checking$"
                    ),
                CallbackQueryHandler(
                    callback.favorites, pattern="^favorites$"
                    ),
                CallbackQueryHandler(
                    callback.autochecking, pattern="^autocheck$"
                    ),
                CallbackQueryHandler(
                    callback.help, pattern="^help$"
                    ),
                CommandHandler('t', callback.test_async) # TODO: Deleted
            ],

            'TYPING_MANUAL_CHECKING': 
            [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    callback.host_checking
                )
            ],

            'CHOOSE_FAVORITE':
            [
                CallbackQueryHandler(
                    callback.check_favorite, pattern="^favorite_."
                    ),
                CallbackQueryHandler(
                    callback.delete_favorite, pattern="^delete_."
                    ),
                CallbackQueryHandler(
                    callback.type_favorite, pattern="^type_favorite$"
                    ),
                CallbackQueryHandler(
                    callback.favorites, pattern="^back$"
                    )
            ],

            'ADD_FAVORITE': 
            [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, callback.add_favorite
                )
            ],
            'CHOOSE_TIMER':
            [
                CallbackQueryHandler(
                    callback.set_autocheck, pattern="^setautocheck_."
                    ),
                CallbackQueryHandler(
                    callback.remove_job, pattern="^remove_job$"
                    )
            ],
            'BACK_TIMER_MENU':
            [
                CallbackQueryHandler(
                    callback.autochecking, pattern="^back$"
                    ),
            ]

        },
        fallbacks=[CommandHandler('start', callback.start), CallbackQueryHandler(callback.start, pattern="^menu$"), 
        CommandHandler('help', callback.help)],
    )

application.add_handler(manual_checking)

