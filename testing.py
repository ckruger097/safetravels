import unittest
from run import app


class BasicTestCase(unittest.TestCase):

    '''Valid home page, 200 response'''
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    '''Invalid page, 404 response'''
    def test_bad_page(self):
        tester = app.test_client(self)
        response = tester.get('a', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    '''Valid flight API page'''
    def test_flight_page(self):
        tester = app.test_client(self)
        response = tester.get('flightcovidAsk', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    '''Valid compare states page'''
    def test_compare_page(self):
        tester = app.test_client(self)
        response = tester.get('compare', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
