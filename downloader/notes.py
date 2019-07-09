import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from shutil import rmtree
from os import path, mkdir, getcwd, listdir,unlink
from img2pdf import convert
import threading
import re
from tqdm import tqdm



print('''\n
--------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------

---------------------------------LECTURE NOTES DOWNLOADER-----------------------------------------    
--------------------------------------------------------------------------------------------------
---------------------------------------USER GUIDE-------------------------------------------------

notes id in url is string you get after "https://lecturenotes.in/notes/" and before "/"
example: if download url is " https://lecturenotes.in/notes/12168-programming-in-c/ "

enter only " 12168-programming-in-c " as notes id 
----------------------------------------------------------------------------------------------------

''')



def sorted_aphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

def getter(url, dest):
    urlretrieve(url, dest)



threads = []
base_url = 'https://lecturenotes.in/'
input_url = ''
temp_dir = path.join(getcwd(), "images")

input_url=input('Enter the notes id : ')
input_url=input_url.strip()
url = base_url+'notes/'+input_url+'/1'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'lxml')
total_page =soup.find('span', class_='total_page')
total_page =int(total_page.string.replace("/", "").strip())


try:
    mkdir('images')
except:
    rmtree(temp_dir)
    mkdir('images')
    
    

for i in tqdm(range(1, total_page+1)):
    url = base_url+'notes/'+input_url+'/{}'.format(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    div = soup.find('div', class_='pic')
    image_url = base_url+div['style'].strip().split('url(')[1].split(');')[0]
    image_loc = path.join(temp_dir, "page{}.jpg".format(i))

    t = threading.Thread(target=getter, args=(str(image_url),str(image_loc)))
    threads.append(t)
    t.start()
    

for t in threads:
    t.join()



image = []
for i in sorted_aphanumeric(listdir(temp_dir)):
    image.append(path.join(temp_dir, i))



with open("ThankYouKiitClub.pdf", "wb") as f:
        f.write(convert(image))
try:
    rmtree(temp_dir)

except :
    unlink(temp_dir)
    rmtree(temp_dir)


print('''\n
------------------------------------Process Completed-----------------------------------------------
---------------------------------LECTURE NOTES DOWNLOADER-----------------------------------------    
--------------------------------------------------------------------------------------------------
''')
