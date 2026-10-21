# Copyright 2026 Ahmed Adel Wafdy
# Licensed under the Apache License, Version 2.0

from mash.BitbakeRecipe import BitbakeRecipe
from mash.verb.bitbake import BitbakeVerb


class StubDescriptor:
    """Minimal stand-in for a colcon PackageDescriptor."""

    def __init__(self, name):
        self.name = name


def test_internal_packages_include_workspace_packages():
    verb = BitbakeVerb()
    internal = verb.get_internal_packages(
        ['released_pkg'], {StubDescriptor('pkg_a'), StubDescriptor('pkg_b')})
    assert internal == {'released_pkg', 'pkg_a', 'pkg_b'}


def test_workspace_package_is_named_without_rosdep(monkeypatch):
    def fail_resolve(*args, **kwargs):
        raise AssertionError('rosdep lookup for a workspace package')

    monkeypatch.setattr(
        'mash.BitbakeRecipe.resolve_rosdep_key', fail_resolve)

    recipe = BitbakeRecipe()
    recipe.set_internal_packages({'pkg_b'})
    assert recipe.convert_to_oe_naming('pkg_b') == 'pkg-b'
    assert recipe.convert_to_oe_naming('pkg_b', True) == 'pkg-b-native'
