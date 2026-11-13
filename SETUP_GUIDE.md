# Setup Guide (English)

## 1. Prepare the GitHub repository

Upload the complete contents of this project to the repository's default branch. Preserve the `.github/workflows/daily.yml` path.

## 2. Configure Google services

1. Create a Gemini API key at https://aistudio.google.com/apikey.
2. In Google Cloud Console, enable YouTube Data API v3: https://console.cloud.google.com/apis/library/youtube.googleapis.com.
3. Create the required OAuth client credentials: https://console.cloud.google.com/apis/credentials.
4. Obtain a YouTube refresh token using `get_token.py` and approve access with the channel owner's Google account.

## 3. Add GitHub Actions secrets

Open Repository Settings → Secrets and variables → Actions. Add:

- `GEMINI_API_KEY`
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

No stock-video API key is required.

## 4. Run a test without uploading

1. Open the Actions tab.
2. Select **Daily Short**.
3. Press **Run workflow**.
4. Set `dry_run` to `1`.
5. Start the workflow.
6. When complete, open the workflow run and download the `short-video` artifact.
7. Check `final.mp4` before enabling uploads.

## 5. Enable uploads

Run the workflow manually with `dry_run=0`. The default privacy status is `private`. To change it, add a repository variable named `PRIVACY` with one of `private`, `unlisted`, or `public`. Keep uploads private until you have verified the output.

## 6. Daily schedule

The workflow is scheduled for 5:00 PM India Standard Time (11:30 UTC). Scheduled runs upload using the `PRIVACY` variable, which defaults to `private`.

## 7. Video generation details

FFmpeg generates portrait 1080×1920 animated abstract scenes. It uses moving geometric elements, texture, scene labels, Hindi narration, Hindi captions, and a music bed. If MP3 files are placed in `music/`, one is selected as the background track; otherwise a synthetic ambient tone is generated.

This is not photorealistic AI video generation. It is an automated motion-graphics approach that avoids external stock-video APIs.

## 8. Troubleshooting

- Missing `GEMINI_API_KEY`: check the exact Secret name and value.
- Gemini quota/model error: check Google AI Studio quotas and model access.
- TTS failure: rerun the workflow; Edge TTS requires network access.
- FFmpeg error: inspect the workflow log and confirm the FFmpeg installation step succeeded.
- YouTube upload error: verify the OAuth credentials, refresh token, API enablement, and channel permissions.

Never paste API keys or refresh tokens into public files or chat.
