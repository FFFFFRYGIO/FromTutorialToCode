import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL


def _slugify_folder_name(title: str, max_len: int = 80) -> str:
    s = title.strip()
    s = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", " ", s)  # Windows-illegal + control chars
    s = re.sub(r"\s+", " ", s).strip()
    s = s.rstrip(". ")  # Windows forbids trailing dot/space
    if not s:
        s = "untitled"
    if len(s) > max_len:
        s = s[:max_len].rstrip(". ")
    return s.replace(" ", "_")


def _extract_video_info(url: str) -> dict[str, Any]:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info


def _write_project_readme(out_dir: Path, info: dict[str, Any], source_url: str) -> None:
    title = info.get("title") or "Untitled"
    uploader = info.get("uploader") or info.get("channel") or info.get("uploader_id")
    channel_url = info.get("channel_url") or info.get("uploader_url")
    video_id = info.get("id")
    tags = info.get("tags") if isinstance(info.get("tags"), list) else None
    description = info.get("description") or ""

    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines: list[str] = []

    lines.append(f"# {title}")
    lines.append(
        "This folder was generated from a YouTube video and can be used as a starting point "
        "for notes, code, and exercises based on the tutorial."
    )
    lines.append("")

    lines.append("## Description")
    lines.append("")
    desc = description.strip().replace("\r\n", "\n").replace("~", "-")
    lines.append(desc if desc else "No description available.")
    lines.append("")

    lines.append("## Generated")
    lines.append("")
    lines.append(f"- **Generated at (UTC):** {generated_at}")
    lines.append(f"- **Source URL used:** {source_url}")
    lines.append(f"- **Video ID:** {video_id or 'N/A'}")
    lines.append(f"- **YouTube channel:** [{uploader}]({channel_url})")
    lines.append(f"- **Tags:** {', '.join(str(t) for t in tags) if isinstance(tags, list) else 'no tags'}")
    lines.append("")

    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Create a subfolder ("pull") from a YouTube URL with a generated README.'
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--base-dir",
        default="tutorials",
        help="Base directory under this project (default: tutorials)",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    base_dir = (project_root / args.base_dir).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    info = _extract_video_info(args.url)
    title = info.get("title") or "untitled"

    folder_name = _slugify_folder_name(str(title))
    out_dir = base_dir / folder_name
    if out_dir.exists():
        pass
        # raise FileExistsError(f"Target folder already exists: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    _write_project_readme(out_dir, info, args.url)

    print(str(out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
