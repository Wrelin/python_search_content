import argparse
import re
import requests
import os

from lxml import html
from lxml.html.clean import Cleaner


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--out', required=True)

    return parser.parse_args()


def clean_content(content):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    cleaner.kill_tags = ['header', 'nav', 'noscript', 'footer', 'head']

    return cleaner.clean_html(content)


def format_content(content):
    list_doc = html.fromstring(content)
    string = str(list_doc.text_content())
    string = re.sub('\n +|\n\f+|\n\t+|\n\r+', '\n', string)

    return re.sub(r'([ \n\t\f\r])\1+', r'\1', string)


def search_content(url):
    req = requests.get(url, timeout=5)
    content = clean_content(req.content)
    return format_content(content.decode('utf-8'))


def write_content(filename, content):
    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(content)


def main():
    args = get_args()
    content = search_content(args.url)
    write_content(args.out, content)
    print('File successfully written.')


if __name__ == '__main__':
    main()
