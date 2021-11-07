import pytest
from lib import parser


@pytest.mark.parametrize('scrapbox, expected', [
    ('[***** アジェンダ]', '# アジェンダ'),
    ('[**** アジェンダ]', '# アジェンダ'),
    ('\t[#*** アジェンダ]', '## アジェンダ'),
    ('[**# アジェンダ]', '### アジェンダ'),
    ('[** アジェンダ]', '### アジェンダ'),
    ('[**# アジェンダ]', '### アジェンダ'),
    ('[* アジェンダ]', '#### アジェンダ'),
    ('\t[* アジェンダ]', '#### アジェンダ'),
    ('[*# アジェンダ]', '#### アジェンダ')
])
def test_heading_scrapbox_to_markdown(scrapbox, expected):
    result = parser.scrapbox_to_markdown(scrapbox)
    assert result == expected


@pytest.mark.parametrize('scrapbox, expected', [
    ('[https://totoro.jpeg]', '![image](https://totoro.jpeg)')
])
def test_image_scrapbox_to_markdown(scrapbox, expected):
    result = parser.scrapbox_to_markdown(scrapbox)
    assert result == expected


@pytest.mark.parametrize('scrapbox, expected', [
    ('[totoro https://totoro.jpeg]', '[totoro](https://totoro.jpeg)')
])
def test_link_scrapbox_to_markdown(scrapbox, expected):
    result = parser.scrapbox_to_markdown(scrapbox)
    assert result == expected


@pytest.mark.parametrize('scrapbox, expected', [
    ('\t3/4（木）', '- 3/4（木）'),
    ('\t\t3/4（木）', '\t- 3/4（木）'),
    ('\t\t\t3/4（木）', '\t\t- 3/4（木）')
])
def test_list_scrapbox_to_markdown(scrapbox, expected):
    result = parser.scrapbox_to_markdown(scrapbox)
    assert result == expected


@pytest.mark.parametrize('scrapbox, expected', [
    ('[- 発表日時]', '~~発表日時~~')
])
def test_strike_scrapbox_to_markdown(scrapbox, expected):
    result = parser.scrapbox_to_markdown(scrapbox)
    assert result == expected


@pytest.mark.parametrize('scrapbox, expected', [
    ('[/ 発表日時]', '_発表日時_')
])
def test_italic_scrapbox_to_markdown(scrapbox, expected):
    result = parser.scrapbox_to_markdown(scrapbox)
    assert result == expected
