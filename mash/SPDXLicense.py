# Copyright 2025 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0

license_map = {
    'Apache 2.0': 'Apache-2.0',
    'Apache-2.0': 'Apache-2.0',
    'Apache 2.0 License': 'Apache-2.0',
    'Apache License 2.0': 'Apache-2.0',
    'BSD-3-Clause': 'BSD-3-Clause',
    'Eclipse Distribution License 1.0': 'EDL-1.0',
    'Eclipse Public License 2.0': 'EPL-2.0',
    'GNU General Public License v2.0': 'GPL-2.0-only',
    'LGPL-2.1-or-later': 'LGPL-2.1-or-later',
    'MIT': 'MIT'
}


def is_spdx_license(license_str):
    """Check if a license string is a valid SPDX identifier.

    This is a very simple check that just checks if the license string
    is in the license_map values or contains only valid characters.
    """
    is_spdx = False

    if license_str in license_map.values():
        is_spdx = True

    return is_spdx


def map_license(license_str):
    """Map a license string to an SPDX identifier.

    If the license string is not in the license_map, it is returned as-is.
    """
    license_found = ''

    if license_str in license_map.keys():
        license_found = license_map[license_str]

    return license_found
