from tests.base_test_case import BaseTestCase


class UserTests(BaseTestCase):
    def test_newsletter_signup(self):
        rv = self.client.post("/newsletter", json={"email": "user@example.com",})
        rv.status_code == 204
