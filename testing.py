import unittest
from run import app
from run import us_state_abbrev

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

    '''Testing all states to see if we get a valid response for the dashboard'''
    def test_fifty_states(self):
        tester = app.test_client(self)
        for state in us_state_abbrev:
            test_state = f"{state}-{us_state_abbrev[state]}"
            test_state.replace(" ", "%20")
            response = tester.get(f'us/{test_state}')
            self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()
