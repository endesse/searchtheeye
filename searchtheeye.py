#!/usr/bin/python

#import sys, getopt, requests, wget
import sys, getopt, requests, re, time
from bs4 import BeautifulSoup

def main(argv):

    url = "https://the-eye.eu/public/"                  #URL to scrap
    searchstring = ""                   #String to lookup
    recursive = True

    try:
        opts, args = getopt.getopt(argv,"hfs:u:",["searchstring=", "url="])
    except getopt.GetoptError:
        print ('searchtheeye.py -u <url> -s <searchstring>')                #Error handling: print correct syntax
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':                 #Display Help menu
            print ('searchtheeye.py -u <url> -s <searchstring>')
            sys.exit()
        elif opt in ("-f", "--folder"):                 #Sets recursive off to only lookup present folder
            recursive = False
        elif opt in ("-s", "--searchstring"):                   #Sets the string to lookup
            searchstring = arg
        elif opt in ("-u", "--url"):                    #Set a url that not the default: https://the-eye.eu/public/
            url = arg
    
    dir_walk(url,searchstring, recursive)

#def custom_bar(current, total, width=80):
#    print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))

#def dir_get(path):
#    wget.download(path, bar=custom_bar)

def dir_walk(path, query, recursive=True):

    response = requests.get(path)
    soup = BeautifulSoup(response.text, 'html.parser')

    for href in soup.html.find_all('a'):
        if href.text != "../":
            if recursive:
                is_folder = re.match('^(.*)\/$', href.text)
                if is_folder != None:
                    dir_walk(path+href.text, query)
                    time.sleep(1)                   #Wait one second for the next query to the URL to prevent filterings
                    
            #SEARCH HERE

    #dwninfo = soup.select_one('#cptrg').get("value")            #Download info for current index using wget

if __name__ == "__main__":
   main(sys.argv[1:])