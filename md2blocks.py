from typing import List
from scrapbox_notation_to_md import scrapbox_to_md
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests


import json
from notion_client import Client


def scrapbox_to_blocks(scrapbox: List[str]):
    blocks = []
    for box in scrapbox:
        block = None
        if "gyazo" in box:
            url = box.split("[")[1][:-1]+".jpg"  # or png for small image
            block = image_block(url)
        elif "youtube" in box or "vimeo" in box:
            url = box.split("[")[1][:-1]
            block = video_block(url)
        else:
            pass

        if block:
            blocks.append(block)

    return blocks


def paragraph_block(text: str, bold: bool, italic: bool, underline: bool, color: str, url: str):
    pass


def bulleted_block():
    pass


def heading_block(level: int, text: str):
    return {
        "object": "block",
        "type": "heading_"+str(level),
        "heading_"+str(level): {
            "text": [
                {
                    "type": "text",
                    "text": {"content": text}
                }
            ]
        }}


def callout_block(text: str):
    pass


def equation_block(text: str):
    pass


def numbered_block():
    pass


def mention_block():
    pass


def code_block():
    pass


# media

def video_block(url: str):
    # only youtube and vimeo
    return {
        "object": "block",
        "type": "video",
        "video": {
            "caption": [],
            "type": "external",
            "external": {
                "url": url
            }
        }
    }


def image_block(url: str):
    return {
        "object": "block",
        "type": "image",
        "image": {
            "caption": [],
            "type": "external",
            "external": {
                "url": url
            }
        }
    }


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
        for content in contents:
            print(content)
        # page content to block
        new_blocks = scrapbox_to_blocks(contents)

        notion.blocks.children.append(block_id, children=new_blocks)
