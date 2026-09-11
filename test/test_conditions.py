# Copyright 2026 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0

from catkin_pkg.package import InvalidPackage
from mash.PackageMetadata import PackageMetadata
from mash.verb.bitbake import BitbakeVerb
import pytest

# osqp_vendor-shaped: a <build_type> per ROS version, guarded by
# $ROS_VERSION conditions. Without a context, catkin_pkg sees both as live
# and raises InvalidPackage (issue #7).
PKG_XML_DUAL_BUILD_TYPE = """<?xml version="1.0"?>
<package format="3">
  <name>osqp_vendor</name>
  <version>0.2.0</version>
  <description>A fake package for testing.</description>
  <maintainer email="maintainer@example.com">Test Maintainer</maintainer>
  <license>Apache-2.0</license>
  <buildtool_depend condition="$ROS_VERSION == 1">catkin</buildtool_depend>
  <buildtool_depend condition="$ROS_VERSION == 2">
    ament_cmake</buildtool_depend>
  <buildtool_depend>git</buildtool_depend>
  <export>
    <build_type condition="$ROS_VERSION == 1">catkin</build_type>
    <build_type condition="$ROS_VERSION == 2">ament_cmake</build_type>
  </export>
</package>
"""

# octomap-shaped: a single dependency only needed on ROS 1.
PKG_XML_ROS_VERSION_DEPEND = """<?xml version="1.0"?>
<package format="3">
  <name>octomap</name>
  <version>1.10.0</version>
  <description>A fake package for testing.</description>
  <maintainer email="maintainer@example.com">Test Maintainer</maintainer>
  <license>BSD</license>
  <exec_depend condition="$ROS_VERSION == 1">catkin</exec_depend>
  <buildtool_depend>cmake</buildtool_depend>
  <export>
    <build_type>cmake</build_type>
  </export>
</package>
"""

# behaviortree_cpp-shaped: an or-condition keyed on $ROS_DISTRO.
PKG_XML_DISTRO_OR_CONDITION = """<?xml version="1.0"?>
<package format="3">
  <name>behaviortree_cpp</name>
  <version>4.10.0</version>
  <description>A fake package for testing.</description>
  <maintainer email="maintainer@example.com">Test Maintainer</maintainer>
  <license>MIT</license>
  <depend condition="$ROS_DISTRO == humble or $ROS_DISTRO == jazzy \
or $ROS_DISTRO == kilted">tinyxml2_vendor</depend>
  <depend>tinyxml2</depend>
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
"""


class StubIndex:
    """Minimal stand-in for rosdistro.Index; no network access involved."""

    def __init__(self, distributions):
        self.distributions = distributions


def _context(ros_version, ros_distro='rolling', ros_python_version=3):
    return {
        'ROS_OS_OVERRIDE': 'openembedded',
        'ROS_DISTRO': ros_distro,
        'ROS_VERSION': str(ros_version),
        'ROS_PYTHON_VERSION': str(ros_python_version),
    }


def test_dual_build_type_resolves_for_ros2_without_raising():
    pkg = PackageMetadata(PKG_XML_DUAL_BUILD_TYPE, _context(2))
    assert pkg.build_type == 'ament_cmake'
    assert [str(d) for d in pkg.buildtool_depends] == ['ament_cmake', 'git']
    assert pkg.excluded_depends == ['catkin']


def test_dual_build_type_resolves_for_ros1_without_raising():
    pkg = PackageMetadata(PKG_XML_DUAL_BUILD_TYPE, _context(1))
    assert pkg.build_type == 'catkin'
    assert [str(d) for d in pkg.buildtool_depends] == ['catkin', 'git']
    assert pkg.excluded_depends == ['ament_cmake']


def test_dual_build_type_raises_without_a_context():
    with pytest.raises(InvalidPackage):
        PackageMetadata(PKG_XML_DUAL_BUILD_TYPE)


def test_ros_version_conditional_depend_excluded_for_ros2():
    pkg = PackageMetadata(PKG_XML_ROS_VERSION_DEPEND, _context(2))
    assert 'catkin' not in [str(d) for d in pkg.exec_depends]
    assert pkg.excluded_depends == ['catkin']


def test_ros_version_conditional_depend_included_for_ros1():
    pkg = PackageMetadata(PKG_XML_ROS_VERSION_DEPEND, _context(1))
    assert 'catkin' in [str(d) for d in pkg.exec_depends]
    assert pkg.excluded_depends == []


def test_distro_or_condition_kept_on_matching_distro():
    pkg = PackageMetadata(
        PKG_XML_DISTRO_OR_CONDITION, _context(2, ros_distro='humble'))
    assert 'tinyxml2_vendor' in [str(d) for d in pkg.build_depends]
    assert pkg.excluded_depends == []


def test_distro_or_condition_excluded_on_other_distro():
    pkg = PackageMetadata(
        PKG_XML_DISTRO_OR_CONDITION, _context(2, ros_distro='rolling'))
    names = [str(d) for d in pkg.build_depends]
    assert 'tinyxml2_vendor' not in names
    assert 'tinyxml2' in names
    assert pkg.excluded_depends == ['tinyxml2_vendor']


def test_no_context_keeps_all_dependencies():
    # Guards the `evaluated_condition is not False` trap: without a
    # context, evaluated_condition stays None on every dependency, and
    # nothing should be dropped even though the raw XML has a condition.
    pkg = PackageMetadata(PKG_XML_ROS_VERSION_DEPEND)
    assert 'catkin' in [str(d) for d in pkg.exec_depends]
    assert pkg.excluded_depends == []


def test_get_ros_python_version_from_index():
    verb = BitbakeVerb()
    index = StubIndex({'melodic': {'python_version': 2}})
    assert verb.get_ros_python_version(index, 'melodic') == 2


def test_get_ros_python_version_defaults_to_3():
    verb = BitbakeVerb()
    index = StubIndex({})
    assert verb.get_ros_python_version(index, 'rolling') == 3


def test_get_condition_context():
    verb = BitbakeVerb()
    index = StubIndex(
        {'humble': {'distribution_type': 'ros2', 'python_version': 3}})
    assert verb.get_condition_context(index, 'humble') == {
        'ROS_OS_OVERRIDE': 'openembedded',
        'ROS_DISTRO': 'humble',
        'ROS_VERSION': '2',
        'ROS_PYTHON_VERSION': '3',
    }
