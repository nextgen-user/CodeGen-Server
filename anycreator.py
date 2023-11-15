import asyncio
import random
from duckduckgo_search import AsyncDDGS
import urllib.request

imgur=[]

def getimage(query):

    async def get_results():
        global imgur
        async with AsyncDDGS() as ddgs:
            async for r in ddgs.images(query, max_results=20):
                imgur.append(r["image"])

    asyncio.run(get_results())
    print(imgur)
    for i in range(1,10):
        try:
            filename=f"static/image{random.randint(1,1000)}.jpg"
            urllib.request.urlretrieve(random.choice(imgur), filename)
            print(filename)
            break
        except:
            pass
    return filename
