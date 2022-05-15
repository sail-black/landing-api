from datetime import datetime, timedelta
import sqlalchemy as sqla
import pytest
from api.app import db
from api.models import Newsletter
from tests.base_test_case import BaseTestCase


class NewsletterModelTests(BaseTestCase):
    def test_newsletter_hashing(self):
        try:
            u = db.session.scalar(
                Newsletter.select().filter_by(email="tim@example.com")
            )
            db.session.delete(u)
            db.session.commit()
        except Exception as e:
            print(e)

        u = Newsletter(email="tim@example.com", confirmed=False)
        db.session.add(u)
        db.session.commit()
        u = db.session.scalar(Newsletter.select().filter_by(email="tim@example.com"))
        assert u.confirmed == False
        u.confirmed = True
        db.session.add(u)
        db.session.commit()
        u = db.session.scalar(Newsletter.select().filter_by(email="tim@example.com"))
        assert u.confirmed
