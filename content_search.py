import argparse
import requests
import re
import os

from lxml import html
from lxml.html.clean import Cleaner
from content_tree import ContentTree


def write_content(filename, content):
    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(content)

    print('File successfully written.')


def get_clean_string(content, encoding):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    cleaner.kill_tags = ['header', 'nav', 'noscript', 'footer', 'head']
    content = cleaner.clean_html(content)

    try:
        content = content.decode(encoding)
    except UnicodeDecodeError:
        content = content.decode('utf-8')

    content = re.sub('\n +|\n\f+|\n\t+|\n\r+', '\n', content)
    return re.sub(r'([ \n\t\f\r])\1+', r'\1', content)


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    return requests.get(url, headers=headers, timeout=5)


def get_content_tree(url):
    data = get_data(url)
    content = get_clean_string(data.content, data.encoding)

    root = html.fromstring(content)
    tree = ContentTree()
    ContentTree.build_tree(tree, root)

    return tree.get_main_child()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--out', required=True)

    return parser.parse_args()


def main():
    args = get_args()
    content_tree = get_content_tree(args.url)
    write_content(args.out, content_tree.get_content())


if __name__ == '__main__':
    main()
