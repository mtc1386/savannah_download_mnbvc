import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 起始URL
base_url = "http://download.savannah.gnu.org/releases/"

record_file_path = 'file_url.txt'
if not os.path.exists(record_file_path):
    with open(record_file_path, 'w') as file:
        pass
with open(record_file_path, 'r') as file:
    file_urls = [line.strip() for line in file]

# 函数用于下载指定URL的文件
def download_file(url, save_dir):
    if url in file_urls:
        pass
    else:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(save_dir, os.path.basename(url)), 'wb') as file:
                file.write(response.content)
        with open(record_file_path, 'a') as file:
            file.write(url + "\n")


# 函数用于递归下载目录中的文件
def download_files_in_directory(directory_url, save_dir):
    response = requests.get(directory_url)
    if response.status_code != 200:
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



def main():
    download_files_in_directory(base_url, r'./download_files')

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
