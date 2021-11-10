from dotenv import load_dotenv
from os.path import join, dirname
import os
from notion_client import Client


# 環境変数
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
notion = Client(auth=NOTION_TOKEN)


def create_block(parent_id, content, is_bullet=False):
    # print(content)
    if "gyazo" in content:
        url = content.split("[")[1][:-1]+".png"  # or png for small image
        block = image_block(url)
    elif "youtube" in content or "vimeo" in content:
        url = content.split("[")[1][:-1]
        block = video_block(url)
    elif len(content) > 2 and content[0] == ">":
        block = callout_block(content[2:])
    elif is_bullet:
        block = bulleted_block(content.lstrip())
    else:
        if "*" in content:
            bold = True
        else:
            bold = False
        if "~" in content:
            color = "orange"
        else:
            color = "default"
        if "/" in content:
            italic = True
        else:
            italic = False
        if "-" in content:
            strike = True
        else:
            strike = False
        if len(content) > 3 and content[0] == "[" and content[-1] == "]":
            content = content[2:-1]
        block = paragraph_block(content, bold, italic,
                                strike, False, color, None)

    new_block_id = notion.blocks.children.append(
        parent_id, children=[block])["results"][-1]["id"]
    return new_block_id


def paragraph_block(text: str,
                    bold: bool = False, italic: bool = False, strike: bool = False,
                    underline: bool = False, color: str = "default", url: str = None):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "text": [
                {
                  "type": "text",
                    "text": {
                        "content": text,
                        "link": url,
                    },
                    "annotations": {
                        "bold": bold,
                        "italic": italic,
                        "strikethrough": strike,
                        "underline": underline,
                        "code": False,
                        "color": color
                    },
                }
            ]
        }
    }


def bulleted_block(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "text": [
                {
                  "type": "text",
                    "text": {
                        "content": text,
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                }
            ]
        }
    }


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
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                    },
                }
            ],
            "icon": {
                "type": "emoji",
                "emoji": "💡"
            }
        }
    }


def equation_block(text: str):
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
