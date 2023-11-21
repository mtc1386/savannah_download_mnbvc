import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from datetime import datetime
import sys

# 生成日志文件
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = f'savannah_monitor_{current_time}.log'
logging.basicConfig(filename=log_file_name, level=logging.INFO, encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# 起始URL
base_url = "http://download.savannah.gnu.org/releases/"
file_urls = []
record_file_path = 'file_url.txt'


def prepare():
    # 支持命令行参数 '--new-record'，删除之前的记录文件，方便测试
    if not os.path.exists(record_file_path) or "--new-record" in sys.argv:
        with open(record_file_path, 'w'):
            pass
    with open(record_file_path, 'r') as file:
        file_urls = [line.strip() for line in file]


# 函数用于下载指定URL的文件
def download_file(url, save_dir):
    if url in file_urls:
        logging.info("文件已下载: " + url)
    else:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(save_dir, os.path.basename(url))
                dump_content(response.content, file_path)
                logging.info(f"文件下载成功, path: {file_path}, url: {url}")
            else:
                logging.error(
                    f"文件下载失败, status_code: {response.status_code}, url: {url}")

            with open(record_file_path, 'a') as file:
                file.write(url + "\n")
        except Exception as e:
            logging.error(f"文件下载报错, url: {url}, Error: {str(e)}")


# 函数用于递归下载目录中的文件
def download_files_in_directory(directory_url, save_dir):
    response = requests.get(directory_url)
    if response.status_code != 200:
        logging.error(
            f"目录URL访问失败, status_code: {response.status_code}, url:{directory_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # 遍历目录中的链接
    body = soup.find('tbody')
    try:
        for link in body.find_all("a"):
            file_url = urljoin(directory_url, link.get('href'))

            # 检查链接是否为目录或者上级目录的链接
            if link.text == "Parent Directory/" or link.text == "Parent directory/" or file_url == directory_url:
                continue

            if file_url.endswith('/'):  # 如果链接是目录，则递归下载
                subdir_name = os.path.join(save_dir, link.text)
                os.makedirs(subdir_name, exist_ok=True)
                download_files_in_directory(file_url, subdir_name)
            else:
                # 开始下载
                download_file(file_url, save_dir)
    except AttributeError:
        print('FLAG')
        print(directory_url)


def dump_content(content, file):
    # 支持命令行参数不要保存为文件，为测试用
    no_save = "--no-save" in sys.argv
    if no_save:
        print(f"Dump content into file: {file}")
    else:
        write_to_file(content, file)


def write_to_file(content, file):
    with open(file, 'wb') as file:
        file.write(content)


def main():
    prepare()
    logging.info("开始下载!")
    download_files_in_directory(base_url, r'./download_files')
    logging.info("任务完成!")


if __name__ == '__main__':
    main()

# FLAG
# http://download.savannah.gnu.org/releases/akfquiz/
# http://download.savannah.gnu.org/releases/bibledit/source/web/
# http://download.savannah.gnu.org/releases/comma/commaspec-html/
# http://download.savannah.gnu.org/releases/comma/doxygen/
# http://download.savannah.gnu.org/releases/construo/doxygen/
# http://download.savannah.gnu.org/releases/getfem/html/homepage/
# http://download.savannah.gnu.org/releases/getht/
# http://download.savannah.gnu.org/releases/liboggpp/dox/
# http://download.savannah.gnu.org/releases/swarm/apps/objc/contrib/lunabook/
# http://download.savannah.gnu.org/releases/swarm/docs/refbook-java/
