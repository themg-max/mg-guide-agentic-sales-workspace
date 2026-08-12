"""Stdout-only CLI for rendering NW-006 card fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .mapper import map_packet_to_card
from .render_html import render_card_html
from .render_text import render_card_text


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render MG Guide meeting follow-up card")
    parser.add_argument("--packet", required=True, help="Path to meeting_follow_up_packet_v1 JSON")
    parser.add_argument("--format", choices=("text", "html"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    packet_path = Path(args.packet)
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    card = map_packet_to_card(packet)
    if args.format == "html":
        print(render_card_html(card))
    else:
        print(render_card_text(card))
    return 0

