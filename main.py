import os
from os.path import join, dirname
import requests
from dotenv import load_dotenv
from notion_client import Client
from tqdm import tqdm

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

limit = 10


test_block_url = "https://api.notion.com/v1/blocks/1b8f110831964c94b8f9e98ec02025e4/children"


def main():
    # get scrapbox data
    headers = {
        "Cookie": "connect.sid="+SCRAPBOX_KEY+";"
    }
    url = API_URL + SCRAPBOX_PROJECT + "?limit="+str(limit)
    r = requests.get(url, headers=headers)
    json_data = r.json()
    scrap_pages = json_data["pages"]
    print("Scrapbox Pages:", len(scrap_pages))

    # notion client

    notion = Client(auth=NOTION_TOKEN)
    notion_pages = notion.databases.query(NOTION_DATABASE)["results"]

    notion_page_dict = {page["properties"]["Title"]
                        ["title"][0]["text"]["content"]: page["id"]
                        for page in notion_pages}

    for page in tqdm(scrap_pages):
        page_title = page["title"]
        page_url = BASE_URL + SCRAPBOX_PROJECT+"/"+page_title.replace(" ", "_")
        # Notion : create new page to the database
        new_page = {
            "Title": {"title": [{"text": {"content": page_title}}]},
            "Link": {"type": "url", "url": page_url},
        }

        if not page_title in notion_page_dict:
            print("Create Page:", page_title)
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE}, properties=new_page)
        else:
            print("Update Page Content:", page_title)
            block_info = notion.blocks.retrieve(notion_page_dict[page_title])
            block_id = block_info["id"]

            # block = notion.blocks.children.list(block_id)  # append(new_block)
            # print(block_id)
            notion.blocks.children.append(block_id, children=new_block)
            break


if __name__ == "__main__":
    main()
