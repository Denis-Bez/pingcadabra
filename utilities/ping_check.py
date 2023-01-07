import asyncio
import time

import aioping 


# TO DO: How doing this asynchronous
# Checking async ping server. Example ip: "85.193.93.171", "worldcadabra.com"
async def ping_aio_check(host):
    try:
        delay = await aioping.ping(host, timeout=5) * 1000
        return(["Server online", delay])
        # print("Ping response in %.0f ms" % delay)

    except TimeoutError:
        return(["Server offline", 5000])
    
    except Exception as e:
        print(e)
        return(["Input adress error", False])


if __name__ == '__main__':
    
    # print(asyncio.run(ping_aio_check('worldcadabra.com')))
    print(asyncio.run(ping_aio_check('https://habr.com/')))
    # print(asyncio.run(ping_aio_check('worldcadabra.com')))
    # hosts = ['46.147.41.173', '85.193.93.171', '85.193.93.171', '85.193.93.171', '85.193.93.171', '46.147.41.173', '46.147.41.173', '46.147.41.173', '46.147.41.173']
    # # run()
    # start_time = time.time()
    # for host in hosts:
    #     # check_ping(host)
    #     asyncio.run(ping_aio_check(host))
    # end_time = time.time()
    # print(end_time - start_time)


    
    
    
