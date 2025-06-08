
Akatsuki Flask Discord OAuth App
Overview

A Flask web application that uses Discord OAuth2 for user authentication. Users can log in with their Discord account, no passwords needed.
Prerequisites. For our Akatsuki-themed Discord Server related Website.

    Python 3.8 or higher

    Git

    Discord Developer account to create an OAuth application

Installation & Setup
1. Clone the repository

git clone https://github.com/yourusername/akatsuki.git
cd akatsuki

2. Create and activate a virtual environment
Linux/macOS

python3 -m venv venv
source venv/bin/activate

Windows (PowerShell)

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Set environment variables

Create a .env file in the project root or export variables in your shell.

Example .env:

DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret
DISCORD_REDIRECT_URI=http://localhost:2900/discord/callback
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

5. Initialize the database

Run Python shell and create tables:

flask shell
>>> from website import db
>>> db.create_all()
>>> exit()

6. Run the application

flask run --port=2900

Access the app at http://localhost:2900.
Usage

    Navigate to /auth/login to log in via Discord.

    After authorizing, you’ll be redirected back and logged in.

Notes

    Use a proper secret key in production.

    HTTPS recommended in production.

    Adjust Discord redirect URI in Discord Developer Portal accordingly.
