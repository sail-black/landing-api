from flask import Blueprint, url_for, render_template_string
from apifairy import body, other_responses
from itsdangerous import SignatureExpired


from api.app import db
from api.email import send_email
from api.models import Newsletter
from api.schemas import (
    PasswordResetRequestSchema,
    NewsletterSchema,
)

newsletter = Blueprint("newsletter", __name__)
newsletter_schema = NewsletterSchema()


@newsletter.route("/newsletter", methods=["GET", "POST"])
@body(PasswordResetRequestSchema)
def newsletter_conformation(args):
    """Request a newsletter conformation token"""
    s = Newsletter.get_seralizer()
    u = Newsletter(email=args["email"])
    email = u.email
    token = s.dumps(email, salt="email-confirm")
    link = "www.sail.black/" + "?token=" + token + "&email=" + email
    send_email(email, "Confirm subscription", "newsletter", token=token, url=link)
    u.confirmed = False
    u.ping()
    error = None
    try:
        db.session.add(u)
        db.session.commit()
    except Exception as e:
        error = str(e)
    return {"user": args["email"], "newsletter_status": False, "error": error}


@newsletter.route("/newsletter/<auth>", methods=["POST"])
@other_responses({400: "Invalid newsletter token"})
def newsletter_conform(auth):
    """Confirm the newsletter subscription"""
    s = Newsletter.get_seralizer()
    try:
        email = s.loads(auth, salt="email-confirm", max_age=3600)
        u = db.session.scalar(Newsletter.select().filter_by(email=email))
        u.confirmed = True
        u.ping()
        db.session.add(u)
        db.session.commit()
        send_email(email, "Welcome to the crew!", "conform")
    except SignatureExpired:
        return "<h1>The token is expired!</h1>"
    return render_template_string("<h1>Thank you for signing up!</h1>")


@newsletter.route("/newsletter/leave", methods=["GET", "POST"])
@body(PasswordResetRequestSchema)
def newsletter_leave(args):
    """Request a newsletter conformation token"""
    s = Newsletter.get_seralizer()
    u = db.session.scalar(Newsletter.select().filter_by(email=args["email"]))
    email = u.email
    u.reason_signoff = args["reason"]
    token = s.dumps(email, salt="sign-off-confirm")
    link = (
        "www.sail.black/" + "newsletter/leave/?token=" + token + "&email=" + email
    )  # change here for react_front_end
    u.ping()
    db.session.add(u)
    db.session.commit()
    send_email(
        email, "Confirm newsletter-sign-off", "conform_signoff", token=token, url=link
    )
    error = None
    return {"user": args["email"], "newsletter_status": u.confirmed, "error": error}


@newsletter.route("/newsletter/leave/<auth>", methods=["POST"])
@other_responses({400: "Invalid newsletter token"})
def newsletter_leave_conform(auth):
    """Confirm the newsletter subscription"""
    s = Newsletter.get_seralizer()
    try:
        email = s.loads(auth, salt="sign-off-confirm", max_age=3600)
        u = db.session.scalar(Newsletter.select().filter_by(email=email))
        u.confirmed = False
        u.ping()
        db.session.add(u)
        db.session.commit()
        send_email(email, "We are sad you left!", "sign-off")
    except SignatureExpired:
        return "<h1>The token is expired!</h1>"
    return render_template_string(
        "<h1>Thank you for joining us for a bit. We hope you come back. We love you!</h1>"
    )
