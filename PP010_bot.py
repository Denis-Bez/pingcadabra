import logging
from datetime import time

from handlers.handlers import application


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    # Doing job_queue persistance
    from handlers.callback import check_queue
    from model import model
    dict_timers = model.Favorites.get_autocheck_dict()
    for i in range(len(dict_timers['user_id'])):
        user_id = dict_timers['user_id'][i]
        timer = dict_timers['timer'][i]
        for j in range(0, 24, timer):
            application.job_queue.run_daily(check_queue, time(j, 0, 0, 0), user_id=user_id, name=str(user_id))
    
    # Run bot
    application.run_polling()