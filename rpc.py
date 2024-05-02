import asyncio
import sys
from xmlrpc.server import SimpleXMLRPCServer

from media_platform.xhs import XiaoHongShuCrawler


def init():
    async def async_init():
        crawler = XiaoHongShuCrawler()
        crawler.init_config(platform="xhs",
                            login_type="qrcode",
                            crawler_type=None,
                            start_page=1,
                            keyword=None)
        await crawler.start()
    asyncio.get_event_loop().run_until_complete(async_init())


def search(keyword: str, start_page: int = 1):
    # 爬取搜索逻辑
    async def async_search():
        crawler = XiaoHongShuCrawler()
        crawler.init_config(platform="xhs",
                            login_type="qrcode",
                            crawler_type="search",
                            start_page=start_page,
                            keyword=keyword)
        crawler.start()
    asyncio.get_event_loop().run_until_complete(async_search())


server = SimpleXMLRPCServer(("localhost", 8000))
# 注册MediaCrawler函数
server.register_function(search, 'search')

if __name__ == '__main__':
    try:
        init()
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        sys.exit(0)
