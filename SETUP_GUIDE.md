# Setup Guide — TAKNA Free Cinematic Shorts

## A. GitHub upload
1. Download and extract `TAKNA_FREE_CINEMATIC_SHORTS_COMPLETE.zip`.
2. Open the extracted `short-bot` folder.
3. Upload all files and folders inside it to the root of `Sibay12/-short-bot` on GitHub. Do not upload the outer folder as a nested directory.
4. Before replacing files, download a ZIP backup of the current repository.

## B. Add secrets
GitHub repository → Settings → Secrets and variables → Actions → New repository secret:
- `GEMINI_API_KEY`
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

Do not place secrets in `make_short.py`. Rotate any credential that has been exposed.

## C. First test (no upload)
1. GitHub → Actions → Daily Short → Run workflow.
2. Keep `dry_run` = `1`.
3. Wait for the run to finish.
4. Download the `short-video` artifact.
5. Watch `final.mp4`. Inspect `script.json` and `visual_sources.txt` too.

## D. Enable upload
Only after reviewing the video, run manually with `dry_run` = `0`. The default upload privacy is `private`. For the daily schedule, set repository variable `PRIVACY` to `private`, `unlisted`, or `public` as desired. The included schedule runs at 17:00 India Standard Time.

## E. Free limitations
This package uses free tools and free/public image sources. It does not call a paid AI video-generation API. It cannot produce photorealistic generated actors or true lip-sync. Commons images may vary in availability and licensing; review `visual_sources.txt` for every downloaded source. Free-tier quotas and GitHub/YouTube limits still apply.
