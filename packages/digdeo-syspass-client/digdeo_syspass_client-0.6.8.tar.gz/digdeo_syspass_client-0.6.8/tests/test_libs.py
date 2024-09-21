import unittest
from syspassclient import Libs


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.utils = Libs()

    def test_check_args(self):
        self.assertRaises(ValueError, self.utils.look_for_args, method="42")
        self.assertRaises(AttributeError, self.utils.look_for_args, method="account/viewPass", hello=42)
        # Lulu is not part of the API
        self.assertRaises(
            AttributeError,
            self.utils.look_for_args,
            method="account/viewPass",
            authToken="Hello",
            tokenPass="Hello",
            account_id=42,
            details=42,
            lulu=42,
        )
        # A require parameter is not set
        self.assertRaises(
            AttributeError, self.utils.look_for_args, method="account/viewPass", authToken="Hello", id=42, details=42
        )
        # Test type of parameters
        self.assertRaises(
            TypeError,
            self.utils.look_for_args,
            method="account/viewPass",
            authToken=42,
            tokenPass="Hello",
            account_id=42,
            details=42,
        )
        self.assertRaises(
            TypeError,
            self.utils.look_for_args,
            method="account/viewPass",
            authToken="Hello",
            tokenPass=42,
            account_id=42,
            details=42,
        )

        # self.assertEqual('', sp_client.check_args(method='account/viewPass', api_version='3.0', lulu=10))

    def test_look_for_error(self):
        data = {}
        req = {}

        self.assertIsNone(self.utils.look_for_error(data=data, req=req), "")

        self.assertRaises(TypeError, self.utils.look_for_error, data=42, req=req)
        self.assertRaises(TypeError, self.utils.look_for_error, data=data, req=42)

        req = {
            "error": {
                "message": "Internal error",
                "code": 42,
                "data": "the data"
            }
        }
        data = {
            "method": "account/create"
        }
        self.assertRaises(ValueError, self.utils.look_for_error, data=data, req=req)

    def test_look_for_parameters_injection(self):
        # Test without method
        self.assertRaises(
            AttributeError,
            self.utils.look_for_parameters_injection,
            method="account/viewPass",
            authToken="Hello",
            tokenPass="Hello",
            id=1,
            hello=42,
        )
        self.assertRaises(
            KeyError,
            self.utils.look_for_parameters_injection,
            authToken="Hello",
            tokenPass="Hello",
            account_id=1
        )

    def test_look_for_parameters_type(self):

        # Test without method
        self.assertRaises(
            TypeError,
            self.utils.look_for_parameters_type,
            method="account/viewPass",
            authToken=42,
            tokenPass="Hello",
            account_id=1,
        )
        self.assertRaises(
            TypeError,
            self.utils.look_for_parameters_type,
            method="account/viewPass",
            authToken="Hello",
            tokenPass="Hello",
            account_id="42",
        )
        self.assertRaises(
            KeyError,
            self.utils.look_for_parameters_type,
            authToken="Hello",
            tokenPass="Hello",
            account_id=1
        )
        self.assertRaises(
            TypeError,
            self.utils.look_for_parameters_type,
            method="userGroup/create",
            name="Hello",
            description="Hello",
            usersId=42
        )
        # That work at all
        self.utils.look_for_parameters_type(
            method="account/viewPass",
            authToken="Hello",
            tokenPass="Hello",
            account_id=1
        )

    def test_look_for_valid_method(self):

        # Test without method
        self.assertRaises(KeyError, self.utils.look_for_valid_method, authToken="Hello", tokenPass="Hello", id=1)
        self.assertRaises(ValueError, self.utils.look_for_valid_method, method="account/42")
        self.utils.look_for_valid_method(method="account/viewPass")

    def test_look_for_required_params(self):

        # Test without method
        self.assertRaises(
            KeyError,
            self.utils.look_for_required_params,
            authToken="Hello",
            tokenPass="Hello",
            account_id=1
        )
        # Require parameter for method='account/viewPass' is ['authToken', 'tokenPass', 'id']]
        # tests without id
        self.assertRaises(
            AttributeError,
            self.utils.look_for_required_params,
            method="account/viewPass",
            authToken="Hello",
            tokenPass="Hello",
        )
        # tests without authToken
        self.assertRaises(
            AttributeError,
            self.utils.look_for_required_params,
            method="account/viewPass",
            tokenPass="Hello",
            account_id=1
        )
        # tests without tokenPass
        self.assertRaises(
            AttributeError,
            self.utils.look_for_required_params,
            method="account/viewPass",
            authToken="Hello",
            account_id=1
        )

        # work at all
        self.utils.look_for_required_params(
            method="account/viewPass",
            authToken="Hello",
            tokenPass="Hello",
            account_id=1
        )

    def test_require_parameter(self):

        # Account
        for element in self.utils.required_parameters('account/search'):
            self.assertTrue(element in ['authToken'])

        for element in self.utils.required_parameters('account/view'):
            self.assertTrue(element in ['account_id', 'authToken', 'tokenPass'])

        for element in self.utils.required_parameters('account/viewPass'):
            self.assertTrue(element in ['account_id', 'authToken', 'tokenPass'])

        for element in self.utils.required_parameters('account/editPass'):
            self.assertTrue(element in ['account_id', 'authToken', 'password', 'tokenPass'])

        for element in self.utils.required_parameters('account/create'):
            self.assertTrue(element in ['authToken', 'categoryId', 'clientId', 'name', 'password', 'tokenPass'])

        for element in self.utils.required_parameters('account/edit'):
            self.assertTrue(element in ['account_id', 'authToken', 'tokenPass'])

        for element in self.utils.required_parameters('account/delete'):
            self.assertTrue(element in ['account_id', 'authToken'])

        # Categories
        for element in self.utils.required_parameters('category/search'):
            self.assertTrue(element in ['authToken'])

        for element in self.utils.required_parameters('category/view'):
            self.assertTrue(element in ['authToken', 'count', 'text'])

        for element in self.utils.required_parameters('category/create'):
            self.assertTrue(element in ['authToken', 'name'])

        for element in self.utils.required_parameters('category/edit'):
            self.assertTrue(element in ['authToken', 'cid', 'name'])

        for element in self.utils.required_parameters('category/delete'):
            self.assertTrue(element in ['authToken', 'cid'])

        # Clients
        for element in self.utils.required_parameters('client/search'):
            self.assertTrue(element in ['authToken'])

        for element in self.utils.required_parameters('client/view'):
            self.assertTrue(element in ['authToken', 'cid', 'tokenPass'])

        for element in self.utils.required_parameters('client/create'):
            self.assertTrue(element in ['authToken', 'name'])

        for element in self.utils.required_parameters('client/edit'):
            self.assertTrue(element in ['authToken', 'cid', 'name'])

        for element in self.utils.required_parameters('client/delete'):
            self.assertTrue(element in ['authToken', 'cid'])

        # Tags
        for element in self.utils.required_parameters('tag/search'):
            self.assertTrue(element in ['authToken'])

        for element in self.utils.required_parameters('tag/view'):
            self.assertTrue(element in ['authToken', 'tagid', 'tokenPass'])

        for element in self.utils.required_parameters('tag/create'):
            self.assertTrue(element in ['authToken', 'name'])

        for element in self.utils.required_parameters('tag/edit'):
            self.assertTrue(element in ['authToken', 'name', 'tagid'])

        for element in self.utils.required_parameters('tag/delete'):
            self.assertTrue(element in ['authToken', 'tagid'])

        # User Groups
        for element in self.utils.required_parameters('userGroup/search'):
            self.assertTrue(element in ['authToken'])

        for element in self.utils.required_parameters('userGroup/view'):
            self.assertTrue(element in ['authToken', 'tokenPass', 'ugid'])

        for element in self.utils.required_parameters('userGroup/create'):
            self.assertTrue(element in ['authToken', 'name'])

        for element in self.utils.required_parameters('userGroup/edit'):
            self.assertTrue(element in ['authToken', 'name', 'ugid'])

        for element in self.utils.required_parameters('userGroup/delete'):
            self.assertTrue(element in ['authToken', 'ugid'])

        # Configuration
        for element in self.utils.required_parameters('config/backup'):
            self.assertTrue(element in ['authToken'])

        for element in self.utils.required_parameters('config/export'):
            self.assertTrue(element in ['authToken'])

    def test_merge(self):

        dict_source = {"a": 0, "b": 0}
        dict_target = {"a": 42.1, "c": 42.3, "d": 42.4}
        self.assertEqual(
            self.utils.merge_dictionary(target=dict_source, source=dict_target),
            {"a": 42.1, "b": 0, "c": 42.3, "d": 42.4},
        )

    def test_random_string(self):

        self.assertRaises(TypeError, self.utils.random_string, length=20, prefix=42)
        self.assertEqual(str, type(self.utils.random_string(length=20)))
        self.assertEqual(20, len(self.utils.random_string(length=20)))

        self.assertEqual(str, type(self.utils.random_string(length=20, prefix="test_")))
        self.assertEqual(25, len(self.utils.random_string(length=20, prefix="test_")))

        # test for 1000000 of case
        # t0 = int(round(time.time() * 1000))
        for count in range(1, 1000, 1):
            value1 = self.utils.random_string(length=20)
            value2 = self.utils.random_string(length=20)

            self.assertNotEqual(value1, value2)

        # sys.stdout.write("done in: {0} secs".format(
        #     convert_milliseconds_to_seconds(int(round(time.time() * 1000)) - t0))
        # )


if __name__ == '__main__':
    unittest.main()
