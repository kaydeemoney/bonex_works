from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize app, db, migration, JWT, and CORS
app = Flask(__name__)
CORS(app)

# Configuring the app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register Blueprints (Routes)
from app.routes.auth import auth_bp
from app.routes.profile import profile_bp
from app.routes.investments import investments_bp
from app.routes.deposits import deposits_bp
from app.routes.withdrawals import withdrawals_bp
from app.routes.referrals import referrals_bp
from app.routes.transactions import transactions_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(investments_bp, url_prefix='/investments')
app.register_blueprint(deposits_bp, url_prefix='/deposits')
app.register_blueprint(withdrawals_bp, url_prefix='/withdrawals')
app.register_blueprint(referrals_bp, url_prefix='/referrals')
app.register_blueprint(transactions_bp, url_prefix='/transactions')

# Other configurations can go here
