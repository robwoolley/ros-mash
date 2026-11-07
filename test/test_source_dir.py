# Copyright 2026 Ahmed Adel Wafdy
# Licensed under the Apache License, Version 2.0

from mash.BitbakeRecipe import BitbakeRecipe


def make_recipe(pkg_path, yocto_release=None):
    recipe = BitbakeRecipe()
    recipe.set_pkg_path(pkg_path)
    if yocto_release:
        recipe.set_yocto_release(yocto_release)
    return recipe


def test_source_dir_defaults_to_workdir():
    recipe = make_recipe('/sub/pkg')
    assert recipe.get_source_dir() == '${WORKDIR}/git/sub/pkg'


def test_source_dir_unpackdir_after_scarthgap():
    recipe = make_recipe('/sub/pkg', 'wrynose')
    assert recipe.get_source_dir() == \
        '${UNPACKDIR}/${BB_GIT_DEFAULT_DESTSUFFIX}/sub/pkg'


def test_source_dir_unpackdir_at_repository_root():
    recipe = make_recipe('', 'wrynose')
    assert recipe.get_source_dir() == \
        '${UNPACKDIR}/${BB_GIT_DEFAULT_DESTSUFFIX}'
