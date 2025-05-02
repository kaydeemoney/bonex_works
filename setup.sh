#!/bin/bash

# Set project root directory
PROJECT_NAME="profit_vault"
VENV_NAME="myenv"

echo "📁 Creating project structure for $PROJECT_NAME..."

# Create directory structure
mkdir -p $PROJECT_NAME/app/routes
mkdir -p $PROJECT_NAME/app/utils
mkdir -p $PROJECT_NAME/templates
mkdir -p $PROJECT_NAME/static/css
mkdir -p $PROJECT_NAME/static/js
mkdir -p $PROJECT_NAME/static/images
mkdir -p $PROJECT_NAME/migrations

# Create empty files
touch $PROJECT_NAME/app/__init__.py
touch $PROJECT_NAME/app/models.py
touch $PROJECT_NAME/app/utils/__init__.py
touch $PROJECT_NAME/app/utils/jwt_utils.py
touch $PROJECT_NAME/app/utils/decorators.py
touch $PROJECT_NAME/app/utils/background_tasks.py

for route in auth profile investments deposits withdrawals referrals transactions
do
  touch $PROJECT_NAME/app/routes/$route.py
done

touch $PROJECT_NAME/app/routes/__init__.py
touch $PROJECT_NAME/.env
touch $PROJECT_NAME/config.py
touch $PROJECT_NAME/run.py

# Add requirements.txt with basic Flask stack
cat <<EOF > $PROJECT_NAME/requirements.txt
Flask
Flask-RESTful
Flask-JWT-Extended
Flask-SQLAlchemy
Flask-Migrate
python-dotenv
mysqlclient
EOF

# Initialize __init__.py in app/
cat <<EOF > $PROJECT_NAME/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes import auth, profile, investments, deposits, withdrawals, referrals, transactions
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(investments.bp)
    app.register_blueprint(deposits.bp)
    app.register_blueprint(withdrawals.bp)
    app.register_blueprint(referrals.bp)
    app.register_blueprint(transactions.bp)

    return app
EOF

# Create run.py
cat <<EOF > $PROJECT_NAME/run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
EOF

# Create config.py
cat <<EOF > $PROJECT_NAME/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql://user:pass@localhost/profit_vault")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret")
EOF

echo "✅ Structure created."

# Optional: Create virtual environment and install dependencies
echo "📦 Installing dependencies into virtual environment ($VENV_NAME)..."
python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate
pip install -r $PROJECT_NAME/requirements.txt

echo "✅ Done! Navigate to $PROJECT_NAME and start coding!"
