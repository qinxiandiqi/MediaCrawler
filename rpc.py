import asyncio
import os
import sys
from xmlrpc.server import SimpleXMLRPCServer

import config
from media_platform.xhs import XiaoHongShuCrawler
from store import xhs as xhs_store
from tools import utils


def init():
    async def async_init():
        crawler = XiaoHongShuCrawler()
        crawler.init_config(platform="xhs",
                            login_type="qrcode",
                            crawler_type=None,
                            start_page=1,
                            keyword=None)
        config.HEADLESS = False
        await crawler.start()
        config.HEADLESS = True
    asyncio.get_event_loop().run_until_complete(async_init())


def search(keyword: str, start_page: int = 1) -> str:
    # 爬取搜索逻辑
    async def async_search():
        crawler = XiaoHongShuCrawler()
        crawler.init_config(platform="xhs",
                            login_type="qrcode",
                            crawler_type="search",
                            start_page=start_page,
                            keyword=keyword)
        await crawler.start()
    asyncio.get_event_loop().run_until_complete(async_search())
    xhs_json_store = xhs_store.XhsJsonStoreImplement()
    xhs_json_store.make_save_file_name
    output_json_file = f"{xhs_json_store.json_store_path}/{xhs_json_store.file_count}_search_contents_{utils.get_current_date()}.json"
    # 当前文件路径
    current = os.path.dirname(os.path.abspath(__file__))
    abs_output_json_file = os.path.join(current, output_json_file)
    print(f"Search result saved to {abs_output_json_file}")
    return abs_output_json_file


server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
# 注册MediaCrawler函数
server.register_function(search, 'search')

if __name__ == '__main__':
    try:
        init()
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        sys.exit(0)
