# FromTutorialToCode

This repository is my learning workspace. It will contain many subfolders, where each subfolder represents one tutorial/course/topic I’m following and the code/examples I implement from it.

Main areas: AI/ML, DevOps, Python, and general software engineering experiments.

## YouTube → folder generator

This repo includes a small script that takes a YouTube link and creates a new subfolder (a “pull”) named after the video title, with a generated `README.md` containing the key video information.

### Usage

```bash
uv run py youtube_pull.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

By default it writes into `tutorials/` in the project root. You can change that:

```bash
uv run py youtube_pull.py "https://www.youtube.com/watch?v=VIDEO_ID" --base-dir "my_subfolder"
```
