# Automated Hindi YouTube Shorts Bot

A GitHub Actions workflow that creates a short Hindi mystery/history video using Gemini, Edge TTS, stock footage, FFmpeg, and the YouTube Data API. The project runs in GitHub's hosted runner; no Android APK or local server is required.

## Project contents

- `make_short.py` — generates the Hindi script, voiceover, footage montage, captions, and YouTube upload.
- `get_token.py` — helper for obtaining a YouTube OAuth refresh token.
- `requirements.txt` — Python dependencies.
- `.github/workflows/daily.yml` — scheduled and manual GitHub Actions workflow.
- `topics_done.json` — generated-topic history.
- `music/` — optional MP3 background music directory.
- `API_SETUP.md` — API key and first-run instructions.
- `SETUP_GUIDE.md` — complete setup guide.

## Quick start

1. Upload the complete contents of this folder to the root of your GitHub repository. Keep the `.github/workflows/` directory structure.
2. Add the five required GitHub Actions secrets listed in `API_SETUP.md`.
3. Open **Actions → Daily Short → Run workflow**.
4. Keep `dry_run` set to `1` for the first run.
5. Download the `short-video` artifact and review `final.mp4`.
6. After successful review, run manually with `dry_run` set to `0` to upload. Upload privacy defaults to `private`.

## Important

- The generated video narration, title, captions, and description are intentionally in Hindi. The setup instructions, code comments, and demonstration messages are in English.
- Pixabay is the primary stock-footage provider. An existing `PEXELS_API_KEY` can be used as an optional fallback.
- API keys must be stored in GitHub Actions Secrets, never committed to the repository.
- Review AI-generated historical claims before publishing.
- The scheduled workflow uploads with `private` visibility by default.
