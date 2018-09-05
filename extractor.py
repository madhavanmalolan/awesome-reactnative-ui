import re
import urllib.request
import json
import datetime
from dateutil import parser
from credentials import creds
import sys
import time
ferr = open('errors.txt','w',encoding='utf-8')
fout = open('README.md','w', encoding='utf-8')
fout.write("# Awesome React Native UI Components\n");
def curl(url, retry=True):
    try:
        """"
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, url, creds['username'], creds['password'])

        auth_handler = urllib.request.HTTPBasicAuthHandler(p)

        opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(opener)    
        o = opener.open(url)
        return o.read()
        """
        return urllib.request.urlopen(url).read()
    except Exception as e:
        print(url)
        print(e)
        

def getRank(image):
    if 'shield' in image or 'badge' in image:
        return 0
    if ".gif" in image:
        return 10
    if ".png" in image:
        return 5
    if ".jpg" in image or ".jpeg" in image:
        return 3
    if ".svg" in image:
        return 2
    return 1

def getImage(repo):
    base = "https://raw.githubusercontent.com/"+repo+    "/master/"
    md = curl(base+"README.md")
    images1 = re.findall("\!\[.*?\]\((.*?)\)",str(md))
    images2 = re.findall("<img.*?src=[\'\"](.*?)[\'\"]",str(md))
    images = images1+images2
    images = sorted(images, key=lambda image : getRank(image), reverse=True)
    if len(images) == 0:
        return ''
    image = images[0]
    finalImage = image if image.startswith("http://") or image.startswith("https://") else base+image
    print(repo +" : "+finalImage)
    return finalImage



def getAgoString(z):
    d = parser.parse(z)
    now = datetime.datetime.now()
    if(now.year - d.year > 0):
        return str(now.year - d.year) + " year"+("" if now.year - d.year == 1 else "s")+ " ago"
    if(now.month - d.month > 0):
        return str(now.month - d.month) + " month"+("" if now.month - d.month == 1 else "s")+ " ago"
    return "This week"

def getRepoInfo(repo):
    response = {'stars':'','lastUpdate':'','issues':'', 'name':'','description':'', 'image':''}
    info = json.loads(curl('https://api.github.com/repos/'+repo))
    response['stars'] = str(info['stargazers_count'])
    response['lastUpdate'] = getAgoString(info['updated_at'])
    response['issues'] = str(info['open_issues'])
    response['name'] = info['name']
    response['description'] = info['description']
    response['image'] = getImage(repo)
    return response

count = 0;
print(sys.argv[1])
for line in open(sys.argv[1]).readlines():
    try:
        if line.startswith("#"):
            fout.write("\n\n#"+line+"\n\n")
            fout.write("|Repository | Activity | Demo|\n")
            fout.write("|---|---|---|\n")
        elif line.startswith('-'):
            print(count)
            count+=1
            repo,img = re.findall("\[(.*)\]\((.*)\)",line)[0]
            
            i = getRepoInfo(repo)
            fout.write("|[<h3>"+i['name']+"</h3>](https://github.com/"+repo+") : "+i['description']+"|<ul><li>Last updated : "+i['lastUpdate']+"</li><li>Stars : "+i['stars']+"</li><li>Open issues : "+i['issues']+"</li></ul>|![]("+i['image']+")|\n")
        time.sleep(121)
            
    except : 
        print("FAILED : "+line)
        ferr.write(line+"\n")

fout.close()
