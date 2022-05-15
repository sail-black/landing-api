from tests.base_test_case import BaseTestCase
from api.app import db
from api.models import Newsletter
from tests.base_test_case import BaseTestCase


class UserTests(BaseTestCase):
    def test_newsletter_signup(self):
        rv = self.client.post("/newsletter", json={"email": "user@example.com",})
        rv.status_code == 204

    def test_newsletter_signoff(self):
        u = Newsletter(email="tim@example.com", confirmed=False)
        db.session.add(u)
        db.session.commit()
        u = db.session.scalar(Newsletter.select().filter_by(email="tim@example.com"))
        rv = self.client.post("/newsletter/leave", json={"email": u.email})
        rv.status_code == 204
