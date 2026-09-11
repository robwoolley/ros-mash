# Copyright 2026 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0

from mash.BitbakeRecipe import BitbakeRecipe
from mash.PackageMetadata import PackageMetadata
from mash.verb.bitbake import BitbakeVerb

# A package.xml with no <build_type> export and no dependencies, so
# import_package() never needs to resolve a rosdep key over the network.
# catkin_pkg reports its build_type as 'catkin' in this case, which is the
# RSL scenario from issue #8.
PKG_XML_NO_BUILD_TYPE = """<?xml version="1.0"?>
<package format="2">
  <name>fake_pkg</name>
  <version>1.2.3</version>
  <description>A fake package for testing.</description>
  <maintainer email="maintainer@example.com">Test Maintainer</maintainer>
  <license>Apache-2.0</license>
</package>
"""

PKG_XML_AMENT_CMAKE = """<?xml version="1.0"?>
<package format="2">
  <name>fake_pkg</name>
  <version>1.2.3</version>
  <description>A fake package for testing.</description>
  <maintainer email="maintainer@example.com">Test Maintainer</maintainer>
  <license>Apache-2.0</license>
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
"""


class StubIndex:
    """Minimal stand-in for rosdistro.Index; no network access involved."""

    def __init__(self, distributions):
        self.distributions = distributions


# resolve_build_type() cannot distinguish an unspecified build_type from an
# explicit <build_type>catkin</build_type>: catkin_pkg reports both as
# 'catkin'. Both are rewritten identically for ROS 2, so one case covers both.
def test_resolve_build_type_rewrites_catkin_for_ros2():
    recipe = BitbakeRecipe()
    recipe.name = 'fake_pkg'
    recipe.set_ros_version(2)
    assert recipe.resolve_build_type('catkin') == 'ament_cmake'


def test_resolve_build_type_leaves_catkin_alone_for_ros1():
    recipe = BitbakeRecipe()
    recipe.name = 'fake_pkg'
    recipe.set_ros_version(1)
    assert recipe.resolve_build_type('catkin') == 'catkin'


def test_resolve_build_type_leaves_other_types_alone():
    recipe = BitbakeRecipe()
    recipe.name = 'fake_pkg'
    recipe.set_ros_version(2)
    assert recipe.resolve_build_type('ament_python') == 'ament_python'


def test_get_ros_version_ros1_distro():
    verb = BitbakeVerb()
    index = StubIndex({'noetic': {'distribution_type': 'ros1'}})
    assert verb.get_ros_version(index, 'noetic') == 1


def test_get_ros_version_ros2_distro():
    verb = BitbakeVerb()
    index = StubIndex({'humble': {'distribution_type': 'ros2'}})
    assert verb.get_ros_version(index, 'humble') == 2


def test_get_ros_version_defaults_to_ros2_when_unknown():
    verb = BitbakeVerb()
    index = StubIndex({})
    assert verb.get_ros_version(index, 'rolling') == 2


def test_import_package_without_build_type_becomes_ament_cmake():
    pkg = PackageMetadata(PKG_XML_NO_BUILD_TYPE)
    recipe = BitbakeRecipe()
    recipe.set_ros_version(2)
    recipe.import_package(pkg)
    assert recipe.build_type == 'ament_cmake'


def test_import_package_with_explicit_build_type_is_unchanged():
    pkg = PackageMetadata(PKG_XML_AMENT_CMAKE)
    recipe = BitbakeRecipe()
    recipe.set_ros_version(2)
    recipe.import_package(pkg)
    assert recipe.build_type == 'ament_cmake'
