# pylint: disable=broad-except
# pylint: disable=consider-using-f-string
# pylint: disable=redefined-outer-name
from urllib import response


try:
    from routes import app
    import unittest
except Exception as e:
    print("Some Modules are Missing {} ".format(e))


class FlaskTest(unittest.TestCase):
    # check if login page response is 200
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content of login page contains 'Please Sign In'
    def test_login_content(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertTrue(b"Please Sign In" in response.data)

    # check if homepage response is 302
    def test_homepage(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)

    # check if logout page response is 200
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.get("/logout")
        statuscode = response.status_code
        self.assertEqual(statuscode, 302)


if __name__ == "__main__":
    unittest.main()
