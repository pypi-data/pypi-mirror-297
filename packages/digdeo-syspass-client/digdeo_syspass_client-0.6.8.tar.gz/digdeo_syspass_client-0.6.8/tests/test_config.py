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
from syspassclient import Config

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class TestConfig(unittest.TestCase):
    def test_use_by_lookup(self):
        config_obj = Config()
        config_obj.verbose = True
        config_obj.verbose_level = 3
        config_obj.debug = True
        config_obj.debug_level = 3
        config_obj.use_by_lookup = True
        self.assertTrue(config_obj.use_by_lookup)
        config_obj.config_read_file()

        config_obj.use_by_lookup = None
        self.assertFalse(config_obj.use_by_lookup)
        config_obj.config_read_file()

        self.assertRaises(TypeError, setattr, config_obj, 'use_by_lookup', 'Hello.42')

    def test_config_read_file(self):
        config_obj = Config()
        config_obj.use_by_lookup = False
        config_obj.verbose = False
        config_obj.verbose_level = 0
        config_obj.debug = False
        config_obj.debug_level = 0
        # config_obj.api_url = 'https://prepsyspass.ddprep.digdeo.net/api.php'
        # config_obj.api_version = '3.1'
        old_data = config_obj.data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_dir, 'config/config.yml')
        config_obj.config_read_file(config_file=config_file)

        config_file = os.path.join(current_dir, 'bad_config_1.yml')
        try:
            config_obj.config_read_file(config_file=config_file)
        except AttributeError:
            pass
        self.assertRaises(AttributeError, config_obj.config_read_file, config_file=config_file)

        config_file = os.path.join(current_dir, 'bad_config_2.yml')
        try:
            config_obj.config_read_file(config_file=config_file)
        except ImportError:
            pass
        self.assertRaises(ImportError, config_obj.config_read_file, config_file=config_file)

        config_file = os.path.join(current_dir, 'bad_config_3.yml')
        config_obj.config_read_file(config_file=config_file)

        self.assertTrue(config_obj.debug)
        self.assertFalse(config_obj.verbose)
        self.assertEqual(3, config_obj.debug_level)
        self.assertEqual(0, config_obj.verbose_level)

        config_obj.config_read_file(config_file=config_file)
        config_obj.debug = False
        config_obj.verbose = False
        config_obj.debug_level = 2
        config_obj.verbose_level = 2

        self.assertFalse(config_obj.debug)
        self.assertFalse(config_obj.verbose)
        self.assertEqual(2, config_obj.debug_level)
        self.assertEqual(2, config_obj.verbose_level)

        config_obj.config_read_file()
        config_obj.data = old_data

        config_obj.use_by_lookup = True
        config_obj.api_url = None
        config_obj.api_version = None
        config_obj.authToken = None
        config_obj.tokenPass = None
        config_obj.debug = True
        config_obj.debug_level = 3
        config_obj.verbose = True
        config_obj.verbose_level = 3

        config_obj.config_read_file()

        config_file = os.path.join(current_dir, 'i_do_not_exist.yml')

        config_obj.config_read_file(config_file=config_file)
        config_obj.debug = True
        config_obj.debug_level = 3
        config_obj.display_resume()

    def test_authToken(self):
        config_obj = Config()
        config_obj.use_by_lookup = False
        config_obj.use_by_lookup = False
        config_obj.verbose = True
        config_obj.verbose_level = 2
        config_obj.debug = True
        config_obj.debug_level = 2
        config_obj.config_read_file()
        self.assertIsNotNone(config_obj.authToken)

        config_obj.authToken = 'Hello.42'
        os.environ['syspass_auth_token'] = 'Hello.4242'

        self.assertEqual(config_obj.authToken, 'Hello.4242')

        del os.environ['syspass_auth_token']
        self.assertEqual(config_obj.authToken, 'Hello.42')

        self.assertRaises(TypeError, setattr, config_obj, 'authToken', 42)

    def test_tokenPass(self):
        config_obj = Config()
        config_obj.verbose = True
        config_obj.verbose_level = 2
        config_obj.debug = True
        config_obj.debug_level = 2
        config_obj.config_read_file()
        self.assertIsNotNone(config_obj.tokenPass)

        config_obj.tokenPass = 'Hello.42'
        os.environ['syspass_token_pass'] = 'Hello.4242'

        self.assertEqual(config_obj.tokenPass, 'Hello.4242')

        del os.environ['syspass_token_pass']
        self.assertEqual(config_obj.tokenPass, 'Hello.42')

        self.assertRaises(TypeError, setattr, config_obj, 'tokenPass', 42)

    def test_verify_ssl(self):
        config_obj = Config()
        config_obj.verbose = True
        config_obj.verbose_level = 2
        config_obj.debug = True
        config_obj.debug_level = 2
        self.assertIsNotNone(config_obj.verify_ssl)
        prev_data = config_obj.data

        config_obj.verify_ssl = False
        os.environ['syspass_verify_ssl'] = 'Hello.4242'
        self.assertTrue(config_obj.verify_ssl)

        del os.environ['syspass_verify_ssl']

        self.assertFalse(config_obj.verify_ssl)

        config_obj.verify_ssl = None

        self.assertTrue(config_obj.verify_ssl)

        os.environ['syspass_verify_ssl'] = "0"
        self.assertTrue(config_obj.verify_ssl)

        config_obj.data = prev_data

        self.assertRaises(TypeError, setattr, config_obj, 'verify_ssl', 42.42)

    def test_property_data(self):
        config_obj = Config()
        config_obj.verbose = False
        config_obj.debug = False
        config_obj.config_read_file()
        self.assertIsNotNone(config_obj.data)

    def test_read(self):
        config_obj = Config()
        config_obj.verbose = True
        config_obj.verbose_level = 2
        config_obj.debug = True
        config_obj.debug_level = 2
        config_obj.data = None
        self.assertIsNone(config_obj.data)

        os.environ['syspass_token_pass'] = 'Hello.4242'
        os.environ['syspass_auth_token'] = 'Hello.4242'
        os.environ['syspass_api_url'] = 'Hello.42'
        os.environ['syspass_api_version'] = '3.0'
        os.environ['syspass_verify_ssl'] = '0'
        os.environ['syspass_debug'] = '1'
        os.environ['syspass_debug_LEVEL'] = '42'
        os.environ['syspass_verbose'] = '1'
        os.environ['syspass_verbose_level'] = '42'
        config_obj.config_read_file()
        config_obj.display_resume()

        del os.environ['syspass_token_pass']
        del os.environ['syspass_auth_token']
        del os.environ['syspass_api_url']
        del os.environ['syspass_api_version']
        del os.environ['syspass_verify_ssl']
        del os.environ['syspass_debug']
        del os.environ['syspass_debug_LEVEL']
        del os.environ['syspass_verbose']
        del os.environ['syspass_verbose_level']

        config_obj.config_read_file()
        config_obj.display_resume()
        self.assertIsNotNone(config_obj.data)

        config_obj.config_import_data(config_obj.get_empty_config_dict())
        config_obj.display_resume()

    # def test_singleton(self):
    #     conf1 = Config()
    #     conf2 = Config()
    #     self.assertEqual(conf1, conf2)

    def test_get_empty_config_dict(self):
        conf = Config()
        what_i_need = {
            'syspassclient': {
                'api_url': None,
                'api_version': None,
                'authToken': None,
                'tokenPass': None,
                'debug': None,
                'debug_level': None,
                'verbose': None,
                'verbose_level': None,
                'verify_ssl': None
            }
        }
        self.assertEqual(what_i_need, conf.get_empty_config_dict())

    def test_display_resume(self):
        conf = Config()
        os.environ['syspass_api_url'] = "False"
        conf.config_read_file()
        conf.display_resume()

    def test_config_directory(self):
        conf = Config()
        if 'syspass_config_dir' in os.environ:
            self.assertEqual(os.path.abspath(os.path.expanduser(os.environ['syspass_config_dir'])), conf.config_directory)
        else:

            default_path = os.path.abspath(
                os.path.join(
                    os.path.join(
                        os.environ['HOME'],
                        '.config'),
                    'digdeo-syspass-client'
                )
            )
            self.assertEqual(default_path, conf.config_directory)
            os.environ['syspass_config_dir'] = '/tmp'
            self.assertEqual('/tmp', conf.config_directory)
            del os.environ['syspass_config_dir']

    def test_get_config_file(self):
        conf = Config()
        wanted_value = os.path.join(conf.config_directory, 'config.yml')
        self.assertEqual(wanted_value, conf.get_config_file())

    # def test_get_empty_config_dict(self):
    #     conf = Config()
    #     self.assertEqual(
    #         {
    #             'syspassclient': {
    #                 'api_url': None,
    #                 'api_version': '3.1',
    #                 'authToken': None,
    #                 'tokenPass': None,
    #                 'debug': True,
    #                 'debug_level': 3,
    #                 'verbose': False,
    #                 'verbose_level': 0
    #             }
    #         },
    #         conf.get_empty_config_dict()
    #     )

    def test_config_file(self):
        conf = Config()
        conf.config_file = 'Lulu'
        self.assertEqual('Lulu', conf.config_file)


if __name__ == "__main__":
    unittest.main()
