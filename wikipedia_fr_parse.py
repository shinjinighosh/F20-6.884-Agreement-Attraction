import requests
from bs4 import BeautifulSoup
from keras.utils import get_file
from timeit import default_timer as timer
import os
import pandas as pd
import matplotlib.pyplot as plt
import bz2
import subprocess
import xml.sax
from WikiXml import WikiXmlHandler
import wiki_dump_parser
import wikiextractor


# get wikipedia files
base_url = 'https://dumps.wikimedia.org/frwiki/'
index = requests.get(base_url).text
soup_index = BeautifulSoup(index, 'html.parser')

dumps = [a['href'] for a in soup_index.find_all('a') if a.text == '20201120/']
print(dumps)
dumps_url = base_url + dumps[0]
dump_html = requests.get(dumps_url).text
soup_dump = BeautifulSoup(dump_html, 'html.parser')
files = []
for file in soup_dump.find_all('li', {'class': 'file'}):
    text = file.text
    if 'pages-articles' in text:
        files.append((text.split()[0], text.split()[1:]))

files_to_download = [file[0] for file in files if '.xml-p' in file[0]]
print(f'There are {len(files_to_download)} files to download.')
data_paths = []
file_info = []

keras_home = '/home/shinjini/.keras/datasets/'

start = timer()
for file in files_to_download:
    path = keras_home + file
    if not os.path.exists(keras_home + file):
        print('Downloading')
        data_paths.append(get_file(file, dumps_url))
        file_size = os.stat(path).st_size / 1e6

        file_articles = int(file.split('p')[-1].split('.')[-2]) - int(file.split('p')[-2])
        file_info.append((file, file_size, file_articles))

    else:
        data_paths.append(path)
        file_size = os.stat(path).st_size / 1e6

        file_number = int(file.split('p')[-1].split('.')[-2]) - int(file.split('p')[-2])
        file_info.append((file.split('-')[-1], file_size, file_number))

# inspect file sizes
print("The largest files are:")
print("Filename, file size, number of articles")
for thing in sorted(file_info, key=lambda x: x[1], reverse=True)[:5]:
    print(thing)

print(f'There are {len(file_info)} partitions.')

file_df = pd.DataFrame(file_info, columns = ['file', 'size (MB)', 'articles']).set_index('file')
file_df['size (MB)'].plot.bar(color = 'red', figsize = (12, 6))
# plt.show()

print(f"The total size of files on disk is {file_df['size (MB)'].sum() / 1e3} GB")

# print(data_paths)
data_path = data_paths[-1]

# inspect data
# lines = []
#
# for i, line in enumerate(subprocess.Popen(['bzcat'],
#                                           stdin=open(data_path),
#                                           stdout=subprocess.PIPE).stdout):
#     lines.append(line)
#     if i > 5e5:
#         break
#
# print(lines[-165:-100])


# Content handler for Wiki XML
# handler = WikiXmlHandler()

# Parsing object
# parser = xml.sax.make_parser()
# parser.setContentHandler(handler)
# for l in lines[-165:-109]:
#     parser.feed(l)
#
# print(handler._pages)

# ALTERNATIVE
xml_path = data_path[:-4]
base_path = "/home/shinjini/.keras/datasets/"
# xml_path = base_path + "frwiki-20201120-pages-articles-multistream6-p13574284p13718495.xml"
# xml_path = base_path + "frwiki-20201120-pages-articles1-p1p306134.xml"
# xml_path = base_path + "frwiki-20201120-pages-articles-multistream6-p9074284p10574283.xml"
# xml_path = base_path + "frwiki-20201101-pages-meta-current1-p1p306134.xml"
xml_path = base_path + "frwiki-20201101-pages-articles1-p1p306134.xml"
print("XML to use is", xml_path)

# wiki_dump_parser.xml_to_csv(xml_path)

# ALTERNATIVE
# python3 -m wikiextractor.WikiExtractor "/home/shinjini/.keras/datasets/frwiki-20201101-pages-articles1-p1p306134.xml"