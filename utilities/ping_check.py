import asyncio
import time

import aioping 


# TO DO: How doing this asynchronous
# Checking async ping server. Example ip: "85.193.93.171", "worldcadabra.com"
async def check_ping(host):
    try:
        delay = await aioping.ping(host, timeout=5) * 1000
        return(["Server online", int(delay)])
        # print("Ping response in %.0f ms" % delay)

    except TimeoutError:
        return(["Server offline", 5000])
    
    except Exception as e:
        print(e)
        return(["Input adress error", False])


if __name__ == '__main__':

    print(asyncio.run(check_ping('habr.com')))



    
    
    
