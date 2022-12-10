from datetime import time

from telegram import Update
from telegram.ext import ContextTypes

from keyboards import keyboards
from utilities import ping_check
from model import model
from settings.config import ADMIN_ID
from model.dictionary_languages import lang_callback, ping_response


# --- Start callback  ---
# Add new users to database or update last date of visiting
async def typehandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    # Define the language
    language = update.effective_user.language_code
    if language == 'ru' and 'be' and 'uk':
        context.user_data['language'] = 'ru'
    else:
        context.user_data['language'] = 'en'


# --- Main menu ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    
    # Add user to database or update time
    user_id = update.effective_user.id
    if model.Users.check_user_available(user_id):
        model.Users.date_update(user_id)
    else:
        model.Users.add_user(user_id)
        # Send message to admin
        await context.bot.send_message(chat_id=ADMIN_ID, text='Invited new user!')
    
    # Main menu
    user_lang = context.user_data['language']
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            lang_callback['start'][user_lang], reply_markup=keyboards.main_menu(user_lang)
            )
    else:
        await update.message.reply_text(
            lang_callback['start'][user_lang], reply_markup=keyboards.main_menu(user_lang)
            )
    
    return 'MAIN_CHOOSING'

# Information About bot
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=lang_callback['help'][user_lang], reply_markup=keyboards.navigation_keyboard(back=False))
    else:
        await update.message.reply_text(text=lang_callback['help'][user_lang], reply_markup=keyboards.navigation_keyboard(back=False))



# --- Manuail checking ---
async def manual_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=lang_callback['manual_checking'][user_lang])

    return 'TYPING_MANUAL_CHECKING'


async def host_checking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_lang = context.user_data['language']
    adress = update.message.text
    # How deleted this message after ping checking
    to_delete = await update.message.reply_text(lang_callback['processing_message'][user_lang])
    response = ping_check_view(adress, user_lang)
    await to_delete.delete()
    await update.message.reply_text(text=response, reply_markup=keyboards.navigation_keyboard(back=False))


# --- Favorite ---
async def favorites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    user_id = update.effective_user.id
    # This way, when we go from main menu
    if query:
        await query.answer()
        await query.edit_message_text(lang_callback['favorites'][user_lang], reply_markup=keyboards.main_favorite(user_id, user_lang))
    # This way, when we add new address to the favorites
    else:
        await update.message.reply_text(lang_callback['favorites_add'][user_lang], reply_markup=keyboards.main_favorite(user_id, user_lang))

    return 'CHOOSE_FAVORITE'


async def type_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=lang_callback['manual_checking'][user_lang])

    return 'ADD_FAVORITE'


async def add_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    adress = update.message.text
    user_id = update.effective_user.id
    
    # Checking that was no more 5 favorites
    count_favorite = len(model.Users.pull_favorite(user_id))
    if count_favorite > 4:
        await update.message.reply_text(f"🤷‍♂️ {lang_callback['no_more_5hosts'][user_lang]}", reply_markup=keyboards.navigation_keyboard())      
    else:
        # Save to database
        model.Favorites.add_favorite(adress, int(user_id))
    
    await favorites(update, context)
    return 'CHOOSE_FAVORITE'


async def delete_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    adress = query.data.split('_')[1]
    # Delete from database
    model.Favorites.delete_favorite(adress, user_id)
    await query.edit_message_text(lang_callback['delete_favorite'][user_lang], reply_markup=keyboards.navigation_keyboard())
    
    return 'CHOOSE_FAVORITE'


async def check_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    adress = query.data.split('_')[1]
    await query.edit_message_text(text=lang_callback['processing_message'][user_lang])
    response = ping_check_view(adress, user_lang)
    await query.edit_message_text(text=response, reply_markup=keyboards.navigation_keyboard())

    return 'CHOOSE_FAVORITE'


# --- Auctochecking ---
# Main menu of autichecking
async def autochecking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    timer_was_set = context.user_data.get('autocheck_status', False)

    await query.edit_message_text(text=lang_callback['autocheck'][user_lang], reply_markup=keyboards.autocheck_keyboard(timer_was_set, user_lang))

    return 'CHOOSE_TIMER'


# Callback when job queue is trigger
async def check_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.job.user_id
    user_lang = context.user_data['language']
    adresses = model.Users.pull_favorite(user_id)
    for adress in adresses:
        response = ping_check_view(adress, user_lang)
        try:
            response = await context.bot.send_message(chat_id=user_id, text=response)
        except Exception as e:
            #Check if user leave bot
            if str(e) == "Forbidden: bot was blocked by the user":
                current_jobs = context.job_queue.get_jobs_by_name(str(user_id))
                if current_jobs:
                    deleted_jobs(current_jobs, user_id)
                model.Users.user_leave(user_id)
                context.user_data['autocheck_status'] = False
            else:
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!Unknow error: {e}")


# Set autochecking, save job queues
async def set_autocheck(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    timer = int(query.data.split('_')[1])
    # TODO: Checking if user don't have favorite adresses
    # Autostart every 1, 4, 12 hours
    for i in range(0, 24, timer):
        context.job_queue.run_daily(check_queue, time(i, 0, 0, 0), user_id=user_id, name=str(user_id))
    context.user_data['autocheck_status'] = lang_callback['timer'][user_lang][0] + str(timer) + lang_callback['timer'][user_lang][1]
    # Add timer information to database
    model.Favorites.add_timer(user_id, timer)
    await query.edit_message_text(text=lang_callback['timer'][user_lang][2] + str(timer) + lang_callback['timer'][user_lang][1], reply_markup=keyboards.navigation_keyboard(menu=False))

    return 'BACK_TIMER_MENU'


# Delete job queue
async def remove_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_lang = context.user_data['language']
    query = update.callback_query
    await query.answer()
    job_name = str(update.effective_user.id)
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if current_jobs:
        deleted_jobs(current_jobs, job_name)
        context.user_data['autocheck_status'] = False
        await query.edit_message_text(lang_callback['timer'][user_lang][3], reply_markup=keyboards.navigation_keyboard(menu=False))
    
    return 'BACK_TIMER_MENU'


# --- Backend functions ---
def deleted_jobs(current_jobs, user_id) -> None:
    for job in current_jobs:
        job.schedule_removal()
        # Delete from database
    model.Favorites.delete_timer(int(user_id))


def ping_check_view(ip, lang) -> str:
    response = ping_check.check_ping(ip)
    return ping_response(response, lang, ip)


