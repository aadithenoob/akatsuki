from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import requests
import os

auth = Blueprint("auth", __name__)

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_SCOPE = "identify guilds"


def discord_auth_url():
    return f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={DISCORD_SCOPE}"


@auth.route("/login")
def login():
    if not all([DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI]):
        return "OAuth2 environment variables not properly configured.", 500

    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    return redirect(discord_auth_url())


@auth.route("/discord/callback")
def discord_callback():
    code = request.args.get("code")
    if not code:
        flash("Missing authorization code from Discord.", category="error")
        return redirect(url_for("auth.login"))

    token_data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
    }

    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if token_response.status_code != 200:
        flash("Failed to get access token from Discord.", category="error")
        return redirect(url_for("auth.login"))

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        flash("Discord did not return an access token.", category="error")
        return redirect(url_for("auth.login"))

    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if user_response.status_code != 200:
        flash("Failed to fetch user data from Discord.", category="error")
        return redirect(url_for("auth.login"))

    user_data = user_response.json()
    discord_id = user_data.get("id")
    username = user_data.get("username")
    discriminator = user_data.get("discriminator", "0")
    avatar = user_data.get("avatar")

    if not discord_id or not username:
        flash("Incomplete user data received from Discord.", category="error")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(discord_id=discord_id).first()
    if not user:
        user = User(
            discord_id=discord_id,
            username=username,
            discriminator=discriminator,
            avatar=avatar,
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    flash("Logged in with Discord!", category="success")
    return redirect(url_for("routes.home"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for("auth.login"))
