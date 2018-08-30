import re
import urllib.request
import json
import datetime
from dateutil import parser

fout = open('README.md','w')
fout.write("# Awesome React Native UI Components\n");

def getImage(repo):
    base = "https://raw.githubusercontent.com/"+repo+    "/master/"
    md = urllib.request.urlopen(base+"README.md").read()
    images = re.findall("\!\[.*?\]\((.*?)\)",str(md))
    print(images)
    images = sorted(images, key=lambda image : 1 if image.endswith('.gif') else 0)
    if len(images) == 0:
        return ''
    image = images[0]
    return image if image.startswith("http://") or image.startswith("https://") else base+image

def getAgoString(z):
    d = parser.parse(z)
    now = datetime.datetime.now()
    if(now.year - d.year > 0):
        return str(now.year - d.year) + "year"+("" if now.year - d.year == 1 else "s")+ " ago"
    if(now.month - d.month > 0):
        return str(now.month - d.month) + "month"+("" if now.month - d.month == 1 else "s")+ " ago"
    if(now.day - d.day > 0):
        return str(now.day - d.day) + "day"+("" if now.day - d.day == 1 else "s")+ " ago"
    if(now.hour - d.hour > 0):
        return str(now.hour - d.hour) + "hour"+("" if now.hour - d.hour == 1 else "s")+ " ago"
    return "Just now"

def getRepoInfo(repo):
    response = {'stars':'','lastUpdate':'','issues':'', 'name':'','description':'', 'image':''}
    try:
        info = json.loads(urllib.request.urlopen('https://api.github.com/repos/'+repo).read())
        response['stars'] = str(info['stargazers_count'])
        response['lastUpdate'] = getAgoString(info['updated_at'])
        response['issues'] = str(info['open_issues'])
        response['name'] = info['name']
        response['description'] = info['description']
        response['image'] = getImage(repo)
        return response

    except Exception as e:
        print(e)
        return response


for line in open('components.txt').readlines():
    if line.startswith("#"):
        fout.write("\n\n#"+line+"\n\n")
        fout.write("|Repository | Activity | Demo|\n")
        fout.write("|---|---|---|\n")
    elif line.startswith('-'):
        repo,img = re.findall("\[(.*)\]\((.*)\)",line)[0]
        
        i = getRepoInfo(repo)
        fout.write("|<ul><li><b>"+i['name']+"</b></li><li>"+i['description']+"</ul>|<ul><li>Last updated : "+i['lastUpdate']+"</li><li>Stars : "+i['stars']+"</li><li>Open issues : "+i['issues']+"</li></ul>|![]("+i['image']+")|\n")

fout.close()
