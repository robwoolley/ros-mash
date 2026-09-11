# Copyright 2026 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0

"""Release-consistency check.

Assert that the release tag, the package `__version__`, and the newest dated
`CHANGELOG.md` version all agree - so no tag ships without a matching, dated
changelog entry. Used as the first guard in the release workflow:

    python scripts/release_consistency.py "$GITHUB_REF_NAME"

Exit 0 when consistent, 1 (with messages on stderr) when they diverge. Stdlib
only; reads files by hand so it needs nothing installed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANGELOG = REPO / 'CHANGELOG.md'
INIT = REPO / 'mash' / '__init__.py'

# `## [X.Y.Z] - 2026-07-04` (em-dash or hyphen); [Unreleased] has no date -> skipped.
_DATED_VERSION = re.compile(
    r'^## \[(\d+\.\d+\.\d+[^\]]*)\]\s+[—-]\s+\d{4}-\d{2}-\d{2}', re.M)
_VERSION_ASSIGN = re.compile(r"^__version__\s*=\s*'([^']+)'", re.M)


def changelog_version(text: str | None = None) -> str:
    """The newest dated version in the CHANGELOG (skips `[Unreleased]`)."""
    if text is None:
        text = CHANGELOG.read_text(encoding='utf-8')
    match = _DATED_VERSION.search(text)
    if match is None:
        raise ValueError(
            'no dated version heading (## [X.Y.Z] - DATE) in CHANGELOG.md')
    return match.group(1)


def package_version(text: str | None = None) -> str:
    """The `__version__` string from `mash/__init__.py` (read, not imported)."""
    if text is None:
        text = INIT.read_text(encoding='utf-8')
    match = _VERSION_ASSIGN.search(text)
    if match is None:
        raise ValueError("no __version__ assignment in mash/__init__.py")
    return match.group(1)


def check(tag: str | None = None) -> list:
    """Return mismatch messages (empty list = consistent).

    Always compares `__version__` against the newest CHANGELOG version; when a
    `tag` is given it must also equal `__version__` (a leading `v` is stripped).
    """
    pkg = package_version()
    changelog = changelog_version()
    errors = []
    if pkg != changelog:
        errors.append(
            f'__version__ {pkg!r} != newest CHANGELOG version {changelog!r}')
    if tag is not None:
        normalized = tag[1:] if tag.startswith('v') else tag
        if normalized != pkg:
            errors.append(f'tag {tag!r} (-> {normalized!r}) != __version__ {pkg!r}')
    return errors


def main(argv: list | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    tag = args[0] if args else None
    errors = check(tag)
    if errors:
        for error in errors:
            print(f'release-consistency: {error}', file=sys.stderr)
        return 1
    print(f'release-consistency: OK ({package_version()})')
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
