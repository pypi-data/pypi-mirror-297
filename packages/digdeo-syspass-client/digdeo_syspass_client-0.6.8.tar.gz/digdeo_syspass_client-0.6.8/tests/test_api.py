#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of SysPass Client
#
# Copyright (C) 2020  DigDeo SAS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import unittest
import os
import syspassclient


class TestSyspassApi(unittest.TestCase):

    def test_api_version(self):
        api = syspassclient.Api()

        os.environ['syspass_api_version'] = '3.1'

        self.assertTrue(isinstance(api.api_version, str))
        self.assertTrue(3.0 <= float(api.api_version))

        self.assertIsNotNone(api.api_version)
        self.assertTrue(isinstance(api.api_version, str))

        api.api_version = "3.0"
        self.assertEqual(api.api_version, "3.1")
        del os.environ['syspass_api_version']
        self.assertEqual(api.api_version, "3.0")

        api.api_version = "3.0"
        self.assertEqual(api.api_version, "3.0")

        api.api_version = None
        self.assertEqual(api.api_version, "3.1")

        self.assertRaises(TypeError, setattr, api, 'api_version', 3.1)

    def test_api_url(self):
        api = syspassclient.Api()
        os.environ['syspass_api_url'] = 'Hello.4242'

        self.assertEqual(api.api_url, 'Hello.4242')

        del os.environ['syspass_api_url']

        api.api_url = 'Hello.42'
        self.assertEqual(api.api_url, 'Hello.42')

        self.assertRaises(TypeError, setattr, api, 'api_url', 42)

    def test_api_data(self):
        api = syspassclient.Api()
        api.api_read_file()
        self.assertIsNotNone(api.api_data)
        self.assertTrue("account/search" in api.api_data)
        self.assertTrue("account/viewPass" in api.api_data)

        dict_to_test = {"account/search": {}, "account/viewPass": {}}
        self.assertNotEqual(dict_to_test, api.api_data)

        api.api_data = dict_to_test
        self.assertEqual(dict_to_test, api.api_data)

    def test_api_extension(self):
        api = syspassclient.Api()
        self.assertEqual(api.api_filename_ext, ".yaml")

        api.api_filename_ext = ".42"
        self.assertIsNotNone(api.api_filename_ext)
        self.assertEqual(api.api_filename_ext, ".42")

        api.api_filename_ext = None
        self.assertEqual(api.api_filename_ext, ".yaml")

    def test_api_filename_extension(self):
        api = syspassclient.Api()
        self.assertTrue(isinstance(api.api_filename_ext, str))
        self.assertEqual(".yaml", api.api_filename_ext)

        api.api_filename_ext = ".42"
        self.assertEqual(".42", api.api_filename_ext)

        api.api_filename_ext = None
        self.assertEqual(".yaml", api.api_filename_ext)

        self.assertRaises(TypeError, setattr, api, "api_filename_ext", 42)

    def test_api_directory(self):
        api = syspassclient.Api()
        self.assertTrue(os.path.exists(api.api_directory))
        api.api_directory = "Hello"
        self.assertEqual(api.api_directory, "Hello")
        api.api_directory = None
        self.assertTrue(os.path.exists(api.api_directory))
        self.assertRaises(TypeError, setattr, api, "api_directory", 42)

    def test_api_filename(self):
        api = syspassclient.Api()
        self.assertTrue(isinstance(api.api_filename, str))
        self.assertTrue(api.api_filename, api.api_version + api.api_filename_ext)

        api.api_version = '3.0'
        self.assertTrue(api.api_filename, api.api_version + api.api_filename_ext)
        api.api_version = '3.1'
        self.assertTrue(api.api_filename, api.api_version + api.api_filename_ext)

    def test_api_file(self):
        api = syspassclient.Api()
        self.assertTrue(isinstance(api.api_file, str))
        self.assertTrue(api.api_file, os.path.join(api.api_directory, api.api_filename))

    def test_read(self):
        api = syspassclient.Api()
        api.debug = True
        api.debug_level = 3
        api.verbose = True
        api.verbose_level = 3
        api.api_read_file()

        old_api_data = api.api_data
        api.api_read_file()
        self.assertEqual(old_api_data, api.api_data)


if __name__ == '__main__':
    unittest.main()
