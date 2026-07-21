#!/usr/bin/env python3
"""README の定期試験カウントダウンを JST の日付で更新する。"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


EXAM_START = date(2026, 7, 28)
EXAM_END = date(2026, 7, 31)
START_MARKER = "<!-- EXAM_COUNTDOWN_START -->"
END_MARKER = "<!-- EXAM_COUNTDOWN_END -->"


def countdown_message(today: date) -> str:
    if today < EXAM_START:
        return f"定期試験開始まであと{(EXAM_START - today).days}日です。"
    if today <= EXAM_END:
        day_number = (today - EXAM_START).days + 1
        return f"本日は定期試験{day_number}日目です。"
    return "定期試験は終了しました。お疲れさまでした！"


def update_readme(readme: Path, today: date) -> None:
    text = readme.read_text(encoding="utf-8")
    replacement = (
        f"{START_MARKER}\n"
        f"**{countdown_message(today)}**\n\n"
        f"最終更新: {today.year}年{today.month}月{today.day}日（JST）\n"
        f"{END_MARKER}"
    )
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL
    )
    updated, count = pattern.subn(replacement, text)
    if count != 1:
        raise RuntimeError(f"カウントダウン領域が1つではありません: {count}個")
    readme.write_text(updated, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        help="検証用の日付（YYYY-MM-DD）。省略時は現在のJST日付を使用",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    jst_today = args.date or datetime.now(ZoneInfo("Asia/Tokyo")).date()
    update_readme(args.readme, jst_today)
