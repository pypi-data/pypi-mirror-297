#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import syspassclient
import uuid

# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper


class TestSyspassClient(unittest.TestCase):
    def setUp(self):
        self.sp_client = syspassclient.SyspassClient(
            use_by_lookup=False,
            api_url='https://this.is.a.test.ici/api.php',
            api_version='3.1',
            authToken='#############################################',
            tokenPass='#############################################',
            verify_ssl=True,
            debug=True,
            debug_level=3,
            verbose=True,
            verbose_level=3
        )

    def test_init(self):
        sp_client = syspassclient.SyspassClient(
            use_by_lookup=False,
            api_url='https://this.is.a.test.ici/api.php',
            api_version='3.1',
            authToken='#############################################',
            tokenPass='#############################################',
            verify_ssl=True,
            debug=True,
            debug_level=3,
            verbose=True,
            verbose_level=3
        )

        # self.assertTrue(sp_client.use_by_lookup)
        sp_client.use_by_lookup = True
        sp_client.api_url = 'https://this.is.a.test.ici/api.php'
        sp_client.api_version = '3.1'
        sp_client.authToken = '#############################################'
        sp_client.tokenPass = '#############################################'
        sp_client.debug = True
        sp_client.debug_level = 3
        sp_client.verbose = True
        sp_client.verbose_level = 3

        # sp_client.read_config()
        # self.assertTrue(sp_client.use_by_lookup)
        # self.assertEqual(sp_client.api_url, 'https://this.is.a.test.ici/api.php')
        self.assertEqual(sp_client.api_version, '3.1')
        # self.assertEqual(sp_client.authToken, '#############################################')
        # self.assertEqual(sp_client.tokenPass, '#############################################')
        self.assertTrue(sp_client.debug)
        self.assertEqual(sp_client.debug_level, 3)
        self.assertTrue(sp_client.verbose)
        self.assertEqual(sp_client.verbose_level, 3)

    def test_Account_delete(self):
        sp_client = syspassclient.SyspassClient()
        self.assertTrue(True)

    def test_AccountSearch(self):
        """Test"""
        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()

        self.assertRaises(TypeError, sp_client.account_view)
        self.assertRaises(TypeError, sp_client.account_view, authToken="Hello")
        self.assertRaises(TypeError, sp_client.account_view, authToken="Hello", tokenPass="Hello")
        self.assertRaises(TypeError, sp_client.account_view, authToken="Hello", tokenPass="Hello", hello=42)

        # prepare a category
        category_random_name = f'Category_{uuid.uuid4().hex[:6]}'
        req = sp_client.category_create(
            name=category_random_name,
            description='a Category for tests'
        )

        actual_category_id = req

        req = sp_client.category_search(
            text=category_random_name
        )

        found_category_id = req

        self.assertEqual(actual_category_id, found_category_id)

        # create a client
        client_random_name = f'Client_{uuid.uuid4().hex[:6]}'
        req = sp_client.client_create(
            name=client_random_name,
            description='a Client for tests'
        )
        actual_client_id = req

        req = sp_client.client_search(
            text=client_random_name
        )

        found_client_id = req

        self.assertEqual(actual_client_id, found_client_id)

        # group
        random_group_name = f'Group_{uuid.uuid4().hex[:6]}'
        req = sp_client.user_group_create(
            name=random_group_name,
            description='a UserGroup for test'
        )
        ugid = req

        req = sp_client.user_group_search(
            text=random_group_name
        )

        found_ugid = req

        self.assertEqual(ugid, found_ugid)

        # create the account
        random_name = utils.random_string(length=20, prefix=f'Account_{uuid.uuid4().hex[:6]}')
        random_password = utils.random_string(length=20)

        req = sp_client.account_create(
            name=random_name,
            categoryId=int(actual_category_id),
            clientId=int(actual_client_id),
            password=random_password,
            userGroupId=int(ugid)
        )
        actual_account_id = req

        # Case where nothing is found
        rep = sp_client.account_search(text=random_name)
        self.assertIsNotNone(rep)
        self.assertEqual(type(req), int)

        # clean up
        sp_client.account_delete(
            account_id=actual_account_id
        )

        req = sp_client.account_search(
            text=client_random_name
        )
        self.assertIsNone(req)

        # authToken - must be set and be a str
        self.assertRaises(TypeError, sp_client.account_search, authToken=42)

        # text - can be None, if not must be a str
        self.assertRaises(TypeError, sp_client.account_search, authToken=sp_client.authToken, text=42)
        # count - can be None, if not must be a int
        self.assertRaises(TypeError, sp_client.account_search, authtoken=sp_client.authToken, count="Hello")
        # category_id - can be None, if not must be a int
        self.assertRaises(TypeError, sp_client.account_search, authToken=sp_client.authToken,
                          categoryId="Hello")
        # client_id - can be None, if not must be a int
        self.assertRaises(TypeError, sp_client.account_search, authToken=sp_client.authToken,
                          categoryId="Hello")
        # tags_id - can be None, if not must be a int
        self.assertRaises(TypeError, sp_client.account_search, authToken=sp_client.authToken,
                          categoryId="Hello")
        # op - can be None or only have 'and' or 'or' value
        self.assertRaises(TypeError, sp_client.account_search, authToken=sp_client.authToken, op=42)
        # self.assertRaises(AssertionError, sp_client.account_search,
        #                   authtoken=self.authtoken,
        #                   op='Hello'
        #                   )
        self.assertRaises(TypeError, sp_client.account_search, authToken=sp_client.authToken, match_all=42)

        # Test without require args
        # self.assertRaises(TypeError, sp_client.account_search)

    def test_AccountView(self):

        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()

        self.assertRaises(TypeError, sp_client.account_view)
        self.assertRaises(TypeError, sp_client.account_view, authToken="Hello")
        self.assertRaises(TypeError, sp_client.account_view, authToken="Hello", tokenPass="Hello")
        self.assertRaises(TypeError, sp_client.account_view, authToken="Hello", tokenPass="Hello", hello=42)

        # Normal case

        # prepare a category
        category_random_name = f'Category_{uuid.uuid4().hex[:6]}'
        req = sp_client.category_create(
            name=category_random_name,
            description='a Category for tests'
        )

        actual_category_id = req

        req = sp_client.category_search(
            text=category_random_name
        )

        found_category_id = req

        self.assertEqual(actual_category_id, found_category_id)

        # create a client
        client_random_name = f'Client_{uuid.uuid4().hex[:6]}'
        req = sp_client.client_create(
            name=client_random_name,
            description='a Client for tests'
        )
        actual_client_id = req

        req = sp_client.client_search(
            text=client_random_name
        )

        found_client_id = req

        self.assertEqual(actual_client_id, found_client_id)

        # group
        random_group_name = f'Group_{uuid.uuid4().hex[:6]}'
        req = sp_client.user_group_create(
            name=random_group_name,
            description='a UserGroup for test'
        )
        ugid = req

        req = sp_client.user_group_search(
            text=random_group_name
        )

        found_ugid = req

        self.assertEqual(ugid, found_ugid)

        # create the account
        random_name = utils.random_string(length=20, prefix=f'Category_{uuid.uuid4().hex[:6]}')
        random_password = utils.random_string(length=20)

        req = sp_client.account_create(
            name=random_name,
            categoryId=int(actual_category_id),
            clientId=int(actual_client_id),
            password=random_password,
            userGroupId=int(ugid)
        )
        actual_account_id = req

        req = sp_client.account_view(
            account_id=actual_account_id
        )

        self.assertIsNotNone(req)
        self.assertTrue('dateAdd' in req)

        # clean up
        sp_client.account_delete(
            account_id=actual_account_id
        )

        req = sp_client.account_search(
            text=client_random_name
        )
        self.assertIsNone(req)

    def test_AccountViewpass(self):

        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()

        sp_client.use_by_lookup = False
        sp_client.config_read_file()

        # prepare a category
        category_random_name = f'Category_{uuid.uuid4().hex[:6]}'
        req = sp_client.category_create(
            name=category_random_name,
            description='a Category for tests'
        )

        actual_category_id = req

        req = sp_client.category_search(
            text=category_random_name
        )

        found_category_id = req

        self.assertEqual(actual_category_id, found_category_id)

        # create a client
        client_random_name = f'Client_{uuid.uuid4().hex[:6]}'
        req = sp_client.client_create(
            name=client_random_name,
            description='a Client for tests'
        )
        actual_client_id = req

        req = sp_client.client_search(
            text=client_random_name
        )

        found_client_id = req

        self.assertEqual(actual_client_id, found_client_id)

        # group
        random_group_name = f'Group_{uuid.uuid4().hex[:6]}'
        req = sp_client.user_group_create(
            name=random_group_name,
            description='a UserGroup for test'
        )
        ugid = req

        req = sp_client.user_group_search(
            text=random_group_name
        )

        found_ugid = req

        self.assertEqual(ugid, found_ugid)

        # create the account
        random_name = utils.random_string(length=20, prefix=f'Category_{uuid.uuid4().hex[:6]}')
        random_password = utils.random_string(length=20)

        req = sp_client.account_create(
            name=random_name,
            categoryId=int(actual_category_id),
            clientId=int(actual_client_id),
            password=random_password,
            userGroupId=int(ugid)
        )
        actual_account_id = req

        rep = sp_client.account_viewpass(
            account_id=actual_account_id
        )

        self.assertIsNotNone(rep)
        self.assertEqual(type(rep), str)

        # clean up
        sp_client.account_delete(
            account_id=actual_account_id
        )

        req = sp_client.account_search(
            text=client_random_name
        )
        self.assertIsNone(req)

    def test_AccountEditPass(self):
        sp_client = syspassclient.SyspassClient()
        self.assertTrue(True)

        # req = sp_client.AccountSearch(text="Charles Palmolive", authToken=self.authToken)

        # categoryId = sp_client.category_search(text=user_name_to_test, count=1)
        # if isinstance(categoryId, dict):
        #     categoryId = categoryId["id"]
        # else:
        #     categoryId = sp_client.category_create(name=user_name_to_test)["itemId"]
        #
        # userGroupId = sp_client.user_group_search(text=user_name_to_test, count=1)
        # if isinstance(userGroupId, dict):
        #     userGroupId = userGroupId['id']
        # else:
        #     userGroupId = sp_client.user_group_create(
        #         name=user_name_to_test,
        #         description=user_name_to_test)['itemId']
        #
        # user_exist = sp_client.AccountSearch(text=user_name_to_test, authToken=self.authToken)

        # if user_exist is None:
        #     sp_client.AccountCreate(
        #             authToken=self.authToken,
        #             tokenPass=self.tokenPass,
        #             name=user_name_to_test,
        #             categoryId=categoryId,
        #             userGroupId=userGroupId,
        #             password=random_string()
        #         )

    def test_AccountCreate(self):
        """Test"""
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()

        # prepare a category
        category_random_name = f'Category_{uuid.uuid4().hex[:6]}'
        req = sp_client.category_create(
            name=category_random_name,
            description='a Category for tests'
        )

        actual_category_id = req

        req = sp_client.category_search(
            text=category_random_name
        )

        found_category_id = req

        self.assertEqual(actual_category_id, found_category_id)

        # create a client
        client_random_name = f'Client_{uuid.uuid4().hex[:6]}'
        req = sp_client.client_create(
            name=client_random_name,
            description='a Client for tests'
        )
        actual_client_id = req

        req = sp_client.client_search(
            text=client_random_name
        )

        found_client_id = req

        self.assertEqual(actual_client_id, found_client_id)

        # group
        random_group_name = f'Group_{uuid.uuid4().hex[:6]}'
        req = sp_client.user_group_create(
            name=random_group_name,
            description='a UserGroup for test'
        )
        ugid = req

        req = sp_client.user_group_search(
            text=random_group_name
        )

        found_ugid = req

        self.assertEqual(ugid, found_ugid)

        # create the account
        random_name = sp_client.random_string(length=20, prefix=f'Category_{uuid.uuid4().hex[:6]}')
        random_password = sp_client.random_string(length=20)

        req = sp_client.account_create(
            name=random_name,
            categoryId=int(actual_category_id),
            clientId=int(actual_client_id),
            password=random_password,
            userGroupId=int(ugid)
        )
        actual_account_id = req

        # sp_client.category_delete(
        #     authToken=self.authToken,
        #     cid=actual_category_id
        # )
        # req = sp_client.category_search(
        #     authToken=self.authToken,
        #     text=category_random_name
        # )
        # self.assertIsNone(req)

        # clean everything
        # sp_client.client_delete(
        #     authToken=self.authToken,
        #     cid=actual_client_id
        # )
        # req = sp_client.client_search(
        #     authToken=self.authToken,
        #     text=client_random_name
        # )
        # self.assertIsNone(req)

        # clean up
        sp_client.account_delete(
            account_id=actual_account_id
        )

        req = sp_client.account_search(
            text=client_random_name
        )
        self.assertIsNone(req)

    def test_Categories(self):
        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()

        random_name = utils.random_string()
        req1 = sp_client.category_create(
            name=random_name,
            description='a Client for tests'
        )
        req2 = sp_client.category_create(
            name=random_name,
            description='a Client for tests'
        )
        self.assertEqual(req1, req2)

        cid = req1

        req = sp_client.category_search(
            text=random_name
        )

        found_cid = req

        self.assertEqual(cid, found_cid)

        sp_client.category_delete(
            cid=cid
        )
        # Try to re-create a deleted category
        # import time
        # time.sleep(15)
        req = sp_client.category_create(
            name=random_name,
            description='a Client for tests'
        )
        cid1 = req

        req = sp_client.category_create(
            name=random_name,
            description='a Client for tests'
        )
        cid2 = req

        self.assertEqual(cid1, cid2)
        sp_client.category_delete(
            cid=cid1
        )

    def test_Clients(self):
        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()

        random_name = utils.random_string()
        req = sp_client.client_create(
            name=random_name,
            description='a Client for tests'
        )
        cid = req

        req = sp_client.client_search(
            text=random_name
        )

        found_cid = req

        self.assertEqual(cid, found_cid)

        sp_client.client_delete(
            cid=cid
        )
        self.assertIsNone(sp_client.client_delete(
            cid=cid
        ))

    def test_issue_5(self):
        # client search with multiple response return only the first one and not the exact match name
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()

        # create first client
        cust1 = f'LULU_{uuid.uuid4().hex[:6]}'
        req_lulu = sp_client.client_create(
            name=cust1,
            description='LULU'
        )
        cid_lulu = req_lulu

        req_lulu = sp_client.client_search(
            text=cust1
        )

        found_cid_lulu = req_lulu

        self.assertEqual(cid_lulu, found_cid_lulu)

        # create second client
        cust2 = f'LALA_{uuid.uuid4().hex[:6]}'
        req_lala = sp_client.client_create(
            name=cust2,
            description='LULU'
        )
        cid_lala = req_lala

        req_lala = sp_client.client_search(
            text=cust2
        )

        found_cid_lala = req_lala

        self.assertEqual(cid_lala, found_cid_lala)

        req_test = sp_client.client_search(
            text=cust1
        )
        self.assertEqual(req_test, cid_lulu)
        sp_client.client_delete(
            cid=cid_lala
        )
        self.assertIsNone(sp_client.client_delete(
            cid=cid_lala
        ))

        sp_client.client_delete(
            cid=cid_lulu
        )
        self.assertIsNone(sp_client.client_delete(
            cid=cid_lulu
        ))

    def test_client_search(self):
        sp_client = syspassclient.SyspassClient()

        dict_wrong = {'result': {
            'result': [
                {'name': 'Hello',
                 'id': 42
                 },
                {'name': 'lulu',
                 'id': 4012
                 }
            ],
            'count': 2
        }
        }
        text = 'lulu'

        self.assertEqual(dict_wrong['result']['result'][0]['name'], 'Hello')
        self.assertEqual(dict_wrong['result']['result'][0]['id'], 42)
        self.assertEqual(dict_wrong['result']['result'][1]['name'], 'lulu')
        self.assertEqual(dict_wrong['result']['result'][1]['id'], 4012)

        if 'result' in dict_wrong and 'count' in dict_wrong['result'] and type(dict_wrong['result']['count']) == int:
            if dict_wrong['result']['count'] > 0:
                for res in dict_wrong['result']['result']:
                    if res['name'].upper() == text.upper():
                        self.assertEqual(4012, res['id'])

    def test_Tags(self):
        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()

        random_name = utils.random_string()
        req1 = sp_client.tag_create(
            name=random_name
        )
        req2 = sp_client.tag_create(
            name=random_name
        )
        self.assertEqual(req1, req2)
        tagid = req1

        req = sp_client.tag_search(
            text=random_name
        )
        self.assertIsNone(sp_client.tag_search(
            text='Hello.42'
        ))

        found_tagid = req

        self.assertEqual(random_name, sp_client.tag_view(
            tagid=tagid
        ))

        self.assertEqual(tagid, found_tagid)

        req = sp_client.tag_delete(
            tagid=tagid
        )
        self.assertEqual(0, req)

        self.assertIsNone(sp_client.tag_delete(
            tagid=tagid
        ))

    def test_UserGroup(self):
        utils = syspassclient.Libs()
        sp_client = syspassclient.SyspassClient()

        random_name = utils.random_string()

        self.assertIsNone(sp_client.user_group_search(text=random_name))

        req = sp_client.user_group_create(
            name=random_name,
            description='a UserGroup for test'
        )
        ugid = req

        self.assertEqual(ugid, sp_client.user_group_create(
            name=random_name,
            description='a UserGroup for test'
        ))
        # self.assertIsNone(sp_client.user_group_create(
        #     name=random_name,
        #     description='a UserGroup for test'
        # )
        # )

        req = sp_client.user_group_search(
            text=random_name
        )

        found_ugid = req

        self.assertEqual(ugid, found_ugid)

        sp_client.user_group_delete(
            ugid=ugid
        )

        # test if it return None in case of error
        self.assertIsNone(sp_client.user_group_delete(
            ugid=ugid
        ))

    def test_api_url(self):
        """Test SyspassClient.api_url property  """
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()
        sp_client.display_resume()
        self.assertIsNone(syspassclient.check_type.CheckType().is_url_or_raise(sp_client.api_url))
        os.environ['syspass_api_url'] = "Hello"
        self.assertRaises(ValueError, syspassclient.check_type.CheckType().is_url_or_raise,
                          sp_client.api_url)
        os.environ['syspass_api_url'] = "http://perdu.com"
        self.assertIsNone(syspassclient.check_type.CheckType().is_url_or_raise(sp_client.api_url))
        del os.environ['syspass_api_url']
        self.assertIsNone(syspassclient.check_type.CheckType().is_url_or_raise(sp_client.api_url))

    def test_generate_json(self):
        sp_client = syspassclient.SyspassClient()

        data = sp_client.generate_json(method="account/viewPass")
        self.assertTrue("id" in data)
        self.assertTrue("jsonrpc" in data)
        self.assertTrue("method" in data)
        self.assertTrue("params" in data)

        self.assertRaises(KeyError, sp_client.generate_json)

    def test_increase_request_id(self):
        sp_client = syspassclient.SyspassClient()

        old_value = sp_client.r_id
        sp_client.increase_request_id(increment=1)
        self.assertEqual(sp_client.r_id, old_value + 1)
        old_value = sp_client.r_id
        sp_client.increase_request_id(increment=42)
        self.assertEqual(sp_client.r_id, old_value + 42)
        self.assertRaises(TypeError, sp_client.increase_request_id, increment="Hello")
        self.assertRaises(ValueError, sp_client.increase_request_id, increment=0)
        self.assertRaises(ValueError, sp_client.increase_request_id, increment=-42)

    # def test_invalid_key(self):
    #     import os
    #     os.environ['syspass_token_pass'] = 'Hello'
    #     utils = syspassclient.Utils()
    #
    #     random_name = utils.random_string()
    #     req = sp_client.tag_create(
    #         authToken=self.authToken,
    #         name=random_name
    #     )

    def test_print_returned_value(self):
        sp_client = syspassclient.SyspassClient()

        sp_client.verbose = True
        sp_client.verbose_level = 3
        sp_client.print_returned_value(req={'error': True})
        sp_client.print_returned_value(req={'Hello': 42})

    def test_controlled_match_all(self):
        sp_client = syspassclient.SyspassClient()
        sp_client.use_by_lookup = False
        sp_client.config_read_file()
        text = 'Hello.42'
        req = {
            'jsonrpc': '2.0',
            'result': {'itemId': 0, 'result': [{'id': 42, 'name': text}], 'resultCode': 0, 'resultMessage': "Hello.42",
                       'count': 1},
            'id': 13
        }

        sp_client.controlled_match_all(req=req, matchall=True, text=text)
        sp_client.controlled_match_all(req=req, matchall=None, text=text)
        self.assertRaises(TypeError, sp_client.controlled_match_all, req=None, matchall=True, text=text)
        self.assertRaises(TypeError, sp_client.controlled_match_all, req=req, matchall=42, text=text)


if __name__ == "__main__":
    unittest.main()
