from pythonping import ping
import asyncio
import time

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
        ping_time = ping(str(ip)).rtt_avg_ms
    # Exception if 
    except Exception as e:
        print(e)
        return(["Input adress error", False])

    if int(ping_time) < 2000:
        print(ping_time)
        return(["Server online", ping_time])
    else:
        print(ping_time)
        return(["Server offline", ping_time])


async def async_check_ping(ip):
    try:
        ping_time = ping(str(ip)).rtt_avg_ms
    except Exception as e:
        print(e)
        return(["Input adress error", False])

    if int(ping_time) < 2000:
        print(ping_time)
        return(["Server online", ping_time])
    else:
        print(ping_time)
        return(["Server offline", ping_time])


async def async_run(ip):
    await async_check_ping('46.147.41.173')
    await async_check_ping('85.193.93.171')
    await async_check_ping('85.193.93.171')
    await async_check_ping('85.193.93.171')
    await async_check_ping('85.193.93.171')
    await async_check_ping('85.193.93.171')
    await async_check_ping('85.193.93.171')
    await async_check_ping('85.193.93.171')
    #await async_check_ping(ip)

if __name__ == '__main__':
    
    @test_time
    async def start():    
        #for i in ['85.193.93.171', '85.193.93.171', '85.193.93.171', '85.193.93.171', '85.193.93.171', '85.193.93.171', '85.193.93.171', '46.147.41.173']:
            #check_ping(i)
        asyncio.run(async_run(None))
    
    start()
    
