# API and Credential Setup

This project requires only the following credentials:

| GitHub Secret | Purpose | Where to obtain it |
|---|---|---|
| `GEMINI_API_KEY` | Generates the Hindi script | https://aistudio.google.com/apikey |
| `YT_CLIENT_ID` | YouTube OAuth client ID | https://console.cloud.google.com/apis/credentials |
| `YT_CLIENT_SECRET` | YouTube OAuth client secret | Same OAuth client in Google Cloud |
| `YT_REFRESH_TOKEN` | Long-lived YouTube authorization token | Generate with `get_token.py` after creating the OAuth client |

Enable **YouTube Data API v3** in the same Google Cloud project:
https://console.cloud.google.com/apis/library/youtube.googleapis.com

## Not required

- `PIXABAY_API_KEY`
- `PEXELS_API_KEY`
- Any paid video-generation API key

FFmpeg creates animated motion-graphics backgrounds locally.

## Add secrets to GitHub

Repository → Settings → Secrets and variables → Actions → New repository secret.

Create each secret using the exact uppercase name in the table. Paste the corresponding value into the Secret value field. Do not share keys in chat or commit them to source control.

## Obtain the YouTube refresh token

1. Create an OAuth client in Google Cloud, following the project's YouTube authentication setup.
2. Put the OAuth Client ID and Client Secret into `get_token.py` only in your private working copy, or use the supported Google Colab workflow described in `SETUP_GUIDE.md`.
3. Run the script and approve access using the Google account that owns the channel.
4. Copy the returned refresh token directly into the GitHub Secret `YT_REFRESH_TOKEN`.
5. Do not commit the edited `get_token.py` or expose the token.

OAuth consent-screen configuration and YouTube API access restrictions are controlled by Google and may vary by project.
