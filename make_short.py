#!/usr/bin/env python3
"""Create a Hindi mystery-history YouTube Short with free FFmpeg motion graphics."""
import asyncio, glob, json, os, pathlib, random, re, subprocess, sys, time
from datetime import date

import requests

ROOT = pathlib.Path(__file__).parent.resolve()
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)
HISTORY = ROOT / "topics_done.json"

GEMINI_KEY = os.environ["GEMINI_API_KEY"]
MODELS = [os.getenv("GEMINI_MODEL", "gemini-3.8-flash"), "gemini-3.5-flash-lite"]
VOICE = os.getenv("TTS_VOICE", "hi-IN-MadhurNeural")  # Female voice option: hi-IN-SwaraNeural
RATE = os.getenv("TTS_RATE", "+8%")
PRIVACY = os.getenv("PRIVACY", "private")  # private / unlisted / public
DRY_RUN = os.getenv("DRY_RUN", "") == "1"  # 1 = generate the video only; do not upload
W, H = 1080, 1920


def log(*a):
    print(*a, flush=True)


def run(cmd):
    p = subprocess.run(cmd, cwd=WORK, capture_output=True, text=True)
    if p.returncode != 0:
        log("FFMPEG ERROR:\n", p.stderr[-2500:])
        raise RuntimeError("ffmpeg/ffprobe failed")
    return p.stdout


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)])
    return float(out.strip())


# ---------------------------------------------------------------- 1. SCRIPT
def load_history():
    if HISTORY.exists():
        try:
            return json.loads(HISTORY.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def gemini_json(prompt):
    last = None
    for model in MODELS:
        for attempt in range(3):
            try:
                r = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                    headers={"x-goog-api-key": GEMINI_KEY},
                    json={"contents": [{"parts": [{"text": prompt}]}],
                          "generationConfig": {"responseMimeType": "application/json",
                                               "temperature": 1.0}},
                    timeout=120)
                if r.status_code == 200:
                    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(txt)
                last = f"{model} {r.status_code}: {r.text[:200]}"
            except Exception as e:
                last = f"{model}: {e}"
            log("Gemini retry:", last)
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"Gemini failed: {last}")


def make_script(history):
    past = [h["title"] for h in history[-80:]]
    prompt = f"""तुम एक वायरल हिंदी YouTube Shorts राइटर हो। चैनल का niche: रहस्यमय और अनसुनी ऐतिहासिक कहानियाँ
(इतिहास के अनसुलझे रहस्य, रहस्यमयी जगहें, गायब हुए लोग/शहर/खज़ाने, अजीब ऐतिहासिक घटनाएँ; भारत और दुनिया दोनों)।

नियम:
- सिर्फ़ असली, अच्छी तरह दर्ज की गई घटनाएँ/रहस्य चुनो। कुछ भी मनगढ़ंत मत लिखो। जो बात किंवदंती या अनुमान है,
  उसके लिए "कहा जाता है" / "माना जाता है" जैसे शब्द इस्तेमाल करो। तारीख़ें और नाम सिर्फ़ तब दो जब पक्के पता हों।
- ये टॉपिक पहले बन चुके हैं, इनसे अलग चुनो: {json.dumps(past, ensure_ascii=False)}
- वीडियो 40-50 सेकंड का: कुल 95-115 हिंदी शब्द।
- पहला वाक्य ज़बरदस्त हुक हो (सवाल, चौंकाने वाला दावा या अधूरा रहस्य) जो पहले 2 सेकंड में रोक ले।
- बीच में तनाव बनाओ, आख़िर में लूप/सवाल: दर्शक कमेंट करे या दोबारा देखे।
- आसान बोलचाल की हिंदी, छोटे वाक्य। कोई गाली, हिंसा का ग्राफ़िक वर्णन, धर्म/जाति पर विवादित बात नहीं।
- 6 से 8 सीन। हर सीन का "visual" अंग्रेज़ी में 2-4 शब्द का stock-footage सर्च हो (vertical, generic, जैसे
  "ancient ruins fog", "old map table", "dark forest night", "desert sand dunes", "candle dark room")।
  किसी असली व्यक्ति/ब्रांड का नाम visual में मत डालो।

सिर्फ़ यह JSON लौटाओ:
{{
 "topic": "टॉपिक एक पंक्ति में",
 "title": "हिंदी टाइटल, 60 अक्षर तक, जिज्ञासा जगाने वाला, मुख्य कीवर्ड शुरू में",
 "hook": "स्क्रीन पर दिखने वाला 3-7 शब्द का हिंदी हुक",
 "scenes": [{{"narration": "हिंदी 1-2 छोटे वाक्य", "visual": "english query"}}],
 "description": "हिंदी में 2-3 पंक्तियाँ, SEO कीवर्ड के साथ",
 "tags": ["12-15 टैग, हिंदी और अंग्रेज़ी मिलाकर"],
 "hashtags": ["#रहस्य", "#इतिहास", "#अनसुनी_कहानी"]
}}"""
    prompt += "\n\nVISUAL HOST RULE: Include the same recurring Indian male cartoon host in every scene. Keep his face, hair and identity consistent. He must be part of the story world (worker, visitor, researcher, traveller, etc.), not a studio news anchor. Change clothing/props to fit each story. Describe visible scene action in each visual field." 
    data = gemini_json(prompt)
    scenes = [s for s in data.get("scenes", []) if s.get("narration") and s.get("visual")]
    if not (4 <= len(scenes) <= 10) or not data.get("title"):
        raise RuntimeError(f"Bad script JSON: {str(data)[:300]}")
    data["scenes"] = scenes
    return data


# ---------------------------------------------------------------- 2. VOICEOVER
async def tts_all(scenes):
    import edge_tts
    for i, s in enumerate(scenes):
        out = WORK / f"voice_{i}.mp3"
        for attempt in range(3):
            try:
                await edge_tts.Communicate(s["narration"], VOICE, rate=RATE).save(str(out))
                break
            except Exception as e:
                log("TTS retry", e)
                await asyncio.sleep(3)
        else:
            raise RuntimeError("TTS failed")
        s["audio_dur"] = duration(out)
        s["dur"] = s["audio_dur"] + 0.3


# ---------------------------------------------------------------- 3. STORY-AWARE 2D ANIMATION
from story_animation import render_animated_scene

def render_scene(i, s):
    render_animated_scene(
        scene_text=s.get("visual", "history scene"),
        narration=s.get("narration", ""),
        seconds=s["dur"],
        output_mp4=WORK / f"scene_{i}.mp4",
        workdir=WORK / f"scene_{i}_frames",
    )
    run(["ffmpeg", "-y", "-i", f"voice_{i}.mp3",
         "-af", f"apad=whole_dur={s['dur']:.2f}", "-ar", "44100",
         "-ac", "2", f"scene_{i}.wav"])


# ---------------------------------------------------------------- 4. CAPTIONS (ASS)
def ts(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{(cs // 6000) % 60:02d}:{(cs // 100) % 60:02d}.{cs % 100:02d}"


def clean(t):
    return re.sub(r"[{}\\]", "", t).replace("\n", " ")


def make_ass(script):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Noto Sans Devanagari,84,&H0000FFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,2,2,70,70,500,1
Style: Hook,Noto Sans Devanagari,104,&H00FFFFFF,&H000000FF,&H000000DD,&H80000000,1,0,0,0,100,100,0,0,1,9,3,8,70,70,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 1,{ts(0)},{ts(2.8)},Hook,,0,0,0,,{clean(script['hook'])}"]
    t = 0.0
    for s in script["scenes"]:
        words = s["narration"].split()
        chunks = [" ".join(words[k:k + 3]) for k in range(0, len(words), 3)]
        total_chars = sum(len(c) for c in chunks) or 1
        cur = t
        for c in chunks:
            d = s["audio_dur"] * len(c) / total_chars
            lines.append(f"Dialogue: 0,{ts(cur)},{ts(cur + d)},Cap,,0,0,0,,{clean(c)}")
            cur += d
        t += s["dur"]
    (WORK / "subs.ass").write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 5. VIDEO ASSEMBLY
def assemble(script):
    n = len(script["scenes"])
    (WORK / "v.txt").write_text("".join(f"file 'scene_{i}.mp4'\n" for i in range(n)))
    (WORK / "a.txt").write_text("".join(f"file 'scene_{i}.wav'\n" for i in range(n)))
    run(["ffmpeg", "-y", "-f", "concat", "-i", "v.txt", "-c", "copy", "video.mp4"])
    run(["ffmpeg", "-y", "-f", "concat", "-i", "a.txt", "-c", "copy", "voice.wav"])
    total = sum(s["dur"] for s in script["scenes"])

    tracks = glob.glob(str(ROOT / "music" / "*.mp3"))
    if tracks:
        music_in = ["-stream_loop", "-1", "-i", random.choice(tracks)]
        music_f = "[2:a]volume=0.12,lowpass=f=3000[m]"
    else:  # Generate a subtle dark drone if no music track is provided.
        music_in = ["-f", "lavfi", "-i", "sine=frequency=55:sample_rate=44100",
                    "-f", "lavfi", "-i", "sine=frequency=82:sample_rate=44100"]
        music_f = "[2:a][3:a]amix=inputs=2:normalize=0,volume=0.07,tremolo=f=0.3:d=0.5,lowpass=f=220[m]"

    fc = (f"{music_f};[1:a][m]amix=inputs=2:duration=first:normalize=0,"
          "loudnorm=I=-16:TP=-1.5:LRA=11[a];[0:v]subtitles=subs.ass[vv]")
    run(["ffmpeg", "-y", "-i", "video.mp4", "-i", "voice.wav", *music_in,
         "-filter_complex", fc, "-map", "[vv]", "-map", "[a]", "-t", f"{total:.2f}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "final.mp4"])
    run(["ffmpeg", "-y", "-ss", "0.9", "-i", "final.mp4", "-frames:v", "1", "-q:v", "2", "thumb.jpg"])
    log(f"Video created: {total:.1f} seconds")
    return WORK / "final.mp4", WORK / "thumb.jpg"


# ---------------------------------------------------------------- 6. YOUTUBE UPLOAD
def upload(video, thumb, script):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=os.environ["YT_CLIENT_ID"],
                        client_secret=os.environ["YT_CLIENT_SECRET"],
                        scopes=["https://www.googleapis.com/auth/youtube"])
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)

    title = clean(script["title"]).strip()
    if len(title) > 88:
        title = title[:88].rstrip()
    title += " #Shorts"
    tags, size = [], 0
    for t in script.get("tags", []):
        t = clean(str(t)).replace(",", "").strip()
        if t and size + len(t) + 1 < 450:
            tags.append(t)
            size += len(t) + 1
    hashtags = " ".join(script.get("hashtags", [])[:5])
    desc = (f"{clean(script['description'])}\n\n{hashtags} #Shorts\n\n"
            "ℹ️ This video was created with AI tools. Stories may draw on historical sources, "
            "traditions, and legends.")
    body = {"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": "27",
                        "defaultLanguage": "hi", "defaultAudioLanguage": "hi"},
            "status": {"privacyStatus": PRIVACY, "selfDeclaredMadeForKids": False}}
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(video), chunksize=-1, resumable=True))
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp["id"]
    log(f"Upload complete ({PRIVACY}): https://youtube.com/shorts/{vid}")
    try:  # Custom thumbnails require an eligible/verified channel; failure is non-fatal.
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb))).execute()
    except Exception as e:
        log("Thumbnail update skipped:", str(e)[:120])
    return vid, title


def main():
    history = load_history()
    script = make_script(history)
    log("Topic:", script["topic"], "|", script["title"])
    log("Visual mode: story-aware 2D cartoon animation with recurring host and TAKNA TECHNOLOGY logo.")
    asyncio.run(tts_all(script["scenes"]))
    for i, s in enumerate(script["scenes"]):
        render_scene(i, s)
    make_ass(script)
    video, thumb = assemble(script)
    (WORK / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
    if DRY_RUN:
        log("DRY_RUN is enabled: upload skipped.")
        return
    vid, title = upload(video, thumb, script)
    history.append({"date": str(date.today()), "topic": script["topic"], "title": title, "video_id": vid})
    HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("FAILED:", repr(e))
        sys.exit(1)
