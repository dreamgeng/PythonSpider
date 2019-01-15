import requests
import re
import json
import time
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh; Tntel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    # return items
    # print(items)
    for item in items:
        yield {  # 生成器 生成一个字典
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),  # 去除首尾空格
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',  # 如果长度大于3，则提取[3:],否则空格
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()

        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:  # open(filename=result.txt, mode=a),open() 将会返回一个 file 对象
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')  # json.dumps	将 Python 对象编码成 JSON 字符串


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
