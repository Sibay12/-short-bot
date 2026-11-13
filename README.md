# Free Automated Hindi YouTube Shorts Bot

This project creates Hindi mystery/history YouTube Shorts using Gemini for the script, Edge TTS for narration, and FFmpeg for video rendering.

## Free video generation mode

The project does **not** call Pixabay, Pexels, Veo, or another stock/video-generation API. FFmpeg creates animated abstract backgrounds locally during each run. This removes stock-footage API keys and rate limits.

The visuals are motion-graphics backgrounds (moving lines, panels, grain, vignette, and scene labels), not photorealistic AI-generated footage.

## Required GitHub Actions secrets

- `GEMINI_API_KEY` — Google AI Studio key for script generation.
- `YT_CLIENT_ID` — YouTube OAuth client ID.
- `YT_CLIENT_SECRET` — YouTube OAuth client secret.
- `YT_REFRESH_TOKEN` — YouTube OAuth refresh token.

No Pixabay or Pexels key is required.

## Run a safe test

1. Open **Actions → Daily Short → Run workflow**.
2. Keep `dry_run` set to `1`.
3. Run the workflow.
4. Download the `short-video` artifact and inspect `final.mp4`.
5. Only after confirming the result, run with `dry_run=0` to upload. The default upload privacy is `private`.

## Schedule

The workflow runs daily at 5:00 PM India Standard Time. Scheduled uploads use the `PRIVACY` repository variable, defaulting to `private`.

## Runtime and limits

- Video rendering is performed by FFmpeg on the GitHub Actions runner.
- Gemini API usage is subject to the current account's model availability, quotas, and free-tier limits.
- Edge TTS is a community client for Microsoft's online text-to-speech service; availability and service terms can change.
- GitHub Actions usage is subject to GitHub plan limits.
- This is free of a paid video-generation API, but it is not a guarantee of unlimited free compute or unlimited API usage.

## Project files

- `make_short.py` — script generation, narration, FFmpeg scenes, captions, assembly, and upload.
- `get_token.py` — obtains the YouTube refresh token.
- `.github/workflows/daily.yml` — scheduled GitHub Actions workflow.
- `requirements.txt` — Python dependencies.
- `topics_done.json` — previously used topics.
- `music/` — optional user-supplied MP3 background music. If empty, the bot creates a subtle synthetic drone.

## Safety

Keep credentials in GitHub Actions Secrets. Never commit API keys or OAuth tokens. The first test should use `dry_run=1`.
