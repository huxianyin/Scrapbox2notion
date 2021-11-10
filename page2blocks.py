import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from box_utils import create_block
from collections import deque


def parse_scrapbox(block_id: str, contents: str):
    id_queue = deque()
    id_queue.append(block_id)
    levels = deque([0])
    for idx, content in enumerate(contents):
        level = len(content) - len(content.lstrip())
        last_level = levels[-1]
        if level == 0:
            create_block(block_id, content)
            id_queue.clear()
            levels.clear()
            levels.append(0)
        elif last_level == 0 and level > 0:
            id = create_block(block_id, content, is_bullet=True)
            id_queue.append(id)
            levels.append(level)

        elif last_level > 0 and level > last_level:
            id = create_block(id_queue[-1], content, is_bullet=True)
            id_queue.append(id)
            levels.append(level)
        elif last_level > 0 and level < last_level:
            while True:
                l = levels.pop()
                id = id_queue.pop()
                if l < level:
                    break
            new_id = create_block(id, content, is_bullet=True)
            id_queue.append(new_id)
            levels.append(level)
        # print(levels)


# 環境変数
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SCRAPBOX_PROJECT = os.environ.get('SCRAPBOX_PROJECT')
SCRAPBOX_KEY = os.environ.get('SCRAPBOX_KEY')

BASE_URL = "https://scrapbox.io/"
API_URL = BASE_URL + "api/pages/"

block_id = "a13c4f327f6045778df4c4272f11cadc"

limit = 200


if __name__ == "__main__":
    headers = {
        "Cookie": "connect.sid="+SCRAPBOX_KEY+";"
    }
    # get pages
    url = API_URL + SCRAPBOX_PROJECT + "?limit="+str(limit)
    r = requests.get(url, headers=headers)
    json_data = r.json()
    scrap_pages = json_data["pages"]
    print("Scrapbox Pages:", len(scrap_pages))

    for page in scrap_pages:
        page_title = page["title"].replace(" ", "_")
        if not "Notion" in page_title:
            continue
        # get page content
        page_url = API_URL + SCRAPBOX_PROJECT + \
            "/"+page_title
        r = requests.get(page_url, headers=headers)
        page_data = r.json()
        pined = page_data["pin"]
        contents = [line["text"] for line in page_data["lines"][1:]]
        # print(contents)
        parse_scrapbox(block_id, contents)
