# TAKNA TECHNOLOGY – Automated Hindi Mystery & History Shorts

A GitHub Actions based Shorts production pipeline. Gemini writes a Hindi historical/mystery script; Edge TTS narrates it; a recurring procedural 2D cartoon host and story-aware backgrounds are rendered with Pillow + FFmpeg; subtitles and background audio are added; YouTube metadata is prepared and the video can be uploaded.

## Features
- Hindi mystery/history Shorts with a strong opening hook and story ending.
- Recurring cartoon host in every scene, with a consistent simple face design and story-role clothing colors.
- Story-aware scene environments (temple, fort, forest, desert, water, archaeology, space, general history).
- TAKNA TECHNOLOGY transparent logo appears subtly in every scene.
- Hindi voice narration, Hindi captions, background music / generated ambient bed.
- SEO title, description, tags, hashtags generated with the script.
- Topic history avoids repeating recent topics.
- Daily GitHub Actions automation plus manual run for an additional video.
- FFmpeg/Pillow rendering; no Pixabay/Pexels or paid video-generation API required.

## Important visual limitation
The host is a procedural 2D cartoon prototype with simple body movement and arm gestures. It is not a photorealistic or fully generative animated film; accurate lip-sync, complex acting, and detailed unique animation for every story beat are not included. Scene selection is based on broad story keywords. Always review the generated video before making it public.

## Required GitHub Actions Secrets
- `GEMINI_API_KEY`
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

No Pixabay or Pexels credentials are required.

## Safe first run
1. Add all four secrets in Settings → Secrets and variables → Actions.
2. Open Actions → Daily Short → Run workflow.
3. Keep `dry_run=1`.
4. Download the `short-video` artifact and review `final.mp4` and `script.json`.
5. When satisfied, run manually with `dry_run=0` to upload. Default privacy is `private`.

## Daily schedule
The workflow is set to 17:00 India Standard Time (11:30 UTC), once per day. Since this channel currently has no useful audience analytics, 17:00 IST is only a starting test time, not a proven peak time. Review YouTube Studio → Analytics → Audience after enough uploads and adjust the cron schedule. A second video can be generated with a separate manual run.

## Cost and limits
- FFmpeg and Pillow are open-source and run on the GitHub Actions runner.
- Gemini usage depends on the current Google AI Studio model availability and account quota.
- Edge TTS is an online community client; availability and service terms may change.
- GitHub Actions minutes and storage are subject to the account's plan limits.
- Therefore the workflow avoids a paid video-generation API, but no one can guarantee unlimited free operation or unlimited API quotas.

## Project map
- `make_short.py`: script, TTS, animation render calls, captions, assembly, SEO and upload.
- `story_animation.py`: recurring host, backgrounds, scene animation and logo.
- `assets/tenaga_technology_logo_transparent.png`: transparent channel logo.
- `.github/workflows/daily.yml`: daily automation and manual run.
- `get_token.py`: one-time YouTube OAuth refresh token helper.
- `topics_done.json`: used-topic history.
- `music/`: optional MP3 music files.
- `SETUP_GUIDE.md`: full setup.
- `API_SETUP.md`: credentials.

Never commit API keys, OAuth tokens, or secrets into source files.
