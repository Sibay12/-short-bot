# Complete Setup Guide – TAKNA TECHNOLOGY Shorts Bot

## 1. Back up the old repository
Before replacing files, download the current GitHub repository as a ZIP and keep it on your device. Do not delete the old copy until the new workflow passes a test.

## 2. Upload this project
Extract the complete ZIP. Upload the contents of the `short-bot/` folder to the root of your GitHub repository. Keep hidden folders, especially `.github/workflows/`. Replace matching project files with these final versions. Do not upload the outer folder as a nested folder.

## 3. Create Gemini API key
1. Open https://aistudio.google.com/apikey
2. Create an API key.
3. Add it to GitHub as secret `GEMINI_API_KEY`.

Model access and free quota depend on Google's current policies and account.

## 4. Enable YouTube Data API
1. Open https://console.cloud.google.com/apis/library/youtube.googleapis.com
2. Select the Google Cloud project used for OAuth.
3. Enable YouTube Data API v3.
4. Open https://console.cloud.google.com/apis/credentials and create an OAuth client that supports the OAuth flow used by the token helper.
5. Complete the OAuth consent screen and test-user configuration as required by Google.

OAuth client type and permitted authorization flow can change with Google's policies. If the device authorization endpoint rejects the client type, use a supported OAuth installed-app flow and update the token helper accordingly; do not expose credentials.

## 5. Obtain YouTube refresh token
Use `get_token.py` in a private local or Colab session after entering your OAuth Client ID and Client Secret in that private copy. Approve access using the Google account that owns the channel. Copy the resulting refresh token directly into GitHub Secrets. Never put it in a public repository or chat.

## 6. Add GitHub secrets
Open Repository → Settings → Secrets and variables → Actions. Add these exact names:
- `GEMINI_API_KEY`
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

The values are sensitive. Do not share screenshots that reveal them.

## 7. Test without uploading
1. Open Actions.
2. Choose `Daily Short`.
3. Click `Run workflow`.
4. Keep `dry_run` set to `1`.
5. Start the run.
6. Download the `short-video` artifact.
7. Review the full video, voice, subtitles, logo, host continuity and facts.

A dry run does not upload the video.

## 8. Enable YouTube upload
After a successful review, manually run with `dry_run=0`. The default upload privacy is `private`. Keep it private until you confirm the result in YouTube Studio. To select another privacy level, configure the repository variable `PRIVACY` as `private`, `unlisted`, or `public`.

## 9. Daily automation
The included workflow is scheduled once a day at 17:00 IST (11:30 UTC). Scheduled runs are configured to upload. The default privacy is `private` unless the repository variable changes it. The first scheduled run should be monitored.

GitHub Actions schedules can be delayed and may be disabled in inactive repositories. Automation does not guarantee a video will publish if an API quota, token, network, runner, or upload error occurs.

## 10. Additional video
Use the manual workflow run again for an extra video. Start with `dry_run=1`, inspect it, then use `dry_run=0` to upload. Avoid launching multiple runs simultaneously.

## 11. Best upload time
This channel has no meaningful audience history yet. 17:00 IST is only an initial test time. After several weeks of uploads, open YouTube Studio → Analytics → Audience and review “When your viewers are on YouTube” (when enough data becomes available). Change the cron schedule based on the channel's own data, not generic claims.

## 12. Costs and limitations
The renderer uses free open-source FFmpeg and Pillow. Gemini API, GitHub Actions and online TTS each have separate quotas/terms and can change. This is not guaranteed to be unlimited free cloud compute. The host is a simple procedural 2D character; it is not a fully lip-synced AI actor.

## 13. Troubleshooting
- `GEMINI_API_KEY` missing: verify exact secret name.
- Gemini quota/model error: check Google AI Studio model availability and quota.
- TTS error: retry; online TTS requires network access.
- FFmpeg/font error: inspect Actions logs; ensure FFmpeg and Noto fonts installed.
- YouTube OAuth error: check token, client ID/secret, consent screen, channel-owner account and API enablement.
- Upload failure: inspect Actions logs and YouTube API quota.
