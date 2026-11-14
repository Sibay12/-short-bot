# Visual engine notes

For every scene, the story generator is asked for:
- `visual`: the concrete scene description
- `visual_query`: a specific English search phrase for the exact place/event/object
- `host_role`: the recurring host's role in that scene
- `host_action`: the action he performs

The renderer fetches a relevant Wikimedia Commons image where possible, adds cinematic pan/zoom and a consistent illustrated host with story-specific costume/prop/action, then encodes the scene with FFmpeg. It writes author/license/page metadata to `work/visual_sources.txt`.

If no suitable image is found, the renderer uses a generated scene background rather than silently reusing the reference screenshots. No screenshot supplied by the user is used as video footage.
