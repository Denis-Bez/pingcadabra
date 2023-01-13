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
        entry_points=[CommandHandler("start", callback.start, block=False)],
        states={

            'MAIN_CHOOSING': 
            [
                CommandHandler('start', callback.start, block=False),
                CallbackQueryHandler(
                    callback.manual_checking, pattern="^manual_checking$", block=False
                    ),
                CallbackQueryHandler(
                    callback.favorites, pattern="^favorites$", block=False
                    ),
                CallbackQueryHandler(
                    callback.autochecking, pattern="^autocheck$", block=False
                    ),
                CallbackQueryHandler(
                    callback.help, pattern="^help$", block=False
                    )
            ],

            'TYPING_MANUAL_CHECKING': 
            [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    callback.host_checking, block=False
                )
            ],

            'CHOOSE_FAVORITE':
            [
                CallbackQueryHandler(
                    callback.check_favorite, pattern="^favorite_.", block=False
                    ),
                CallbackQueryHandler(
                    callback.delete_favorite, pattern="^delete_.", block=False
                    ),
                CallbackQueryHandler(
                    callback.type_favorite, pattern="^type_favorite$", block=False
                    ),
                CallbackQueryHandler(
                    callback.favorites, pattern="^back$", block=False
                    )
            ],

            'ADD_FAVORITE': 
            [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, callback.add_favorite, block=False
                )
            ],
            'CHOOSE_TIMER':
            [
                CallbackQueryHandler(
                    callback.set_autocheck, pattern="^setautocheck_.", block=False
                    ),
                CallbackQueryHandler(
                    callback.remove_job, pattern="^remove_job$", block=False
                    )
            ],
            'BACK_TIMER_MENU':
            [
                CallbackQueryHandler(
                    callback.autochecking, pattern="^back$", block=False
                    ),
            ]

        },
        fallbacks=[CommandHandler('start', callback.start, block=False), CallbackQueryHandler(callback.start, pattern="^menu$", block=False), 
        CommandHandler('help', callback.help, block=False)],
    )

application.add_handler(manual_checking)

