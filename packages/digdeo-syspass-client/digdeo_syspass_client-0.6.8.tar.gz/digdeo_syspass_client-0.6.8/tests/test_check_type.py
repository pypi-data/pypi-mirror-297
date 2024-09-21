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
from syspassclient import CheckType


class TestCheckType(unittest.TestCase):
    def test_is_str_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_str_or_raise, None)
        self.assertIsNone(check.is_str_or_raise("Hello"))

    def test_is_int_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_int_or_raise, None)
        self.assertIsNone(check.is_int_or_raise(42))

    def test_is_float_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_float_or_raise, None)
        self.assertIsNone(check.is_float_or_raise(42.24))

    def test_is_list_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_list_or_raise, None)
        self.assertIsNone(check.is_list_or_raise([42, 42]))

    def test_is_dict_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_dict_or_raise, None)
        self.assertIsNone(check.is_dict_or_raise({"anwser": 42}))

    def test_is_bool_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_bool_or_raise, None)
        self.assertIsNone(check.is_bool_or_raise(True))
        self.assertIsNone(check.is_bool_or_raise(False))

    def test_is_url_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_url_or_raise, None)
        self.assertRaises(ValueError, check.is_url_or_raise, "42")
        self.assertIsNone(check.is_url_or_raise("http://127.0.0.1"))

    def test_is_ascii_or_raise(self):
        check = CheckType()
        self.assertRaises(TypeError, check.is_ascii_or_raise, None)
        self.assertRaises(ValueError, check.is_ascii_or_raise, "\xe2")
        self.assertIsNone(check.is_ascii_or_raise("coucou"))


if __name__ == "__main__":
    unittest.main()
