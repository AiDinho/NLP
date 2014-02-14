import urllib2, sys, time
from urllib2 import URLError
from random import randint


class dictCrawler:
    
    def __init__(self, vocabfile, sitesfile):
        self.vocab = []
        self.urlBases = []
        self.headers = {'User-Agent':'Mozilla 5.10'}
        
        self.vocabList(vocabfile)
        self.urlBasePool(sitesfile)
    
    def urlBasePool(self, sitesfile):    #build up a url sites pool
        with open(sitesfile, 'r') as fhandle:
            for line in fhandle:
                self.urlBases.append(line.strip())
    
    def vocabList(self, vocabfile):
        with open(vocabfile, 'r') as fhandle:
            for line in fhandle:
                self.vocab.append(line.strip())
    
    def crawl(self, url):
        request = urllib2.Request(url,None,self.headers)
        try:
            response = urllib2.urlopen(request)
            return response.read()
        except URLError, e:
            print e.reason
            return "No definition found."           
        
    def crawlManage(self):
        for word in self.vocab:
            time.sleep(1)
            k = randint(0,len(self.urlBases)-1)
            url = str(self.urlBases[k]) + str(word)            
            with open('./dict/raw/'+str(word), 'w') as fhandle:
                html = self.crawl(url)
                fhandle.write(html)

    def uniTest(self):
        print str(self.urlBases)


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        vocabfile = sys.argv[1]
        sitesfile = sys.argv[2]
    else:
        vocabfile = './words'  #use a words list in /usr/share/dict/
        sitesfile = './sites' 
    c = dictCrawler(vocabfile, sitesfile)
    c.crawlManage()