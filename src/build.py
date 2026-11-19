import json,re
d=json.load(open('pairs2.json'));out={}
for k in d:
    tr=json.load(open(f'tricks{k}.json'));items=[]
    for i,(it,m) in enumerate(zip(d[k],tr)):
        if re.search(r'Pedigree ชุด|ใน pedigree',it['q']):continue
        it=dict(it);it['m']=m;it['n']=i;items.append(it)
    out[k]=items
out['13']=json.load(open('data13.json'))
js=json.dumps(out,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
t=open('template4.html',encoding='utf-8').read().replace('/*DATA*/',js)
art=t.replace('<!--PWA-HEAD-->\n','').replace('<!--PWA-SW-->\n','')
open('/home/claude/index.html','w',encoding='utf-8').write(art)
head='''<meta name="theme-color" content="#F2F1F6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Bio Cards">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
'''
sw='''<script>if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){})})}</script>
'''
pwa=t.replace('<!--PWA-HEAD-->\n',head).replace('<!--PWA-SW-->\n',sw)
open('/home/claude/pwa/index.html','w',encoding='utf-8').write(pwa)
s=open('/home/claude/pwa/sw.js').read()
s=re.sub(r'const VERSION = "biocards-v\d+";','const VERSION = "biocards-v5";',s)
open('/home/claude/pwa/sw.js','w').write(s)
print(len(art),len(pwa))
