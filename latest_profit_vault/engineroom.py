from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
import uuid, json
from config import Config
from datetime import datetime, timedelta
#this is for the validation efficiency of the wtf form you must always include it
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 300 * 1024  # 300KB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


#wtf form validation, for form input sending
csrf = CSRFProtect(app)
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = '7caa483b-e1c7-4a65-b901-queenofthecoast'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#model definition for the database



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    transaction_pin = db.Column(db.String(4), nullable=False)
    username = db.Column(db.String(4), nullable=False)
    referral_code = db.Column(db.String(4), nullable=False)
    referred_by = db.Column(db.String(4), nullable=False)
    is_admin = db.Column(db.String(4), nullable=False)
    user_id = db.Column(db.String(4), nullable=False)
    profile_picture_id = db.Column(db.String(4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Investment_Plans(db.Model):
    __tablename__ = 'investment_plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_amount = db.Column(db.Float, nullable=False)
    max_amount = db.Column(db.Float, nullable=False)
    period_in_days = db.Column(db.Integer, nullable=False)
    monthly_roi = db.Column(db.Float, nullable=False)
    annual_roi = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

class User_Investments(db.Model):
    __tablename__ = 'user_investments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    plan_id = db.Column(db.Integer, nullable=False)
    amount_invested = db.Column(db.Float, nullable=False)
    profit_earned = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Deposits(db.Model):
    __tablename__ = 'deposits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  nullable=False)
    amount = db.Column(db.Numeric(20, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    transaction_id = db.Column(db.String(100), nullable=False)
    network = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Withdrawal(db.Model):
    __tablename__ = 'withdrawal'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    wallet_address = db.Column(db.String(100), nullable=False)
    network = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Referral(db.Model):
    __tablename__ = 'Referral'  # match the raw SQL capitalization
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer,  nullable=False)
    referred_user_id = db.Column(db.Integer, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  nullable=False)
    reference_id = db.Column(db.Integer,  nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, etc.
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class wallet_settings(db.Model):
    __tablename__ = 'wallet_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    current_wallet_address = db.Column(db.Integer, nullable=False)
    former_wallet_address= db.Column(db.String(50), nullable=True)  # deposit, withdrawal, etc.
    amount = db.Column(db.Float, nullable=False)
    destination_wallet=db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=7, max=15)])
    gender = SelectField('Gender', choices=[
        ('', 'Select an option'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer Not To Say', 'Prefer Not To Say')
    ], validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])   
    username = StringField('Preferred Username', validators=[DataRequired()])
    referral_code = StringField('Referral Code (optional)', validators=[Optional()])
    referred_by = StringField('Referred By (optional)', validators=[Optional()]) 
    transaction_pin = StringField('Transaction Pin', validators=[DataRequired(), Length(min=4, max=4)])
    reenter_transaction_pin = StringField('Re-enter Transaction Pin', validators=[DataRequired(), EqualTo('transaction_pin', message="Pins must match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#these are the routes for pages pertaining to the landing page    
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        print("form is validated")
        # Handle file upload
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            print("allowed files working")
            try:
                # Process the file
                joint_id = uuid.uuid4()
                profile_pic_name = joint_id
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{profile_pic_name}.{filename.rsplit('.', 1)[1]}")
                file.save(filepath)

                # Image processing: Make the image round
                img = Image.open(filepath)
                img = img.convert("RGBA")
                size = (200, 200)
                img = img.resize(size, Image.Resampling.LANCZOS)
                mask = Image.new("L", size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, size[0], size[1]), fill=255)
                img.putalpha(mask)

                if filename.rsplit('.', 1)[1].lower() in ['jpeg', 'jpg']:
                    img = img.convert("RGB")
                    filepath = os.path.splitext(filepath)[0] + ".jpg"
                    img.save(filepath, "JPEG")
                else:
                    img.save(filepath, "PNG")
            except Exception as e:
                flash(f"Error processing profile pic: {str(e)}", "danger")
                print("error processing image")
                return render_template('signup.html', form=form)
        else:
            flash("Error uploading profile pic. Please upload a valid image.", "danger")
            print("error uploading")
            return render_template('signup.html', form=form)

        # Get form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        mobile = form.mobile.data
        gender = form.gender.data
        country = form.country.data
        state = form.state.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        username = form.username.data
        referral_code = form.referral_code.data
        referred_by = form.referred_by.data
        transaction_pin = form.transaction_pin.data
        reenter_transaction_pin = form.reenter_transaction_pin.data
        user_id = profile_pic_name
        created_at = datetime.now()

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            print("password dont match")
            return render_template('signup.html', form=form)
        if transaction_pin != reenter_transaction_pin:
            print("pin dont match")
            flash("Transaction pins do not match!", "danger")
            return render_template('signup.html', form=form)

        # Save user to database
        user = User(
            first_name=first_name, last_name=last_name, email=email, mobile=mobile, gender=gender,
            country=country, state=state, password_hash=password, transaction_pin=transaction_pin,
            username=username, referral_code=referral_code, referred_by=referred_by, is_admin=None,
            user_id=user_id, profile_picture_id=user_id, created_at=created_at
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Account created for {first_name} {last_name}!", 'success')
            print("account created")
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            error_message = str(e.orig)

            # Check if the error is about the email uniqueness
            if 'email' in error_message:
                flash('An account with this email already exists.', 'error')

            # You can extend to other fields if you later make them UNIQUE
            elif 'username' in error_message:
                flash('This username is already taken. Please choose another.', 'error')
            elif 'mobile' in error_message:
                flash('This mobile number is already registered.', 'error')

            else:
                flash('An error occurred during registration. Please try again.', 'error')
            

    else:
        print(form.errors) 
    
    # If GET request or form validation failed, show the form
    return render_template('signup.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Use the WTForm here
    if form.validate_on_submit():
        print("validated")
        email = form.email.data
        password = form.password.data
        got_user_email = User.query.filter_by(email=email).first()
        if got_user_email:
            print("email valid")
            full_details = got_user_email
            if full_details.password_hash == password:  # For now, direct compare (should hash in production)
                print("going to dashboard")
                return redirect(url_for('index', email=email))
            else:
                flash("Invalid user credentials", "danger")
                return render_template('login.html', form=form)
        else:
            flash("Email not found", "danger")
            print("email not found ")
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

if __name__=='__main__':
	app.run(debug=True)

