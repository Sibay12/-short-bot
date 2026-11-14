# API and Credential Setup

| GitHub Secret | Purpose | Source |
|---|---|---|
| `GEMINI_API_KEY` | Hindi story/script generation | https://aistudio.google.com/apikey |
| `YT_CLIENT_ID` | YouTube OAuth client ID | https://console.cloud.google.com/apis/credentials |
| `YT_CLIENT_SECRET` | YouTube OAuth client secret | Same OAuth client |
| `YT_REFRESH_TOKEN` | Channel authorization for automated uploads | Generate with `get_token.py` after OAuth approval |

Enable YouTube Data API v3: https://console.cloud.google.com/apis/library/youtube.googleapis.com

## Not required
- `PIXABAY_API_KEY`
- `PEXELS_API_KEY`
- Paid video-generation API key

## Important
OAuth authorization flow support depends on Google's current OAuth client rules. The included helper uses Google's device-code endpoint. If Google rejects the OAuth client type or flow, use a currently supported installed-app authorization flow. Do not paste credentials into chat or commit them to GitHub.

Add secrets in GitHub: Repository → Settings → Secrets and variables → Actions → New repository secret.

## Current free-tier model defaults
The project defaults to `gemini-3.8-flash` and falls back to `gemini-3.5-flash-lite`. Google model availability and quotas can change; if needed, set the GitHub repository variable `GEMINI_MODEL` to a currently available free-tier text model. Check Google AI Studio before changing it.
