from mistletoe import markdown as render_markdown
from typing import Optional
from starlette.status import HTTP_302_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from textwrap import dedent
from fastapi import Form, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from re import match
from smtp_emailer import send
from email.mime.application import MIMEApplication
from sys import path
from os import getcwd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Session as DBSession, relationship
from uuid import uuid4
try:
    path.append(getcwd())
    from config import (
        WEBAPP_NAME,
        SMTP_HOST,
        SMTP_PORT,
        SMTP_USERNAME,
        SMTP_PASSWORD,
        SENDER_ADDRESS,
        REDIRECT_URL,
    )
    path.pop()
except:
    print("Error: invalid or missing config.py")
    exit(1)

EMAIL_REGEX = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True)
    confirmed = Column(Boolean, default=False) 
    sessions = relationship('Session', back_populates='user')

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    secret = Column(String, default=lambda: str(uuid4()))
    confirmed = Column(Boolean, default=False)
    user = relationship('User', back_populates='sessions')

def send_email(recipient, subject, html, attachments=[]):
    mail_attachments = []
    if attachments:
        for attachment in attachments:
            if attachment.size > 0:
                mail_attachment = MIMEApplication(
                    attachment.file.read(),
                    name=attachment.filename,
                )
                mail_attachment['Content-Disposition'] = 'attachment; filename="%s"' % attachment.filename
                mail_attachments.append(mail_attachment)
    send(SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_ADDRESS, recipient, subject, html, mail_attachments)

def send_sign_in_email(host, secret, email):
    # Put together the sign-in HTML
    sign_in_url = f"https://{host}/sign_in/{secret}"
    html = render_markdown(dedent(f"""
        Hi,

        To complete the sign in process and start using {WEBAPP_NAME}, please
        click the link below:

        <a clicktracking="off" href="SIGN_IN_URL">SIGN_IN_URL</a>

        If you didn't sign in to {WEBAPP_NAME}, please ignore this email.

        Thank you!<br>
        &mdash; The {WEBAPP_NAME} Team
    """))
    html = html.replace("SIGN_IN_URL", sign_in_url)
 
    # Set the subject.
    subject = f"{WEBAPP_NAME}: Sign in link."

    # Send it all
    send_email(email, subject, html)

    response_html = render_markdown(dedent(f"""
        ## Check your email.

        A sign-in link has been sent to EMAIL.

        Please check your email and click on the link to sign in.

        If you don't see the email within a few minutes, please check your spam or junk folder.
    """))

    response_html = response_html.replace("EMAIL", email)

    # Return HTML for the user.
    return response_html

def check_email_html(email):
    html = render_markdown(dedent(f"""
        ## Check your email.

        A confirmation link has been sent to EMAIL.

        Please check your email and click on the link to confirm your details.

        If you don't see the email within a few minutes, please check your spam or junk folder.
    """))

    html = html.replace("EMAIL", email)

    return html

def send_confirmation_email(host, secret, email):
    # Put together the confirmation HTML
    confirmation_url = f"https://{host}/sign_in/{secret}"

    html = render_markdown(dedent(f"""
        Hi,

        To complete the sign up process and start using {WEBAPP_NAME},
        please confirm your email address by clicking the link below:

        <a clicktracking="off" href="CONFIRMATION_URL">CONFIRMATION_URL</a>

        If you didn't sign up for {WEBAPP_NAME}, please ignore this email.

        Thank you!<br>
        &mdash; The {WEBAPP_NAME} Team
    """))

    html = html.replace("CONFIRMATION_URL", confirmation_url)
    subject = f"{WEBAPP_NAME}: Please confirm your email address."

    # Send it all
    send_email(email, subject, html)

    return check_email_html(email)

def setup_authbase(app, engine):
    for Model in [User, Session]:
        if not inspect(engine).has_table(Model.__tablename__):
            Model.__table__.create(engine)

    @app.post("/auth", response_class=HTMLResponse)
    async def auth(request: Request, response: Response, email: str = Form()):

        domain = "." + ".".join(request.headers.get("host").split(".")[-2:])

        email = email.lower()

        if not match(EMAIL_REGEX, email):
            return HTMLResponse("Invalid email address.", status_code=HTTP_400_BAD_REQUEST)

        with DBSession(engine) as db_session:
            user = db_session.query(User).where(User.email == email).first()
            if user:
                if user.confirmed:
                    # This user has sign up and is confirmed. Need to generate a session then send sign_in email.
                    session = Session(user=user)
                    db_session.add(session)
                    db_session.commit()
                    response.set_cookie(
                        key=f"session_id",
                        value=session.id,
                        domain=domain,  # Allows the cookie to be accessible across all subdomains
                        httponly=True,  # Prevents JavaScript access to the cookie
                        secure=True,  # Ensures the cookie is only sent over HTTPS
                        samesite="None",  # Allows the cookie to be sent with cross-origin requests
                        path="/",  # Makes the cookie available on all paths
                    )
                    return send_sign_in_email(request.headers.get("host"), session.secret, email)
                else:
                    # User account exists, but is unconfirmed.
                    # In this case, tell them to check their email again.
                    return check_email_html(email)
            else:
                user = User(email=email)
                session = Session(user=user)
                db_session.add(user)
                db_session.add(session)
                db_session.commit()
                response.set_cookie(
                    key=f"session_id",
                    value=session.id,
                    domain=domain,  # Allows the cookie to be accessible across all subdomains
                    httponly=True,  # Prevents JavaScript access to the cookie
                    secure=True,  # Ensures the cookie is only sent over HTTPS
                    samesite="None",  # Allows the cookie to be sent with cross-origin requests
                    path="/",  # Makes the cookie available on all paths
                )
                return send_confirmation_email(request.headers.get("host"), session.secret, email)

    @app.get("/sign_in/{secret}", response_class=HTMLResponse)
    async def sign_in(secret: str):
        with DBSession(engine) as db_session:
            session = db_session.query(Session).where(Session.secret == secret).first()
            if session is None:
                return HTMLResponse("Invalid session secret.", status_code=HTTP_400_BAD_REQUEST)
            session.user.confirmed = True
            session.confirmed = True
            db_session.commit()
        return RedirectResponse(REDIRECT_URL)

    @app.get("/me")
    async def me(request: Request):
        session_id = request.cookies.get(f"session_id")
        with DBSession(engine) as db_session:
            session = db_session.get(Session, session_id)
        if session is None:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        return {"id": session.user.id, "email": session.user.email}

    @app.post("/sign_out")
    async def sign_out(request: Request):
        session_id = request.cookies.get(f"session_id")
        with DBSession(engine) as db_session:
            session = db_session.get(Session, session_id)
            if session is None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
            session.delete(session)
            session.commit()
        return Response()
