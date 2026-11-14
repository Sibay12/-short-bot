# TAKNA TECHNOLOGY — Free Cinematic Shorts Automation

A free-tool workflow for Hindi history/mystery Shorts. It creates a 9:16 video with story-specific scene queries, Wikimedia Commons imagery when available, a recurring illustrated in-story host, camera motion, Hindi narration, captions, music bed and optional YouTube upload.

## What this build does

- Generates a 6–8 scene Hindi story using the Gemini API free quota (Google may change free quotas/model availability).
- Requests a specific visual query, host role and host action for every story beat.
- Searches Wikimedia Commons without a paid image API; downloads and caches usable images. If a query has no usable image or the service is unavailable, it uses a generated cinematic background.
- Keeps the same illustrated host face/hair identity across scenes; clothing, role and prop vary by scene.
- Adds subtle TAKNA TECHNOLOGY logo, Edge TTS Hindi narration, captions and a low-volume generated music bed (or a user-supplied MP3).
- Creates `work/final.mp4`, `work/script.json`, and `work/visual_sources.txt`.
- Uploads to YouTube only when `DRY_RUN=0`.

## Honest quality / cost note

This is a free, image-led motion-graphics workflow—not a generative AI film model. The host is an illustrated recurring character with animated walking/gestures and scene props; it is not photorealistic, does not have AI lip-sync, and cannot guarantee that every historical scene has a matching Commons photograph. Camera movement and scene imagery add motion, but some source images are still photographs. Wikimedia Commons licenses vary; source/author/license links are recorded in `work/visual_sources.txt`. Review the attribution and license before reusing a generated video commercially. Gemini free-tier limits, GitHub Actions limits, and YouTube API quota apply; “free” does not mean unlimited.

## Setup

1. Extract the ZIP. Upload the **contents of `short-bot/`** to the root of your GitHub repository (not an extra nested folder). Back up the current repository first.
2. In GitHub → Settings → Secrets and variables → Actions, add repository secrets:
   - `GEMINI_API_KEY`
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`
3. Never paste keys/tokens into source files or chat. If a secret was exposed, rotate it and update GitHub.
4. Open Actions → Daily Short → Run workflow. Keep `dry_run` at `1` for the first run.
5. Download the `short-video` artifact and inspect `final.mp4`, `script.json`, and `visual_sources.txt`.
6. Only after approving the video, run again with `dry_run=0`. The scheduled daily workflow is configured for 5:00 PM IST and uploads automatically with privacy `private` unless you change the repository variable `PRIVACY` to `unlisted` or `public`.

## Local requirements

Python 3.12, FFmpeg, Noto Sans Devanagari fonts, and packages in `requirements.txt`.

```bash
pip install -r requirements.txt
# Linux package example: sudo apt-get install ffmpeg fonts-noto-core
export GEMINI_API_KEY='YOUR_KEY'
export DRY_RUN=1
python make_short.py
```

## Voice options

Default: `hi-IN-MadhurNeural`. Female: set `TTS_VOICE=hi-IN-SwaraNeural`. Optional speed: `TTS_RATE=+5%`.

## Folder notes

- `make_short.py` — story generation, voice, subtitles, assembly and YouTube upload.
- `story_animation.py` — Commons image retrieval and animated scene renderer.
- `assets/` — TAKNA TECHNOLOGY logo.
- `music/` — optional royalty-cleared MP3s. Only add music you have rights to use.
- `.github/workflows/daily.yml` — daily and manual GitHub Actions workflow.

## Troubleshooting

- Gemini 429/503: free quota or temporary capacity issue; retry later or change `GEMINI_MODEL` to a currently supported model in Google AI Studio.
- Commons image missing: fallback background is used; inspect `visual_sources.txt` and `script.json`.
- FFmpeg/subtitle errors: ensure `ffmpeg` and `fonts-noto-core` are installed.
- Upload errors: verify all four YouTube secrets and OAuth consent/test-user setup. Start with `DRY_RUN=1`.
