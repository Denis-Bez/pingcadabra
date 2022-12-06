from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from model import model
from model.dictionary_languages import lang_callback


# --- Main menu ---
def main_menu(lang):
    keyboard = [
        [InlineKeyboardButton(lang_callback['main_menu'][lang][0], callback_data='manual_checking')],
        [InlineKeyboardButton(lang_callback['main_menu'][lang][1], callback_data='favorites')],
        [InlineKeyboardButton(lang_callback['main_menu'][lang][2], callback_data='autocheck')],
        [InlineKeyboardButton(f"ℹ️ {lang_callback['main_menu'][lang][3]}", callback_data='help')],
    ]       
    return InlineKeyboardMarkup(keyboard)


# --- Favorites ---
def main_favorite(user_id, lang):
    favorites = model.Users.pull_favorite(user_id)
    keyboard = []
    for button in favorites:
        keyboard.append([InlineKeyboardButton(button, callback_data='favorite_'+str(button)), InlineKeyboardButton(lang_callback['favorites_keyboard'][lang][0], callback_data='delete_'+str(button))])
    
    # Invisible button if favorites = 5
    if len(favorites) < 5:
        keyboard.append([InlineKeyboardButton(lang_callback['favorites_keyboard'][lang][1], callback_data='type_favorite')])
    
    keyboard.append(template_nav_keyboard(back=False))

    return InlineKeyboardMarkup(keyboard)


# --- Autochecking ---
def autocheck_keyboard(timer_was_set, lang):
    keyboard = [
        [InlineKeyboardButton(lang_callback['autocheck_keyboard'][lang][0], callback_data='setautocheck_1')],
        [InlineKeyboardButton(lang_callback['autocheck_keyboard'][lang][1], callback_data='setautocheck_4')],
        [InlineKeyboardButton(lang_callback['autocheck_keyboard'][lang][2], callback_data='setautocheck_12')]
    ]
    # Button "Turn off"     
    if timer_was_set:
        keyboard.append([InlineKeyboardButton(timer_was_set, callback_data='remove_job'), InlineKeyboardButton(lang_callback['autocheck_keyboard'][lang][3], callback_data='remove_job')])
    
    keyboard.append(template_nav_keyboard(back=False))

    return InlineKeyboardMarkup(keyboard)


# --- Navigation keyboard ---
def template_nav_keyboard(menu=True, back=True):
    keyboard = []
    if back:
        keyboard.append(InlineKeyboardButton('↩️', callback_data='back'))
    if menu:
        keyboard.append(InlineKeyboardButton('🏠', callback_data='menu'))
    return keyboard


def navigation_keyboard(menu=True, back=True):
    keyboard = []
    keyboard.append(template_nav_keyboard(menu, back))
    return InlineKeyboardMarkup(keyboard)