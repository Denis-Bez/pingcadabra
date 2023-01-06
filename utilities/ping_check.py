import asyncio
import time

from pythonping import ping
import aioping 

# Using decorator
def test_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        operating_time = end_time - start_time
        print(f"Operating time: {'%.3f' % operating_time}")
        return result
    
    return wrapper


# TO DO: How doing this asynchronous
# Checking ping server. Example ip: "85.193.93.171", "worldcadabra.com"
def check_ping(ip):
    try:
        ping_time = ping(str(ip), timeout=2).rtt_avg_ms
    # Exception if 
    except Exception as e:
        print(e)
        return(["Input adress error", False])
    
    if int(ping_time) < 2000:
        return(["Server online", ping_time])
    else:
        return(["Server offline", ping_time])


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


    
    
    
