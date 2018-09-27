import unittest
import keyvalue

class GetSetTest(unittest.TestCase):
    EXISTING_KEY = "existing_key"
    EXISTING_VALUE = "existing_value"
    HOMEPAGE_MSG = b'The results of your get or set operation will appear here'
    GET_KEY_MSG = 'The value for <b>{k}</b> is <b>{v}</b>'
    SET_KEY_MSG = 'The value for <b>{k}</b> has been set to <b>{v}</b>'
    def setUp(self):
        keyvalue.app.config['TESTING'] = True
        keyvalue.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/keyvalue_TESTING.db'

        self.app = keyvalue.app.test_client()
        keyvalue.db.create_all()
        self.setupDB()


    def tearDown(self):
        keyvalue.db.drop_all()

    def setupDB(self):
        kv = keyvalue.KeyValue(key=self.EXISTING_KEY, value=self.EXISTING_VALUE)
        keyvalue.db.session.merge(kv)
        keyvalue.db.session.commit()

    def test_homepage_no_operation(self):
        rv = self.app.get('/')
        self.assertIn(self.HOMEPAGE_MSG, rv.data)

    def test_get_good_key(self):
        rv = self.app.post('/', data= {'get_key':'existing_key'})
        self.assertIn(self.GET_KEY_MSG.format(k='existing_key', v='existing_value').encode(), rv.data)

    def test_get_bad_key(self):
        rv = self.app.post('/', data= {'get_key':'nonexisting_key'})
        self.assertIn(b'Oops! The value for that key has not been set', rv.data)

    def test_set_value(self):
        rv = self.app.post('/', data= {'set_value':'new_value',
                                       'set_key':'new_key'})
        self.assertIn(self.SET_KEY_MSG.format(k='new_key',v='new_value').encode(), rv.data)

    def test_set_existing_value(self):
        rv = self.app.post('/', data= {'set_value':'new_value',
                                       'set_key':'existing_key'})
        self.assertIn(self.SET_KEY_MSG.format(k='existing_key', v='new_value').encode(), rv.data)

    def test_get_empty_key(self):
        """ Should just show homepage message"""
        rv = self.app.post('/', data= {'get_key':''})
        self.assertIn(self.HOMEPAGE_MSG, rv.data)

    def test_set_empty_key(self):
        """ Should just show homepage message"""
        rv = self.app.post('/', data= {'set_key':'', 'set_value':'val'})
        self.assertIn(self.HOMEPAGE_MSG, rv.data)

    def test_set_empty_value(self):
        """ Empty value ok, will be set"""
        rv = self.app.post('/', data= {'set_key':'key', 'set_value':''})
        self.assertIn(self.SET_KEY_MSG.format(k='key', v='').encode(), rv.data)

    def test_set_then_get_key(self):
        self.app.post('/', data= {'set_value':'new_value',
                                  'set_key':'new_key'})
        rv = self.app.post('/', data= {'get_key':'new_key'})
        self.assertIn(self.GET_KEY_MSG.format(k='new_key', v='new_value').encode(), rv.data)


if __name__ == '__main__':
    unittest.main()
