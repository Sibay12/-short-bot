#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(__file__).resolve().parent
main=root/'make_short.py'
if not main.exists(): sys.exit('Run from existing short-bot repository root.')
src=main.read_text(encoding='utf-8')
if 'from story_animation import render_animated_scene' in src:
    print('Already patched.'); raise SystemExit(0)
a=src.find('# ---------------------------------------------------------------- 3. FREE PROCEDURAL VISUALS')
b=src.find('# ---------------------------------------------------------------- 4. CAPTIONS (ASS)')
if a<0 or b<0 or b<=a: sys.exit('Expected renderer section not found; no files changed.')
block='''# ---------------------------------------------------------------- 3. STORY-AWARE 2D ANIMATION
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


'''
src=src[:a]+block+src[b:]
# Append host-specific creative constraints to the existing Gemini prompt without disturbing its JSON schema.
needle='    data = gemini_json(prompt)'
extra='''    prompt += "\\n\\nVISUAL HOST RULE: Include the same recurring Indian male cartoon host in every scene. Keep his face, hair and identity consistent. He must be part of the story world (worker, visitor, researcher, traveller, etc.), not a studio news anchor. Change clothing/props to fit each story. Describe visible scene action in each visual field." 
'''
if needle in src: src=src.replace(needle,extra+needle,1)
src=src.replace('log("Visual mode: free FFmpeg-generated animated backgrounds; no stock-video API required.")',
                'log("Visual mode: story-aware 2D cartoon animation with recurring host and TAKNA TECHNOLOGY logo.")')
main.write_text(src,encoding='utf-8')
req=root/'requirements.txt'
old=req.read_text(encoding='utf-8') if req.exists() else ''
if 'Pillow' not in old: req.write_text(old.rstrip()+'\nPillow>=10.0.0\n',encoding='utf-8')
(root/'assets').mkdir(exist_ok=True)
logo=Path(__file__).resolve().parent/'assets'/'tenaga_technology_logo_transparent.png'
if not logo.exists(): sys.exit('Missing assets/tenaga_technology_logo_transparent.png')
print('Patch applied. Run GitHub Actions with dry_run=1 first.')
