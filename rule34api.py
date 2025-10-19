from aiohttp import ClientSession
from asyncio import get_event_loop, new_event_loop
from xmltojson import parse

class R34api():
    def __init__(self):
        self.session = ClientSession()
        self.headers ={'Connection': 'keep-alive', 'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8', 'sec-ch-ua-platform': '"linux"', 'host': 'rule34-api.netlify.app', 'referer': 'https://kurosearch.com/', 'origin': 'https://kurosearch.com', 'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}
        self.api = "https://rule34-api.netlify.app"

    def __del__(self):
        try:
            loop = get_event_loop()
            loop.create_task(self._close_session())
        except RuntimeError:
            loop = new_event_loop()
            loop.run_until_complete(self._close_session())

    async def _close_session(self):
        if not self.session.closed:
            await self.session.close()

    async def search_posts(self,page:int,tag:str):
        async with self.session.get(f"{self.api}/posts?limit=20&pid={page}&tags=sort:id:desc+{tag}+-young*+-loli*", headers=self.headers) as req:
            return await req.json()

    async def recomend_posts(self,page:int):
        async with self.session.get(f"{self.api}/posts?limit=20&pid={page}&tags=sort:id:desc+-young*+-loli*", headers=self.headers) as req:
            return await req.json()

    async def posts_count(self,page:int,tag:str):
        async with self.session.get(f"{self.api}/count?limit=20&pid={page}&tags=sort:id:desc+{tag}+-young*+-loli*", headers=self.headers) as req:
            return parse(await req.text())

