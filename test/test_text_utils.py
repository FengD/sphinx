import pytest
from ..sphinx.text_utils import split_long_text, clean_no_need_text, normalize_text

@pytest.fixture
def test_split_long_text():
    text = "这是一个测试。这是另一个测试。这个测试有点长，所以应该被分成多段。"
    result = split_long_text(text, max_length=10)
    assert len(result) == 4
    assert result[0] == "这是一个测试。"
    assert result[1] == "这是另一个测试。"
    assert result[2] == "这个测试有点长，"
    assert result[3] == "所以应该被分成多段。"

def test_clean_no_need_text():
    text = "测试😊，去除表情符号。"
    result = clean_no_need_text(text)
    assert result == "测试，去除表情符号。"

def test_normalize_text():
    text = "这是一个测试…？！；这个测试有特殊字符：、以及《》【】"
    result = normalize_text(text)
    assert result == "这是一个测试。这个测试有特殊字符，以及"
