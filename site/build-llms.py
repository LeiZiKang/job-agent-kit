#!/usr/bin/env python3
"""Build the public documentation bundle, using only this fixed source allowlist.

Run from any directory with Python 3.9+. No network, third-party packages,
timestamps, personal files, or generated output are used as inputs.
"""

from pathlib import Path
import re
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parent.parent
SOURCES = (
    "README.md",
    "CHANGELOG.md",
    "docs/architecture.md",
    "docs/lessons.md",
    "docs/strategy-patterns.md",
)
REPO = "https://github.com/LeiZiKang/job-agent-kit/blob/main/"


def main():
    sections = [
        "# job-agent-kit — full documentation\n\n"
        "> Public repository documentation. Regenerate with python3 site/build-llms.py.\n\n"
        "Source files are reproduced below in order. Relative Markdown links "
        "are expanded to their public repository URLs.\n"
    ]
    for name in SOURCES:
        content = (ROOT / name).read_text(encoding="utf-8").rstrip()
        content = re.sub(
            r"\]\(([^\s)]+)\)",
            lambda match: "](" + urljoin(REPO + name, match.group(1)) + ")",
            content,
        )
        sections.append(f"\n---\n\nSource: [{name}]({REPO}{name})\n\n{content}\n")
    output = ROOT / "site/llms-full.txt"
    output.write_text("".join(sections), encoding="utf-8")
    print(f"Generated site/llms-full.txt from {len(SOURCES)} sources ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
