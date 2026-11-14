"""Free story-driven cinematic scene renderer for TAKNA Shorts.
Uses Wikimedia Commons photographs (where available) + a recurring animated host.
No paid image/video API is required. Attribution is saved in work/visual_sources.txt.
"""
from __future__ import annotations
import hashlib, math, os, random, re, subprocess, time
from pathlib import Path
from urllib.parse import quote
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

W, H, FPS = 540, 960, 12
ROOT = Path(__file__).parent.resolve()
LOGO = ROOT / 'assets' / 'tenaga_technology_logo_transparent.png'
COMMONS = 'https://commons.wikimedia.org/w/api.php'
SESSION = requests.Session()
SESSION.headers.update({'User-Agent':'TAKNA-Shorts-Free-Creator/1.0 (educational video project)'})


def _seed(s): return int(hashlib.sha256(str(s).encode('utf-8')).hexdigest()[:8],16)

def _commons_image(query, cache_dir):
    """Find a freely licensed Commons image; cache locally. Return (path, attribution)."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(query.encode()).hexdigest()[:16]
    cached = cache_dir / f'{key}.jpg'
    meta = cache_dir / f'{key}.txt'
    if cached.exists(): return cached, (meta.read_text(encoding='utf-8') if meta.exists() else query)
    terms = re.sub(r'[^\w\s-]', ' ', query, flags=re.UNICODE).strip()[:120] or 'historical place'
    try:
        r=SESSION.get(COMMONS, params={'action':'query','generator':'search','gsrsearch':f'filetype:bitmap {terms}','gsrnamespace':6,'gsrlimit':8,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1100,'format':'json'},timeout=25)
        r.raise_for_status(); pages=r.json().get('query',{}).get('pages',{})
        candidates=list(pages.values())
        random.Random(_seed(query)).shuffle(candidates)
        for page in candidates:
            info=(page.get('imageinfo') or [{}])[0]; url=info.get('thumburl') or info.get('url')
            if not url: continue
            ext=info.get('extmetadata') or {}
            license_name=(ext.get('LicenseShortName') or {}).get('value','License information on Commons page')
            artist=re.sub('<[^>]+>','', (ext.get('Artist') or {}).get('value','Author not listed'))[:180]
            pageurl=info.get('descriptionurl','https://commons.wikimedia.org/')
            data=SESSION.get(url,timeout=35); data.raise_for_status()
            tmp=cached.with_suffix('.tmp'); tmp.write_bytes(data.content)
            try:
                im=Image.open(tmp); im.verify()
                tmp.replace(cached)
                attribution=f"{page.get('title','Commons image')} | {artist} | {license_name} | {pageurl}"
                meta.write_text(attribution,encoding='utf-8')
                return cached,attribution
            except Exception:
                tmp.unlink(missing_ok=True)
    except Exception as e:
        print('Commons image search skipped:',str(e)[:180],flush=True)
    return None, f'No Commons image found for: {query}'


def _fallback_bg(kind, seed):
    rnd=random.Random(seed); im=Image.new('RGB',(W,H)); px=im.load()
    palettes={'temple':((18,20,35),(145,82,43)),'fort':((16,25,42),(111,87,62)),'forest':((5,25,22),(37,92,61)),'water':((5,27,48),(25,105,137)),'desert':((39,27,20),(190,126,66)),'space':((4,7,25),(43,32,78)),'dig':((28,23,19),(133,91,57)),'history':((12,20,35),(72,76,89))}
    a,b=palettes.get(kind,palettes['history'])
    for y in range(H):
        t=y/(H-1)
        c=tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
        for x in range(W): px[x,y]=c
    d=ImageDraw.Draw(im,'RGBA')
    # Cinematic depth silhouettes, never a fixed template scene.
    if kind in ('temple','fort'):
        for x in range(-30,W,95):
            h=rnd.randint(170,330); d.rectangle((x,H-h,x+65,H),fill=(5,9,17,190))
            d.polygon([(x-12,H-h),(x+30,H-h-55),(x+78,H-h)],fill=(8,12,21,210))
    elif kind=='forest':
        for x in range(-40,W,65):
            d.rectangle((x+20,300,x+42,H),fill=(7,24,20,220)); d.ellipse((x-35,170,x+95,440),fill=(9,49,36,210))
    elif kind=='water':
        for y in range(590,H,35): d.arc((-80,y-25,W+80,y+25),0,180,fill=(150,211,225,100),width=3)
    elif kind=='desert':
        d.polygon([(0,650),(120,510),(260,680),(410,530),(W,640),(W,H),(0,H)],fill=(143,91,48,255))
    else:
        for _ in range(90):
            x=rnd.randrange(W); y=rnd.randrange(H); d.ellipse((x,y,x+2,y+2),fill=(235,225,192,rnd.randrange(50,170)))
    return im


def _kind(text):
    t=text.lower()
    for k,words in {'temple':['temple','mandir','मंदिर','पूजा','शिव','विष्णु'],'fort':['fort','castle','किला','महल','राजा'],'forest':['forest','jungle','जंगल','वन'],'water':['sea','ocean','river','समुद्र','नदी','पानी'],'desert':['desert','रेगिस्तान','मरुस्थल','रेत'],'space':['space','planet','ग्रह','अंतरिक्ष','तारा'],'dig':['archae','excavat','खुदाई','पुरातत्व','अवशेष']}.items():
        if any(w in t for w in words): return k
    return 'history'


def _fit_crop(src, frame, zoom, panx, pany):
    sw,sh=src.size; scale=max(W/sw,H/sh)*zoom
    nw,nh=int(sw*scale),int(sh*scale)
    bg=src.resize((nw,nh),Image.Resampling.LANCZOS)
    maxx=max(0,nw-W); maxy=max(0,nh-H)
    x=int(maxx*(0.5+0.35*math.sin(panx))); y=int(maxy*(0.5+0.22*math.sin(pany)))
    return bg.crop((x,y,x+W,y+H)).convert('RGBA')


def _draw_host(im, frame, total, role, action, kind, scene_seed):
    """Recurring Indian male host; same facial identity, story-specific costume/prop and movement."""
    d=ImageDraw.Draw(im,'RGBA'); p=frame/max(1,total-1); phase=frame*2*math.pi/24
    # Host is intentionally in-scene, lower-left/third; walk cycle and gesture vary by story action.
    cx=int(W*(.34+.045*math.sin(p*math.pi*2))); base=H-95; bob=int(5*math.sin(phase*2))
    skin=(173,112,78,255); hair=(27,25,27,255); ink=(13,18,25,255)
    roletext=(role+' '+action+' '+kind).lower()
    if any(x in roletext for x in ['soldier','warrior','guard','सैनिक']): coat=(91,103,75,255); accent=(183,153,91,255)
    elif any(x in roletext for x in ['priest','पूजारी','पुजारी']): coat=(194,151,91,255); accent=(227,203,157,255)
    elif any(x in roletext for x in ['worker','मजदूर','कारीगर']): coat=(173,111,53,255); accent=(228,184,112,255)
    elif kind in ('forest','desert','dig'): coat=(89,112,91,255); accent=(201,166,111,255)
    else: coat=(45,93,119,255); accent=(205,169,113,255)
    # Contact shadow
    d.ellipse((cx-62,base-9,cx+62,base+12),fill=(0,0,0,100))
    stride=math.sin(phase); arm=math.sin(phase+1.2)
    # Legs with walking motion
    hip=(cx,base-205+bob)
    d.line((hip,(cx-20+int(20*stride),base-105),(cx-24+int(25*stride),base-15)),fill=(35,39,48,255),width=19)
    d.line((hip,(cx+22-int(20*stride),base-105),(cx+25-int(25*stride),base-15)),fill=(29,34,43,255),width=19)
    d.ellipse((cx-47+int(25*stride),base-20,cx-5+int(25*stride),base+1),fill=(20,23,30,255))
    d.ellipse((cx+4-int(25*stride),base-20,cx+47-int(25*stride),base+1),fill=(20,23,30,255))
    # torso / story costume
    d.rounded_rectangle((cx-43,base-330+bob,cx+43,base-185+bob),18,fill=coat,outline=ink,width=4)
    d.line((cx,base-320+bob,cx+2,base-194+bob),fill=accent,width=4)
    d.ellipse((cx-7,base-265+bob,cx+7,base-251+bob),fill=(230,199,132,255))
    # Head and consistent hair silhouette
    heady=base-410+bob
    d.ellipse((cx-47,heady,cx+47,heady+108),fill=skin,outline=ink,width=4)
    d.pieslice((cx-50,heady-17,cx+50,heady+80),180,360,fill=hair)
    d.polygon([(cx-48,heady+40),(cx-39,heady+5),(cx-12,heady-10),(cx+18,heady-7),(cx+45,heady+25),(cx+39,heady+42),(cx+15,heady+22),(cx-8,heady+19),(cx-30,heady+37)],fill=hair)
    # Eyes, eyebrows, nose, moustache and smile
    d.line((cx-29,heady+49,cx-12,heady+46),fill=ink,width=4); d.line((cx+12,heady+46,cx+29,heady+49),fill=ink,width=4)
    d.ellipse((cx-25,heady+53,cx-14,heady+66),fill=(250,244,225,255)); d.ellipse((cx+14,heady+53,cx+25,heady+66),fill=(250,244,225,255))
    d.ellipse((cx-21,heady+56,cx-16,heady+64),fill=ink); d.ellipse((cx+16,heady+56,cx+21,heady+64),fill=ink)
    d.line((cx,heady+62,cx-5,heady+78,cx+4,heady+80),fill=(115,69,55,255),width=3)
    d.arc((cx-17,heady+73,cx+18,heady+96),5,170,fill=(91,48,44,255),width=3)
    # Arms: one gestures toward evidence/landmark, alternate swing while walking
    left=(cx-39,base-310+bob); right=(cx+39,base-310+bob)
    if any(x in roletext for x in ['discover','find','खोज','देख','point','इशारा']):
        d.line((left,(cx-73,base-245),(cx-105,base-290)),fill=coat,width=17)
        d.ellipse((cx-116,base-302,cx-96,base-282),fill=skin)
    else:
        d.line((left,(cx-63,base-250+int(arm*13)),(cx-54,base-205)),fill=coat,width=17)
    d.line((right,(cx+66,base-248+int(arm*12)),(cx+73,base-205)),fill=coat,width=17)
    d.ellipse((cx+63,base-215,cx+83,base-194),fill=skin)
    # Story prop changes by scene type
    if kind=='dig' or any(x in roletext for x in ['archae','खुदाई','research']):
        d.line((cx+88,base-330,cx+123,base-165),fill=(113,79,48,255),width=8); d.line((cx+110,base-320,cx+139,base-309),fill=(180,185,188,255),width=8)
    elif kind=='temple':
        d.ellipse((cx+78,base-280,cx+105,base-252),fill=(246,185,66,240),outline=(255,226,148,255),width=3)
    elif kind=='fort':
        d.line((cx+83,base-310,cx+112,base-180),fill=(112,82,51,255),width=7); d.polygon([(cx+75,base-316),(cx+105,base-325),(cx+117,base-309)],fill=(174,177,174,255))
    elif kind=='water':
        d.rounded_rectangle((cx+78,base-280,cx+105,base-240),7,fill=(125,83,49,255),outline=accent,width=3)
    # Subtle logo, constant position and size
    if LOGO.exists():
        try:
            logo=Image.open(LOGO).convert('RGBA'); logo.thumbnail((66,66)); logo.putalpha(logo.getchannel('A').point(lambda v:int(v*.72)))
            im.alpha_composite(logo,(W-logo.width-15,15))
        except Exception: pass


def render_animated_scene(scene_text, narration, seconds, output_mp4, workdir, role='traveller', action='exploring'):
    workdir=Path(workdir); workdir.mkdir(parents=True,exist_ok=True)
    frames=workdir/'frames'; frames.mkdir(exist_ok=True)
    for old in frames.glob('f*.jpg'): old.unlink()
    text=f'{scene_text} {narration}'; kind=_kind(text); seed=_seed(text)
    # visual_query should describe the actual place/event in this story, not a generic stock mood.
    query=str(scene_text).strip()[:160] or f'{kind} historical scene'
    asset, attribution=_commons_image(query, ROOT/'work'/'commons_cache')
    if asset:
        try:
            bg=Image.open(asset).convert('RGB')
            if bg.width<400 or bg.height<300: asset=None
        except Exception: asset=None
    if not asset: bg=_fallback_bg(kind,seed)
    else:
        bg=ImageEnhance.Color(bg).enhance(.88); bg=ImageEnhance.Contrast(bg).enhance(1.08)
    (ROOT/'work').mkdir(parents=True,exist_ok=True)
    with (ROOT/'work'/'visual_sources.txt').open('a',encoding='utf-8') as f: f.write(attribution+'\n')
    total=max(24,int(float(seconds)*FPS))
    for i in range(total):
        p=i/max(1,total-1)
        frame=_fit_crop(bg,i,1.05+.11*p, p*math.pi*2, p*math.pi)
        # cinematic dark lower gradient for caption readability; captions are added later by ASS.
        overlay=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay,'RGBA')
        for y in range(620,H):
            alpha=int(95*(y-620)/(H-620)); od.line((0,y,W,y),fill=(4,8,16,alpha))
        frame=Image.alpha_composite(frame,overlay)
        _draw_host(frame,i,total,role,action,kind,seed)
        frame.convert('RGB').save(frames/f'f{i:05d}.jpg',quality=88,optimize=True)
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate',str(FPS),'-i',str(frames/'f%05d.jpg'),'-an','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p',str(output_mp4)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError('Scene render failed: '+p.stderr[-1200:])
    for old in frames.glob('f*.jpg'): old.unlink()
    return kind
