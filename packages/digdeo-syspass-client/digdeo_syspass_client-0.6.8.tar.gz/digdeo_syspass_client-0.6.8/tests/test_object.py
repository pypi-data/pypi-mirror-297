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
from syspassclient import Object


class TestObject(unittest.TestCase):
    def test_verbose(self):
        my_object = Object()
        my_object.verbose = False
        self.assertFalse(my_object.verbose)
        my_object.verbose = True
        self.assertTrue(my_object.verbose)
        self.assertRaises(TypeError, setattr, my_object, 'verbose', 42)

    def test_verbose_level(self):
        my_object = Object()
        my_object.verbose_level = 0
        self.assertEqual(0, my_object.verbose_level)
        my_object.verbose_level = 42
        self.assertEqual(42, my_object.verbose_level)
        my_object.verbose_level = 0
        self.assertEqual(0, my_object.verbose_level)
        self.assertRaises(TypeError, setattr, my_object, 'verbose_level', 'Hello')

    def test_debug(self):
        my_object = Object()
        my_object.debug = False
        self.assertFalse(my_object.debug)
        my_object.debug = True
        self.assertTrue(my_object.debug)
        my_object.debug = False
        self.assertFalse(my_object.debug)
        self.assertRaises(TypeError, setattr, my_object, 'debug', 42)

    def test_debug_level(self):
        my_object = Object()
        my_object.debug_level = 0
        self.assertEqual(0, my_object.debug_level)
        my_object.debug_level = 42
        self.assertEqual(42, my_object.debug_level)
        my_object.debug_level = 0
        self.assertEqual(0, my_object.debug_level)
        self.assertRaises(TypeError, setattr, my_object, 'debug_level', 'Hello')


if __name__ == '__main__':
    unittest.main()
