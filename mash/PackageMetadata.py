# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib

from catkin_pkg.package import parse_package_string


class PackageMetadata:
    """Package metadata parsed from a ROS package manifest."""

    def __init__(self, pkg_xml, evaluate_condition_context=None):
        """Parse `pkg_xml` and populate the recipe-relevant fields."""
        # Set defaults
        self.upstream_email = None
        self.upstream_name = None
        self.homepage = 'https://wiki.ros.org'

        pkg = parse_package_string(pkg_xml)

        if evaluate_condition_context:
            pkg.evaluate_conditions(evaluate_condition_context)

        self.name = pkg.name
        self.version = pkg.version
        self.description = pkg.description
        self.upstream_license = pkg.licenses

        self.license_line = ''
        self.license_md5 = ''

        i = 1
        for line in pkg_xml.splitlines():
            if 'license' in line:
                self.license_line = str(i)
                md5 = hashlib.md5()
                md5.update((line + '\n').encode('utf-8'))
                self.license_md5 = md5.hexdigest()
                break
            i = i + 1

        if 'website' in [url.type for url in pkg.urls]:
            self.homepage = [
                url.url for url in pkg.urls if url.type == 'website'
            ][0]
        elif len(pkg.urls) > 0:
            self.homepage = [
                url.url for url in pkg.urls
            ][0]

        self.longdescription = pkg.description

        self.upstream_email = [
            author.email for author in pkg.maintainers
        ][0]
        self.upstream_name = [
            author.name for author in pkg.maintainers
        ][0]
        self.author_email = [
            author.email for author in pkg.authors
        ][0] if pkg.authors else ''
        self.author_name = [
            author.name for author in pkg.authors
        ][0] if pkg.authors else ''
        self.member_of_groups = [
            group.name for group in pkg.member_of_groups
        ]
        self.build_type = pkg.get_build_type()

        self.build_depends = pkg.build_depends
        self.buildtool_depends = pkg.buildtool_depends
        self.build_export_depends = pkg.build_export_depends
        self.buildtool_export_depends = pkg.buildtool_export_depends
        self.exec_depends = pkg.exec_depends
        self.run_depends = pkg.run_depends
        self.test_depends = pkg.test_depends
        self.doc_depends = pkg.doc_depends
