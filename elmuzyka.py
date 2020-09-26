import re
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path

if len(sys.argv)>1:
    outdir=sys.argv[1]
    if(outdir[-1]!='/'):
        outdir=outdir+"/"
else:
    sys.exit("błąd: brak katalogy wyjściowego do zapisania plików.")

pattern = re.compile("source: .*.mp3")
for licznik in range(18):
    page = urlopen ("https://www.polskieradio.pl/9/5403/Strona/"+str(licznik+1))
    soup = BeautifulSoup(page, 'html.parser')
    retli = soup.findAll ('i', {'class' : 'fa fa-volume-up ico-pr'}, limit=None)
    #link=soup.find('li',{'class' : 'article'})
    for link in soup.find_all('li',{'class' : 'article'}):
        title=link.getText().strip()
        reta=link.find('a')
        href='https://www.polskieradio.pl/'+reta['href']
        print('-------------------------------------------------------------')
        print('znaleziono odcinek: '+title)
        print('zidentyfikowano adres odcinka: '+href)
        pageo = urlopen (href)
        soupo = BeautifulSoup(pageo, 'html.parser')
        linko=soupo.find('h1',{'class' : 'title'})
        linkod=soupo.find('span',{'class' : 'time'})
        skrypt=soupo.find('aside',{'class' : 'clearfix list-files'})
        if skrypt is not None:
            titleo=linko.getText().strip()
            date=linkod.getText().strip()
            year=date[6:10]
            month=date[3:5]
            day=date[0:2]
            data=year+'.'+month+'.'+day
            print('tytuł odcinka: '+titleo)
            print('data odcinka: '+data)
            skryptt=skrypt.getText()
            x=re.search(pattern,skryptt)
            mp3address='https:'+x.group()[9:]
            print('adres odcinka: '+mp3address)
            site = urlopen(mp3address)
            meta = site.info()
            filesize=int(int(meta.get("Content-Length"))/1024/1024)
            print('wielkość pliku: '+str(filesize)+' MB')
            newname=data+'.'+titleo+'.mp3'
            filename=outdir+newname
            #sprawdzić czy taki plik już nie istnieje
            my_file = Path(filename)
            if my_file.exists():
                print('plik zostaje pominięty, ponieważ już został pobrany: '+newname)
            else:
                print('zapisywanie pliku: '+newname)
                data = site.read()
                with open(filename, 'wb') as f:
                    f.write(data)
    