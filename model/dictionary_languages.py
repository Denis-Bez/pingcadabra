lang_callback = {
    "start": {
        "ru":"Проверьте работает ли ваш сервер:",
        "en":"Check server availability:"
    },
    "main_menu": {
        "ru":["Проверить пинг", "Избранное", "Автопроверка", "О Боте"],
        "en":["Ping test", "Favorites", "Auto-check", "About Bot"]
    },
    "manual_checking": {
        "ru":"Введите адрес хоста\nПример: '85.193.93.171', 'worldcadabra.com'",
        "en":"Enter the host adress\nExample: '85.193.93.171', 'worldcadabra.com'"
    },
    "processing_message": {
        "ru":"Идет проверка работы хоста...",
        "en":"Waiting response of the host..."
    },
    "favorites": {
        "ru":"Сохраните адреса в избранном",
        "en":"Save the addresses in the favorites"
    },
    "favorites_keyboard": {
        "ru":["Удалить", "Добавить адрес в избранное"],
        "en":["Delete", "Add host to the favorites"]
    },
    "favorites_add": {
        "ru":"Адес добавлен в Избранное!",
        "en":"Host was added to the favorites!"
    },
    "no_more_5hosts": {
        "ru":"Можно использовать не более 5 адресов в избранном",
        "en":"You can use no more than 5 addresses in favorites"
    },
    "delete_favorite": {
        "ru":"Адрес удален из избранного",
        "en":"Host was removed from favorites"
    },
    "autocheck": {
        "ru":"Выберите интервал автопроверки",
        "en":"Select the auto-check interval"
    },
    "autocheck_keyboard": {
        "ru":["Автопроверка каждый час", "Автопроверка каждые 4 часа", "Автопроверка каждые 12 часов", "Отключить"],
        "en":["Auto-check every hour", "Auto-check every 4 hours", "Auto-check every 12 hours", "Turn off"]
    },
    "timer": {
        "ru":["Таймер включен (", "ч.)", "Таймер установлен (", "Таймер остановлен!"],
        "en":["The timer turn on (", "h.)", "Timer was set (", "Timer was turn off"]
    },
    "help": {
        "ru":
        "Описание:\n\n\
🌎 Бот позволяет автоматически проверять доступность IP-адреса или хоста, а так же показывает пинг (/start)\n\
🌍 Можно проверить ответ введя имя или адрес вручную\n\
🌏 Или же добавьте хосты в избранное\n\
🌎 И Установите таймер автопроверки\n\
    \nКонтакты: worldcadabra.com",   
        "en":
        "Description:\n\n\
🌎 Bot for Auto-check the reachability and ping IP addresses or hostnames (/start)\n\
🌍 You can check host response manually\n\
🌏 Or add hosts to the Favorites\n\
🌎 And set an auto-check timer\n\
    \nContacts: worldcadabra.com",
    }
}

def ping_response(response, lang, ip):
    if response[0] == "Input adress error":
        if lang == "ru":
            return f"Проверьте правильность ввода адреса хоста: {ip}\nПример: '85.193.93.171', 'worldcadabra.com'"
        elif lang == "en":
            return f"Check that the host address is entered correctly: {ip}\nExample: '85.193.93.171', 'worldcadabra.com'"
    elif response[0] == "Server online":
        if lang == "ru":
            return f"Устройство с адресом: {ip} - ONLINE.\nВремя ответа: {response[1]} мс"
        if lang == "en":
            return f"Host {ip} is - ONLINE.\nPing time: {response[1]} ms"
    elif response[0] == "Server offline":
        if lang == "ru":
            return f"Устройство с адресом: {ip} - OFFLINE.\nВремя ответа более {response[1]} мс"
        if lang == "en":
            return f"Host {ip} is - OFFLINE.\nPing time is longer than {response[1]} ms"