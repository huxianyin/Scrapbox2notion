
def scrapbox_to_blocks(scrapbox):
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


class Box:
    def __init__(self, text: str, level: int) -> None:
        self.text = text
        self.children = []
        self.parent = None
        self.level = level

    def Add(self, child) -> None:
        self.children.append(child)

    def SetParent(self, parent):
        self.parent = parent

    def ToString(self):
        if len(self.children) == 0:
            return "{" + self.text + "}"
        else:
            string = "{" + self.text
            for child in self.children:
                string = string + child.ToString()
            return string+"}"

    def ToBlock(self):
        pass
