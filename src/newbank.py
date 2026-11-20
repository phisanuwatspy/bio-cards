import json,re,html
new=json.load(open('bank2_new.json',encoding='utf-8'))
DROP={'10':{0,1,2,3,4},'12':{0},
 '13':{1,3,4,6,8,9,13,17,20,21,22,24,25,26,28,30,31,32,42,44,46,47,48,49,50,51,52,53,56,59,60,62,64,65,66,69,71,74,75,84,86,87,89,90,115}}
def clean(s):
    s=re.sub(r'<sup>(.*?)</sup>',lambda m:m.group(1),s)
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    s=re.sub(r'\s*\((?:ดู)?สไลด์ \d+\)','',s)
    s=re.sub(r'\s*(?:ตาม|จาก|ใน)สไลด์ \d+','',s)
    s=s.replace('เข้ากับข้อมูลในเอกสาร','เป็นไปได้').replace('ตามข้อมูลในเอกสาร','')
    s=re.sub(r'(?:ตรงกับ|สอดคล้องกับ)เอกสาร','ถูกต้อง',s)
    s=re.sub(r'\s*(?:จาก|ใน)เอกสาร','',s)
    s=re.sub(r'\s*ตามเอกสาร','',s)
    s=re.sub(r'\s*\(ข้อมูลเสริม\)','',s)
    return re.sub(r'\s+',' ',s).strip()
def cleane(s):
    s=re.sub(r'<mark[^>]*>','\u0001',s).replace('</mark>','\u0002')
    s=re.sub(r'<sup>(.*?)</sup>',lambda m:m.group(1),s)
    s=html.unescape(re.sub(r'<[^>]+>','',s))
    s=re.sub(r'\s*\((?:ดู)?สไลด์ \d+\)','',s);s=re.sub(r'\s*(?:ตาม|จาก|ใน)สไลด์ \d+','',s);s=re.sub(r'\s*ตามเอกสาร','',s)
    s=re.sub(r'\s*\(ข้อมูลเสริม\)','',s)
    return re.sub(r'[ \t]+',' ',s).strip()
FIX={'13:104':('น้ำส้มสายชู',None),'13:105':('นัตโตะ',['ทวนจัง','ถั่วเน่า','ทวนจังผสมถั่วเน่า']),
 '13:116':('carrageenan',['agar','alginate','acetic acid']),'13:117':('Plasmodium อาศัยยุงเป็นพาหะ ต้องกันยุงกัด',None),
 '13:121':('เทมเป้',['ทวนจัง','ซอสปรุงรส','น้ำปลา']),
 '13:19':('ชอบกรด (acidophilic)',['ทนเค็มจัด (halophiles)','สร้างมีเทน (methanogen)','ทนแรงดันสูง (piezophile)'])}
out={}
for n,L in new.items():
    keep=[]
    for i,it in enumerate(L):
        if i in DROP.get(n,()):continue
        a=clean(it['o'][it['a']]);x=[clean(o) for k,o in enumerate(it['o']) if k!=it['a']]
        k=f'{n}:{i}'
        if k in FIX:
            a=FIX[k][0]; x=FIX[k][1] or x
        keep.append({'k':k,'s':it['sec'],'q':clean(it['q']),'a':a,'x':x,'e':cleane(it['e'])})
    out[n]=keep
json.dump(out,open('newbank_clean.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for n,L in out.items():
    for it in L:
        flag=' <<PAREN' if '(' in it['a'] and not all('(' in o for o in it['x']) else ''
        print(it['k'],'|',it['q'],'=>',it['a'],'| x:',' / '.join(it['x']),flag)
