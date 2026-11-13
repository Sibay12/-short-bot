"""Procedural story-aware 2D cartoon renderer for the Shorts bot."""
import math, os, random, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

W,H,FPS=540,960,15
ROOT=Path(__file__).parent.resolve()
LOGO=ROOT/"assets"/"tenaga_technology_logo_transparent.png"

def kind_for(text):
    t=str(text).lower()
    rules={
      "temple":["temple","mandir","मंदिर","पूजा","शिव","विष्णु","देव"],
      "water":["sea","ocean","water","समुद्र","पानी","नदी","बाढ़"],
      "fort":["fort","castle","किला","महल","राजा"],
      "forest":["forest","jungle","जंगल","पेड़"],
      "desert":["desert","रेगिस्तान","रेत"],
      "space":["space","planet","earth","आकाश","ग्रह","पृथ्वी","तारा"],
      "dig":["dig","archae","खुदाई","पुरातत्व","अवशेष"]}
    for k,words in rules.items():
        if any(w in t for w in words): return k
    return "history"

def draw_bg(im,k,f,seed):
    d=ImageDraw.Draw(im,"RGBA")
    a,b=(7,16,40),(17,55,91)
    for y in range(H):
        q=y/H; c=tuple(int(a[i]*(1-q)+b[i]*q) for i in range(3))
        d.line((0,y,W,y),fill=c+(255,))
    rnd=random.Random(seed)
    if k in ("space","history","fort","temple"):
        for j in range(65):
            x=rnd.randrange(W); y=rnd.randrange(30,H-180); al=int(90+150*abs(math.sin(f*.12+j)))
            d.ellipse((x-2,y-2,x+2,y+2),fill=(215,235,255,al))
    if k=="water":
        for n in range(10):
            y=650+n*27
            d.line([(x,y+int(8*math.sin(x/25+f*.18+n))) for x in range(0,W+8,8)],fill=(75,185,235,190),width=3)
        for j in range(16):
            x=(j*41+f*2)%(W+20); y=560+(j*67)%350
            d.ellipse((x,y,x+7,y+7),outline=(190,230,255,150),width=2)
    elif k=="temple":
        d.polygon([(65,490),(270,245),(475,490)],fill=(30,43,72,255))
        d.rounded_rectangle((90,460,450,800),8,fill=(42,59,88,255))
        for x in (135,205,275,345,415): d.rounded_rectangle((x-15,480,x+15,770),5,fill=(115,143,168,255))
        d.polygon([(220,460),(270,350),(320,460)],fill=(75,94,125,255))
    elif k=="fort":
        d.polygon([(20,570),(20,370),(90,370),(90,320),(155,320),(155,390),(220,390),(220,300),(300,300),(300,390),(370,390),(370,330),(445,330),(445,390),(520,390),(520,570)],fill=(47,59,79,255))
        for x in range(60,500,90): d.rectangle((x,420,x+20,465),fill=(9,21,40,255))
    elif k=="forest":
        for x in range(-20,W+30,75):
            d.rectangle((x+25,420,x+42,850),fill=(29,57,54,255))
            d.polygon([(x-35,520),(x+34,260),(x+105,520)],fill=(21,82,68,255))
    elif k=="desert":
        d.polygon([(0,650),(120,560),(250,660),(390,550),(540,640),(540,960),(0,960)],fill=(139,103,65,255))
        d.polygon([(0,740),(180,650),(330,760),(470,660),(540,710),(540,960),(0,960)],fill=(105,82,61,255))
    elif k=="dig":
        d.rectangle((0,620,W,H),fill=(91,65,49,255))
        for x in range(25,W,70): d.arc((x,650,x+80,760),0,180,fill=(178,137,92,180),width=3)
    else:
        for x in range(-20,W,110): d.rectangle((x,620,x+95,830),fill=(49,66,83,140),outline=(100,125,150,100),width=2)
    for j in range(3):
        x=int((j*210+f*1.8)%(W+160))-80
        d.polygon([(x,0),(x+32,0),(x+210,H),(x+145,H)],fill=(95,173,226,14))

def draw_host(im,f,k):
    d=ImageDraw.Draw(im,"RGBA"); cx=270; bob=int(5*math.sin(f*.22))
    shirt="#c58a3f" if k in ("temple","dig","fort") else ("#2d9bc4" if k=="water" else "#397e9a")
    sw=int(22*math.sin(f*.18))
    d.ellipse((158,815,382,850),fill=(0,0,0,90))
    d.line([(cx-55,660),(cx-105-sw,730),(cx-80-sw,765)],fill=shirt,width=28)
    d.line([(cx+55,660),(cx+105+sw,715),(cx+80+sw,750)],fill=shirt,width=28)
    d.ellipse((cx-92-sw,746,cx-66-sw,775),fill="#d99a72")
    d.ellipse((cx+66+sw,731,cx+92+sw,760),fill="#d99a72")
    d.rounded_rectangle((cx-68,625+bob,cx+68,815+bob),28,fill=shirt,outline="#17233c",width=4)
    d.rounded_rectangle((cx-22,580+bob,cx+22,650+bob),10,fill="#d99a72")
    d.ellipse((cx-82,430+bob,cx-48,500+bob),fill="#d99a72",outline="#17233c",width=3)
    d.ellipse((cx+48,430+bob,cx+82,500+bob),fill="#d99a72",outline="#17233c",width=3)
    d.ellipse((cx-72,390+bob,cx+72,590+bob),fill="#e7ad83",outline="#17233c",width=4)
    d.pieslice((cx-76,370+bob,cx+76,505+bob),180,360,fill="#202333")
    d.polygon([(cx-72,450+bob),(cx-58,405+bob),(cx-25,385+bob),(cx+25,385+bob),(cx+62,415+bob),(cx+72,460+bob),(cx+42,435+bob),(cx,425+bob),(cx-38,440+bob)],fill="#202333")
    d.line([(cx-48,470+bob),(cx-24,464+bob)],fill="#382b2b",width=4); d.line([(cx+24,464+bob),(cx+48,470+bob)],fill="#382b2b",width=4)
    d.ellipse((cx-43,474+bob,cx-24,493+bob),fill="white"); d.ellipse((cx+24,474+bob,cx+43,493+bob),fill="white")
    d.ellipse((cx-36,478+bob,cx-29,489+bob),fill="#202333"); d.ellipse((cx+29,478+bob,cx+36,489+bob),fill="#202333")
    d.line([(cx,485+bob),(cx-8,520+bob),(cx+5,522+bob)],fill="#a96e5a",width=3)
    d.arc((cx-25,520+bob,cx+25,550+bob),5,175,fill="#713e3b",width=3)
    d.ellipse((cx-13,680+bob,cx+13,706+bob),fill="#0f9b91",outline="#e7f4ff",width=2)
    if f%90<35: d.line([(cx+90,725+bob),(cx+145,675+bob)],fill="#f3c86a",width=5)
    if LOGO.exists():
        logo=Image.open(LOGO).convert("RGBA"); logo.thumbnail((72,72))
        logo.putalpha(logo.getchannel("A").point(lambda v:int(v*.78)))
        im.alpha_composite(logo,(W-logo.width-14,14))

def render_animated_scene(scene_text,narration,seconds,output_mp4,workdir):
    k=kind_for(str(scene_text)+" "+str(narration)); frames=Path(workdir)/"frames"; frames.mkdir(parents=True,exist_ok=True)
    for old in frames.glob("f*.jpg"): old.unlink()
    for i in range(max(15,int(float(seconds)*FPS))):
        im=Image.new("RGBA",(W,H),(0,0,0,255)); draw_bg(im,k,i,abs(hash(str(scene_text)))%100000); draw_host(im,i,k)
        d=ImageDraw.Draw(im,"RGBA")
        for j in range(9):
            x=(j*61+i*(1+j%3))%W; y=(j*93+i*2)%(H-130)
            d.ellipse((x,y,x+3,y+3),fill=(210,230,255,110))
        im.convert("RGB").save(frames/f"f{i:05d}.jpg",quality=86)
    cmd=["ffmpeg","-y","-framerate",str(FPS),"-i",str(frames/"f%05d.jpg"),"-an","-c:v","libx264","-preset","veryfast","-crf","24","-pix_fmt","yuv420p",str(output_mp4)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError("Animated scene FFmpeg failed: "+p.stderr[-1000:])
    for old in frames.glob("f*.jpg"): old.unlink()
    return k
