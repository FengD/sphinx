import re

def split_long_text(text, max_length=100):
    segments = re.split(r'(?<=[。\.])', text)
    result = []
    current_segment = ""
    
    for segment in segments:
        if len(current_segment) + len(segment) <= max_length:
            current_segment += segment
        else:
            if current_segment:
                result.append(current_segment)
            current_segment = segment
    if current_segment:
        result.append(current_segment)

    return result

def clean_no_need_text(text):
    text = text.replace('\n', ' ').strip()
    
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002500-\U00002BEF"  # Chinese characters
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "]+", flags=re.UNICODE
    )
    
    cleaned_text = emoji_pattern.sub(r'', text)
    
    return cleaned_text

def normalize_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[…？！；]', '。', text)
    text = re.sub(r'[?!;]', '.', text)
    text = re.sub(r'[：、]', '，', text)
    text = re.sub(r'[:]', ',', text)
    text = re.sub(r'[《》【】（）“”’‘——￥」「]', '', text)
    text = re.sub(r'[<>\"\'\[\]\{\}\(\)\_\-\—+=*&%$#@]', '', text)
    text = re.sub(r'。+', '。', text)
    text = re.sub(r'，+', '，', text)
    text = re.sub(r'\.+', '.', text)
    text = re.sub(r'[āáǎà]', 'a', text)
    text = re.sub(r'[ēéěèê]', 'e', text)
    text = re.sub(r'[ōóǒò]', 'o', text)
    text = re.sub(r'[ü]', 'u', text)
    text = re.sub(r'[ǐî]', 'i', text)

    return text
