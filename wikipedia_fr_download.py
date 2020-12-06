import requests
from bs4 import BeautifulSoup
from keras.utils import get_file
from timeit import default_timer as timer
import os

base_url = 'https://dumps.wikimedia.org/frwiki/'
index = requests.get(base_url).text
soup_index = BeautifulSoup(index, 'html.parser')

# dumps = [a['href'] for a in soup_index.find_all('a') if a.has_attr('href')]
dumps = [a['href'] for a in soup_index.find_all('a') if a.text == '20201120/']
print(dumps)
# dump_url = base_url + '20201120/'
dumps_url = base_url + dumps[0]
dump_html = requests.get(dumps_url).text
soup_dump = BeautifulSoup(dump_html, 'html.parser')
# print(soup_dump.find_all('li', {'class': 'file'})[:3])
# useful = "/frwiki/20201120/frwiki-20201120-pages-articles-multistream.xml.bz2"
files = []
for file in soup_dump.find_all('li', {'class': 'file'}):
    text = file.text
    if 'pages-articles' in text:
        files.append((text.split()[0], text.split()[1:]))

files_to_download = [file[0] for file in files if '.xml-p' in file[0]]
print(f'There are {len(files_to_download)} files to download.')

data_paths = []

start = timer()
for file in files_to_download:
    data_paths.append(get_file(file, dumps_url + file))

end = timer()
print(f'{round(end - start)} total seconds elapsed.')

