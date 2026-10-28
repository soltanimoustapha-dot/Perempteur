import json, requests, io, os, re, time
from PIL import Image
H={'User-Agent':'HeritagePrototype/1.0 (https://github.com/soltanimoustapha-dot/perempteur; soltanim@hotmail.com)'}
Q=json.load(open('heritage/queries.json'))
os.makedirs('heritage/img',exist_ok=True)
meta={}
for k,q in Q.items():
    try:
        r=requests.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','generator':'search','gsrsearch':q+' filetype:bitmap','gsrnamespace':6,'gsrlimit':8,'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':1000,'format':'json'},headers=H,timeout=30).json()
        pages=sorted(r.get('query',{}).get('pages',{}).values(),key=lambda p:p.get('index',99))
    except Exception as e:
        print(k,e); continue
    n=0; meta[k]=[]
    for p in pages:
        if n>=4: break
        ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
        if ii.get('width',0)<700: continue
        try:
            b=requests.get(ii['thumburl'],headers=H,timeout=40).content
            im=Image.open(io.BytesIO(b)).convert('RGB')
        except Exception as e:
            print(k,e); continue
        im.thumbnail((900,900)); fn=f'{k}_{n}.jpg'
        im.save('heritage/img/'+fn,quality=82)
        art=re.sub('<[^>]+>','',em.get('Artist',{}).get('value',''))[:80]
        meta[k].append({'file':fn,'title':p['title'],'license':em.get('LicenseShortName',{}).get('value',''),'artist':art,'page':ii.get('descriptionurl','')})
        n+=1; time.sleep(0.3)
    print(k,n)
json.dump(meta,open('heritage/meta.json','w'),ensure_ascii=False,indent=1)
b=requests.get('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson',timeout=60).content
open('heritage/land110.geojson','wb').write(b)
b=requests.get('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson',timeout=60).content
open('heritage/land50.geojson','wb').write(b)
