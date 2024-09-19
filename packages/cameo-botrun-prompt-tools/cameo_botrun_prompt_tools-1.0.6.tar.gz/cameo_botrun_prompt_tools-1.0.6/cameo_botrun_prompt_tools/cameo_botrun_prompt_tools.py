import os
from dotenv import load_dotenv
import json
from litellm import completion


load_dotenv(dotenv_path='./.env')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY is None:
    raise EnvironmentError("沒有設定OPENAI_API_KEY環境變數。請檢查您的.env文件或環境設置。")


def format_info_for_readability(
    info,
    prompt="請將以下資訊整理成方便人類閱讀的格式輸出：\n",
    model="gpt-4o-mini"
):
    if isinstance(info, (dict, list)):
        info_str = json.dumps(info, ensure_ascii=False, indent=2)
    else:
        info_str = str(info)
    
    full_prompt = f"{prompt}{info_str}"    
    response = completion(
        model=model,
        messages=[{"role": "user", "content": full_prompt}]
    )

    formatted_info = response.choices[0].message.content
    
    return formatted_info


def print_button(button_name, button_prompt):
    button_txt = f'@begin button(\"{button_name}\") {button_prompt} @end'
    print(button_txt)


def print_link(url, link_prompt):
    link_txt = f'@begin link(\"{url}\") {link_prompt} @end'
    print(link_txt)


def print_items(items, item_type):
    if not isinstance(items, list):
        raise TypeError(f"{item_type}s 參數必須是一個列表")
    
    for item in items:
        if item_type == "button":
            if not isinstance(item, dict) or 'label' not in item or 'content' not in item:
                raise ValueError("每個按鈕必須是包含 'label' 和 'content' 鍵的字典")
            print_button(item['label'], item['content'])
        elif item_type == "link":
            if not isinstance(item, dict) or 'url' not in item or 'content' not in item:
                raise ValueError("每個連結必須是包含 'url' 和 'content' 鍵的字典")
            print_link(item['url'], item['content'])


def print_buttons(buttons):
    print_items(buttons, "button")


def print_links(links):
    print_items(links, "link")
