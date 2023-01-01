from pythonping import ping
import asyncio

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
        return(["Server online", ping_time])
    else:
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

async def async_run():
    await async_check_ping('85.193.93.171')
    await async_check_ping('46.147.41.173')

if __name__ == '__main__':
    # print(check_ping('85.193.93.171'))
    asyncio.run(async_run())
    
