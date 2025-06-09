from flask import Blueprint, render_template
from flask_login import login_required, current_user

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return render_template("home.html", user=current_user)

@routes.route("/active_poll")
def active_poll():
    return render_template("home.html", user=current_user)
