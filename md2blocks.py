import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from notion_client import Client
from box_utils import Box


def parse_scrapbox(contents: str):
    last_head = 0
    all_boxes = []
    block = []
    for idx, content in enumerate(contents):
        head = len(content) - len(content.lstrip())
        # head为连续的递增数列为一个区块
        if head == 0:
            all_boxes.append(head)
        elif head > last_head and last_head == 0:
            block.append(idx)
        elif head > last_head:
            pass

        last_head = head
    # for box in boxes:
    #    print(box.ToString())

        # 環境変数
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SCRAPBOX_PROJECT = os.environ.get('SCRAPBOX_PROJECT')
SCRAPBOX_KEY = os.environ.get('SCRAPBOX_KEY')
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DATABASE = os.environ["NOTION_DATABASE"]

BASE_URL = "https://scrapbox.io/"
API_URL = BASE_URL + "api/pages/"

block_id = "1b8f110831964c94b8f9e98ec02025e4"

limit = 10

notion = Client(auth=NOTION_TOKEN)

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
        boxes = parse_scrapbox(contents)

        # page content to block
        #new_blocks = scrapbox_to_blocks(contents)

        #notion.blocks.children.append(block_id, children=new_blocks)
