# Complete Setup Guide

## 1. Requirements

- A GitHub account and a repository for this project.
- A Google AI Studio API key for Gemini.
- A Pixabay API key for stock video.
- A Google Cloud OAuth client configured for YouTube Data API v3.
- A YouTube refresh token for the channel that will receive uploads.

No Android APK, phone installation, paid server, or local computer is required. GitHub Actions runs the Python project in the cloud.

## 2. Upload the project to GitHub

1. Download and extract the complete project ZIP.
2. Open your GitHub repository.
3. Upload the contents of the `short-bot` folder to the repository root.
4. Ensure `.github/workflows/daily.yml` remains at that exact path.
5. Commit the files to the `main` branch.

## 3. Create API credentials

### Gemini

Create an API key in Google AI Studio. Store it as `GEMINI_API_KEY`.

### Pixabay

Use the official [Pixabay API documentation](https://pixabay.com/api/docs/) and follow its current instructions to obtain an API key. Store it as `PIXABAY_API_KEY`.

### YouTube OAuth

1. Open Google Cloud Console and select or create a project.
2. Enable **YouTube Data API v3**.
3. Configure the OAuth consent screen.
4. Create an OAuth client and note its Client ID and Client Secret.
5. Use `get_token.py` in Google Colab after inserting the OAuth client credentials into the two placeholder values.
6. Follow the displayed verification URL, enter the device code, sign in to the Google account that owns the target channel, and approve access.
7. Copy the refresh token shown by the script.

If Google does not offer the device authorization flow for your OAuth client configuration, use a supported OAuth flow and obtain a refresh token with the same YouTube scope. Do not expose the token.

## 4. Add GitHub Actions secrets

Go to **Repository → Settings → Secrets and variables → Actions**. Add these repository secrets:

- `GEMINI_API_KEY`
- `PIXABAY_API_KEY`
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

Optionally add `PEXELS_API_KEY` only if you already have a working older Pexels key. It is a fallback; a new Pexels key is not necessary.

## 5. Run a safe test

1. Open the repository's **Actions** tab.
2. Select **Daily Short**.
3. Click **Run workflow**.
4. Keep `dry_run` set to `1`.
5. Start the workflow and wait for completion.
6. Open the run and download the `short-video` artifact.
7. Check `final.mp4` and `script.json`.

A dry run generates the video but skips YouTube upload.

## 6. Upload after review

When the video looks correct, run the workflow again and set `dry_run` to `0`. The default upload privacy is `private`. Review the uploaded video in YouTube Studio before changing its visibility.

The scheduled workflow runs daily at 5:00 PM India Standard Time and uploads privately by default.

## 7. Optional background music

Place royalty-free or properly licensed MP3 files in the `music/` directory. If no MP3 file exists, the bot creates a subtle synthetic background drone. Only use music you have the right to publish.

## 8. Troubleshooting

- **Missing secret:** Check the spelling of every secret name and ensure it is saved under Actions secrets.
- **Pixabay returns no clips:** Check the key, API access, search terms, and Pixabay availability. The video builder can use a fallback background if no stock clip is found.
- **Gemini error:** Verify the key, API access, quota, and model availability.
- **YouTube OAuth error:** Confirm the OAuth client ID, client secret, refresh token, consent configuration, and YouTube Data API v3 access.
- **FFmpeg error:** Review the failed GitHub Actions log. The workflow installs FFmpeg automatically.
- **No artifact:** The video generation step may have failed before `final.mp4` was created. Read the job log from the first error.

## 9. Security and publishing checklist

- Never commit API keys, OAuth secrets, or refresh tokens.
- Never paste credentials into chat or screenshots.
- Keep uploads private until manually reviewed.
- Fact-check historical claims, dates, names, and legends before publishing.
- Use stock footage and music only in accordance with their license terms.

## 10. Language behavior

The technical instructions, code comments, workflow labels, and demonstration messages in this package are in English. The actual Shorts content (Hindi narration, title, on-screen captions, description, and hashtags) remains in Hindi by design.
