# API Setup

## Required GitHub Actions secrets

Open **Repository → Settings → Secrets and variables → Actions → New repository secret**. Create these five secrets exactly as named:

| Secret name | Value |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `PIXABAY_API_KEY` | Pixabay API key (primary stock-video source) |
| `YT_CLIENT_ID` | YouTube OAuth client ID |
| `YT_CLIENT_SECRET` | YouTube OAuth client secret |
| `YT_REFRESH_TOKEN` | YouTube OAuth refresh token |

`PEXELS_API_KEY` is optional. If you already have an older Pexels key, you may add it as an additional secret. It is used only when Pixabay cannot provide a suitable clip. A new Pexels key is not required.

## Get the Pixabay API key

1. Sign in to Pixabay or create an account.
2. Open the [official Pixabay API documentation](https://pixabay.com/api/docs/).
3. Follow Pixabay's account/API instructions to obtain your key.
4. Save it in GitHub as `PIXABAY_API_KEY`.

## First test (recommended)

1. Open **Actions → Daily Short → Run workflow**.
2. Keep `dry_run` set to `1`.
3. Run the workflow and wait for it to finish.
4. Open the completed run and download the `short-video` artifact.
5. Check `final.mp4`. Only after reviewing it, run again with `dry_run` set to `0` to upload.

Uploads default to **Private**. Do not change the repository variable `PRIVACY` to `public` until you have tested the workflow and reviewed the generated content.

Never paste API keys or OAuth tokens into chat, source files, or public commits. Store them only in GitHub Actions Secrets.
