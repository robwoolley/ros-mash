# Copyright 2026 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0

"""Print one version's CHANGELOG section.

Used by the release workflow to build GitHub Release notes from the CHANGELOG:

    python scripts/changelog_section.py "$GITHUB_REF_NAME" > RELEASE_NOTES.md

Extracts the block under `## [X.Y.Z] - DATE` up to (but not including) the next
`## ` heading or the trailing link-reference definitions. Stdlib only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANGELOG = REPO / 'CHANGELOG.md'


def changelog_section(version: str, text: str | None = None) -> str:
    """Return the CHANGELOG block for `version` (a leading `v` is stripped)."""
    version = version[1:] if version.startswith('v') else version
    if text is None:
        text = CHANGELOG.read_text(encoding='utf-8')

    heading = re.compile(rf'^## \[{re.escape(version)}\][^\n]*$', re.M)
    start = heading.search(text)
    if start is None:
        raise ValueError(f'no CHANGELOG section for version {version!r}')

    lines = text[start.start():].splitlines()
    body = [lines[0]]  # the heading itself
    for line in lines[1:]:
        # stop at the next version heading or the link-reference block
        if line.startswith('## ') or re.match(r'^\[[^\]]+\]:\s', line):
            break
        body.append(line)
    return '\n'.join(body).strip() + '\n'


def main(argv: list | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print('usage: changelog_section.py <version|vX.Y.Z>', file=sys.stderr)
        return 2
    try:
        sys.stdout.write(changelog_section(args[0]))
    except ValueError as exc:
        print(f'changelog_section: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
