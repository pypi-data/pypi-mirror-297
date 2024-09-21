## Overview

Authbase a provides authentication for FastAPI/SQLAlchemy webapps.

It doesn't use passwords for authentication, instead it relies on users
clicking a link that was sent to their email address. The logic behind this is
that usually there is a reset password option that sends an email anyway, so in
theory it is a system that has the same or a similar level of security.

AuthBase also provides a function for emailing users.

## Setup

    pip install authbase

Then in your FastAPI webapp:

    from fastapi import FastAPI
    from sqlalchemy import create_engine
    from authbase import setup_authbase

    app = FastAPI()
    engine = create_engine('sqlite:///example.db')
    setup_authbase(app, engine)

    # ... the rest of your code goes here ...

Then edit config.py in the root directory of your project to contain:

    # Name of your webapp.
    WEBAPP_NAME='My Example App'

    # Email settings.
    SMTP_HOST='smtp.example.org'
    SMTP_PORT=587
    SMTP_USERNAME='username'
    SMTP_PASSWORDD='password'
    SENDER_ADDRESS='My Example App <no-reply@example.org>'

    # Redirct URL where users are sent after they successfully confirm their email
    # address or sign in.
    REDIRECT_URL='https://example.org/signed-in'

## API

### POST /auth

Signs up a new user or initiates the sign in process.

This endpoint takes a single parameter, **email**, which should be the email
address of the user signing up or signing in.

The response is HTML with a message instructing the user to check their email
for a confirmation link or a link to sign in.

The response sets a **session_id** cookie.

Here's an example JS snippet that you can attach to a form submit event:

    const form = document.getElementById("my-sign-in-form")
    form.addEventListener("submit", event => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        fetch("https://api.example.org/auth", {
            method: "POST",
            body: formData,
            credentials: "include",
        }).then(... handle response ...);
    });

### POST /sign_out

This endpoint takes no parameters and signs out the user associated with the
**session_id** cookie.

Here's an example JS snippet that makes this request:

    await fetch('https://api.example.org/sign_out', {
        method: 'POST',
        credentials: 'include',
    }); 

### GET /me

Gets information about the currently signed in user.

The request should send the **session_id** cookie.

The response is A JSON object with two fields, **id**, and **email_address**.

This response returns error 401 (Unauthenticated) if the user has not signed in.

Here's an example JS snippet that makes this request:

    fetch('https://api.example.org/me', {
        method: 'GET',
        credentials: 'include',
    }).then(... handle response ...);

### GET /sign_in/{

This endpoint is for internal use only.
