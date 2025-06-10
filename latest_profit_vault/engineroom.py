from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, BooleanField,HiddenField, SelectField, DecimalField, DateField,DateTimeField, TextAreaField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange
import uuid, json
from config import Config
from datetime import datetime, timedelta
#this is for the validation efficiency of the wtf form you must always include it
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
from decimal import Decimal, InvalidOperation
import string
import secrets
from functools import wraps



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



class AdminWalletAddress(db.Model):
    __tablename__ = 'admin_wallet_addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    network = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)

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
    username = db.Column(db.String(20), nullable=False)
    registration_referral_id = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.String(4), nullable=True)
    user_id = db.Column(db.String(100), nullable=False)
    profile_picture_id = db.Column(db.String(100), nullable=False)
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
    comment = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    plan_id = db.Column(db.String(100))

    
class UserAdminMessage(db.Model):
    __tablename__ = 'user_admin_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    sender = db.Column(db.Enum('user', 'admin'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



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

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class CryptoWallet(db.Model):
    __tablename__ = 'crypto_wallet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), unique=True, nullable=True)
    total_balance_usd = db.Column(db.Float)
    total_earnings_usd = db.Column(db.Float)
    total_invested_usd = db.Column(db.Float)
    referral_earnings_usd = db.Column(db.Float)
    active_investments_count = db.Column(db.Integer)
    last_investment_date = db.Column(db.DateTime, nullable=True)
    roi_percentage = db.Column(db.Float)
    withdrawable_balance = db.Column(db.Float)
    last_login_date = db.Column(db.DateTime, nullable=True)
    account_status = db.Column(db.String(20), default='Active')
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Deposit(db.Model):
    __tablename__ = 'deposits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    amount_deposited = db.Column(db.Numeric(10, 2), nullable=False)
    senders_wallet_address = db.Column(db.String(255), nullable=False)
    senders_wallet_network = db.Column(db.String(100), nullable=False)
    estimated_time_of_sending = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    comment = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)  # 0 = pending, 1 = rejected, 2 = confirmed



class ContactAdminForm(FlaskForm):
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send')

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
    registration_referral_id = StringField('Referral Code (optional)', validators=[Optional()])
    transaction_pin = StringField('Transaction Pin', validators=[DataRequired(), Length(min=4, max=4)])
    reenter_transaction_pin = StringField('Re-enter Transaction Pin', validators=[DataRequired(), EqualTo('transaction_pin', message="Pins must match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class InvestmentPlanForm(FlaskForm):
    name = StringField("Plan Name", validators=[DataRequired()])
    
    min_amount = FloatField("Minimum Amount ($)", validators=[
        DataRequired(), NumberRange(min=0)
    ])
    max_amount = FloatField("Maximum Amount ($)", validators=[
        DataRequired(), NumberRange(min=0)
    ])
    
    period_in_days = IntegerField("Period (Days)", validators=[
        DataRequired(), NumberRange(min=1)
    ])
    monthly_roi = FloatField("Monthly ROI (%)", validators=[
        DataRequired(), NumberRange(min=0)
    ])
    annual_roi = FloatField("Annual ROI (%)", validators=[
        DataRequired(), NumberRange(min=0)
    ])
    
    comment = TextAreaField("Comment", validators=[Optional()])
    
    submit = SubmitField("Save Plan")



class AdminWalletAddressForm(FlaskForm):
    submit = SubmitField("Save")

class InvestmentForm(FlaskForm):
    plan_id = HiddenField('Plan ID', validators=[DataRequired()])
    amount_invested = FloatField('Amount to Invest', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit Investment')


class DepositForm(FlaskForm):
    amount_deposited = DecimalField('Enter Amount', validators=[DataRequired()])
    senders_wallet_network = SelectField('Select USDT Network', validators=[DataRequired()],
        choices=[
            ('ERC20', 'ERC20'),
            ('TRC20', 'TRC20'),
            ('SOL', 'SOL'),
            ('BEP20', 'BEP20'),
            ('Polygon_POS', 'Polygon_POS'),
            ('TON', 'TON'),
            ('Arbitrum_One', 'Arbitrum_One'),
        ])
    senders_wallet_address = StringField('Sender Wallet Address', validators=[DataRequired()])
    comment = TextAreaField('Comment (Optional)')


class CryptoWalletForm(FlaskForm):
    user_id = StringField("User ID", validators=[Optional(), Length(max=100)])
    total_balance_usd = FloatField("Total Balance (USD)", validators=[Optional()])
    total_earnings_usd = FloatField("Total Earnings (USD)", validators=[Optional()])
    total_invested_usd = FloatField("Total Invested (USD)", validators=[Optional()])
    referral_earnings_usd = FloatField("Referral Earnings (USD)", validators=[Optional()])
    active_investments_count = IntegerField("Active Investments Count", validators=[Optional()])
    last_investment_date = DateTimeField("Last Investment Date", validators=[Optional()], format='%Y-%m-%d %H:%M:%S')
    roi_percentage = FloatField("ROI Percentage", validators=[Optional()])
    withdrawable_balance = FloatField("Withdrawable Balance", validators=[Optional()])
    last_login_date = DateTimeField("Last Login Date", validators=[Optional()], format='%Y-%m-%d %H:%M:%S')
    account_status = StringField("Account Status", validators=[Optional(), Length(max=20)])
    date_joined = DateTimeField("Date Joined", validators=[Optional()], format='%Y-%m-%d %H:%M:%S')
    last_updated = DateTimeField("Last Updated", validators=[Optional()], format='%Y-%m-%d %H:%M:%S')

    submit = SubmitField("Submit")




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash("You must be logged in to view this page", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function




def get_profile_picture():
    email=session.get("email")

    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not found", 404

    user_id = user.user_id
    is_admin = user.is_admin
    profile_picture = "noname.png"
     # Profile picture logic
    uploads_folder = os.path.join(app.static_folder, 'uploads')
    if os.path.isdir(uploads_folder) and user.profile_picture_id:
        for file_name in os.listdir(uploads_folder):
            if file_name.startswith(user.profile_picture_id):
                profile_picture = file_name
                break
    return profile_picture


#these are the routes for pages pertaining to the landing page    
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')
    


@app.route("/admin_investment_plan", methods=['GET', 'POST'])
@login_required
def admin_investment_plan():
    email=session.get("email")
    
    form = InvestmentPlanForm()
    if form.validate_on_submit():
        print("form is validated")
        name = form.name.data
        min_amount=form.min_amount.data
        max_amount=form.max_amount.data
        period_in_days=form.period_in_days.data
        monthly_roi=form.monthly_roi.data
        annual_roi=form.annual_roi.data
        comment=form.comment.data

        plan_id= str(uuid.uuid4())

        investment=Investment_Plans(name=name, min_amount=min_amount,max_amount=max_amount, period_in_days=period_in_days,monthly_roi=monthly_roi,
                                    annual_roi=annual_roi, comment=comment, plan_id=plan_id)
        try:
            db.session.add(investment)
            db.session.commit()
            flash(f"Investment plan added!", 'success')
            return redirect(url_for('admin_investment_plan', form=form))
        except IntegrityError as e:
            db.session.rollback()
            flash("Error: Could not add investment plan. It may already exist or have bad data.", "danger")
    return render_template("admin_investment_plan.html", form=form)

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
        registration_referral_id = form.registration_referral_id.data
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
            username=username, registration_referral_id=registration_referral_id, is_admin=None,
            user_id=user_id, profile_picture_id=user_id, created_at=created_at
        )
        try:
            db.session.add(user)
            user_account=CryptoWallet(user_id=user_id)
            db.session.add(user_account)
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




@app.route("/deposit", methods=['GET', 'POST'])
@login_required
def deposit():
    form = DepositForm()
    email=session.get('email')
    profile_picture=session.get("profile_picture")
    user=User.query.filter_by(email=email).first()
    if not user:
        flash("Invalid session. Please log in again.", "danger")
        return redirect(url_for('login'))
    user_id=user.user_id
    print(user_id)
    if form.validate_on_submit():  
        print("validated on submit")
        flash('Requesting Deposit Information.', 'success')
        return redirect(url_for('user_deposit_confirmation', user_id=user_id, 
                                amount_deposited=form.amount_deposited.data,
                                user=user, profile_picture=profile_picture,
                                senders_wallet_address=form.senders_wallet_address.data, 
                                senders_wallet_network=form.senders_wallet_network.data, comment=form.comment.data, status=0))
    else:
        print(form.errors)
    return render_template('deposit.html', form=form, user=user, profile_picture=profile_picture)


@app.route("/user_deposit_confirmation", methods=['GET', 'POST'])
@login_required
def user_deposit_confirmation():
    email=session.get('email')
    profile_picture=session.get('profile_picture')
    if request.method == 'POST':
        if request.form['action'] == 'confirm':
            deposit = Deposit(
                user_id=request.form['user_id'],
                amount_deposited=request.form['amount_deposited'],
                senders_wallet_address=request.form['senders_wallet_address'],
                senders_wallet_network=request.form['senders_wallet_network'],
                estimated_time_of_sending=request.form['estimated_time_of_sending'],
                comment=request.form.get('comment', ''),
                status=0
            )

            transaction_copy= Transaction(user_id=request.form['user_id'],
                                          type="Deposit", amount=request.form['amount_deposited'],
                                          status="Pending",
                                          description=request.form.get('comment', ''))
            
            db.session.add(deposit)
            db.session.add(transaction_copy)
            db.session.commit()
            flash("✅ Deposit successfully confirmed and submitted. Awaiting admin review.", "success")
            return redirect(url_for('deposit_success'))

        elif request.form['action'] == 'reject':
            flash("❌ Deposit request was cancelled.", "info")
            return redirect(url_for('deposit_cancelled'))

    # GET request
    user_id = request.args.get('user_id')
    user=User.query.filter_by(user_id=user_id).first()
    amount_deposited = request.args.get('amount_deposited')
    senders_wallet_address = request.args.get('senders_wallet_address')
    senders_wallet_network = request.args.get('senders_wallet_network')
    estimated_time_of_sending = request.args.get('estimated_time_of_sending')
    comment = request.args.get('comment')
    status = request.args.get('status')



    reciever_address_wallet = AdminWalletAddress.query.filter_by(network=senders_wallet_network).first().address

    reciever_address = reciever_address_wallet if reciever_address_wallet else None
    if not reciever_address:
        flash("Invalid wallet network selected.", "danger")
        return redirect(url_for('deposit'))
    return render_template('user_deposit_confirmation.html',
                           user_id=user_id, user=user, profile_picture=profile_picture,
                           amount_deposited=amount_deposited,
                           senders_wallet_address=senders_wallet_address,
                           senders_wallet_network=senders_wallet_network,
                           estimated_time_of_sending=estimated_time_of_sending,
                           comment=comment,
                           status=status,
                           reciever_address=reciever_address)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        got_user_email = User.query.filter_by(email=email).first()

        if got_user_email:
            if got_user_email.password_hash == password:  # Plain text comparison
                session['email'] = email  # Store email in session
                profile_picture=get_profile_picture()

                session['profile_picture']=profile_picture

                if got_user_email.is_admin:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))
            else:
                flash("Invalid password", "danger")
        else:
            flash("Email not found", "danger")

    return render_template('login.html', form=form)

@app.route("/admin_manage_referrals", methods=['GET', 'POST'])
@login_required
def admin_manage_referrals():
    email=session.get('email')
    if request.method == 'POST':
        user_id = request.form.get('referee_id')  # This is the referree
        try:
            reward = Decimal(request.form.get('reward_amount', '0.00'))
        except InvalidOperation:
            flash("Invalid reward amount", 'danger')
            return redirect(url_for('admin_manage_referrals'))

        referee = User.query.filter_by(user_id=user_id).first()

        if not referee or not referee.registration_referral_id:
            flash("Referee not found or has no referral", 'danger')
            return redirect(url_for('admin_manage_referrals'))

        referrer = User.query.filter_by(user_id=referee.registration_referral_id).first()
        if not referrer:
            flash("Referrer not found", 'danger')
            return redirect(url_for('admin_manage_referrals'))

        wallet = CryptoWallet.query.filter_by(user_id=referrer.user_id).first()
        if wallet:
            reward_float = float(reward)
            wallet.total_balance_usd = (wallet.total_balance_usd or 0) + reward_float
            wallet.total_earnings_usd = (wallet.total_earnings_usd or 0) + reward_float
            wallet.referral_earnings_usd = (wallet.referral_earnings_usd or 0) + reward_float
            wallet.withdrawable_balance = (wallet.withdrawable_balance or 0) + reward_float
            wallet.last_updated = datetime.utcnow()

            referee.registration_referral_id = None  # Mark referral as processed
            db.session.commit()
            flash(f"Reward of ${reward} confirmed for {referrer.email}, referred by {referee.email}", 'success')


            transaction_copy= Transaction(user_id=referrer.user_id,
                                          type="Referral", amount=reward_float,
                                          status="Complete",
                                          description=f"referred by {referee.email}")
            
            db.session.add(transaction_copy)
            db.session.commit()
           
        
        
        else:
            flash(f"Wallet not found for referrer {referrer.email}", 'danger')

        return redirect(url_for('admin_manage_referrals'))

    # GET: show all referees with valid referrer
    referees = User.query.filter(User.registration_referral_id.isnot(None)).all()

    # attach referrer email for template display
    data = []
    for user in referees:
        referrer = User.query.filter_by(user_id=user.registration_referral_id).first()
        data.append({
            'referee': user,
            'referrer_email': referrer.email if referrer else 'Unknown'
        })

    return render_template('admin_manage_referrals.html', referees=data)

@app.route("/admin_wallet_addresses", methods=["GET", "POST"])
@login_required
def admin_wallet_addresses():
    email=session.get('email')
    form = AdminWalletAddressForm()
    records = AdminWalletAddress.query.order_by(AdminWalletAddress.network).all()

    if request.method == "POST":
        for record in records:
            new_address = request.form.get(record.network)
            if new_address and new_address != record.address:
                record.address = new_address
        db.session.commit()
        flash("Wallet addresses updated successfully.", "success")
        return redirect(url_for("admin_wallet_addresses"))

    return render_template("admin_wallet_addresses.html", form=form, records=records)

@app.route("/admin_manage_deposits", methods=["GET", "POST"])
@login_required
def admin_manage_deposits():
    email=session.get('email')
    if request.method == "POST":
        user_id = request.form.get("user_id")
        action = request.form.get("action")

        deposit = Deposit.query.filter_by(user_id=user_id, status=0).first()
        wallet = CryptoWallet.query.filter_by(user_id=user_id).first()
        transaction = Transaction.query.filter_by(user_id=user_id, type="deposit", status="pending").first()

        if deposit:
            if action == "confirm":
                if wallet:
                    wallet.total_balance_usd = (wallet.total_balance_usd or 0) + float(deposit.amount_deposited)
                    wallet.withdrawable_balance = (wallet.withdrawable_balance or 0) + float(deposit.amount_deposited)

                if transaction:
                    transaction.status = "completed"

                db.session.delete(deposit)
                db.session.commit()

                flash(f"Deposit by {user_id} confirmed and wallet updated.", "success")

            elif action == "reject":
                if transaction:
                    transaction.status = "rejected"

                db.session.delete(deposit)
                db.session.commit()

                flash(f"Deposit by {user_id} rejected and removed.", "danger")

            return redirect(url_for("admin_manage_deposits"))
        else:
            flash("No matching pending deposit found.", "warning")
            return redirect(url_for("admin_manage_deposits"))

    # For display: combine deposit and email in one structure
    pending_deposits = Deposit.query.filter_by(status=0).all()
    deposit_data = []

    for deposit in pending_deposits:
        user = User.query.filter_by(user_id=deposit.user_id).first()
        email = user.email if user else "Unknown"
        deposit_data.append({"deposit": deposit, "email": email})

    return render_template("admin_manage_deposits.html", deposit_data=deposit_data)

@app.route("/admin_users_list")
@login_required
def admin_users_list():
    email=session.get('email')
    users = User.query.all()
    return render_template("users.html", users=users)

# Show edit form
@app.route("/edit_user/<string:user_id>", methods=["GET"])
@login_required
def edit_user(user_id):
    email=session.get('email')
    user = User.query.filter_by(user_id=user_id).first_or_404()
    bank=CryptoWallet.query.filter_by(user_id=user_id).first_or_404()
    return render_template("edit_user.html", user=user, bank=bank)


@app.route("/transaction_history")
@login_required
def transaction_history():
    email=session.get('email')
    profile_picture=session.get('profile_picture')
    user=User.query.filter_by(email=email).first()
    user_id=User.query.filter_by(email=email).first().user_id
    transaction_log=Transaction.query.filter_by(user_id=user_id).all()
    return render_template("transaction_history.html",user=user, profile_picture=profile_picture, transaction_log=transaction_log)




# Show edit form
@app.route("/user_profile", methods=["GET"])
@login_required
def user_profile():
    email=session.get('email')
    profile_picture=session.get('profile_picture')
    user = User.query.filter_by(email=email).first_or_404()
    return render_template("user_profile.html", user=user, profile_picture=profile_picture)


# Handle user update
@app.route("/user_profile_updating", methods=["POST"])
@login_required
def user_profile_updating():
    email=session.get('email')
    user = User.query.filter_by(email=email).first_or_404()
    try:
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.mobile = request.form['mobile']
        user.gender = request.form['gender']
        user.country = request.form['country']
        user.state = request.form['state']
        user.username = request.form['username']
        

        pincode=request.form['transaction_pin']

        if pincode:
            user.transaction_pin = request.form['transaction_pin']
        
        db.session.commit()
        flash("User updated successfully.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Update failed: {str(e)}", "danger")

    return redirect(url_for("user_profile"))







# Handle user update
@app.route("/update_user/<string:user_id>", methods=["POST"])
@login_required
def update_user(user_id):
    email=session.get('email')
    user = User.query.filter_by(user_id=user_id).first_or_404()
    try:
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.mobile = request.form['mobile']
        user.gender = request.form['gender']
        user.country = request.form['country']
        user.state = request.form['state']
        user.username = request.form['username']
        user.transaction_pin = request.form['transaction_pin']
        user.registration_referral_id = request.form['registration_referral_id']
        user.is_admin = request.form.get('is_admin')
        user.password_hash = request.form.get('password_hash')
        
        db.session.commit()
        flash("User updated successfully.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Update failed: {str(e)}", "danger")

    return redirect(url_for("admin_users_list"))

# Delete user
@app.route("/delete_user/<string:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    email=session.get('email')
    user = User.query.filter_by(user_id=user_id).first_or_404()
    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Deletion failed: {str(e)}", "danger")

    return redirect(url_for("admin_users_list"))



@app.route("/user_dashboard")
@login_required
def user_dashboard():
    email=session.get("email")
    
    if not email:
        return "Email parameter missing", 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not found", 404

    user_id = user.user_id
    is_admin = user.is_admin
    
    profile_picture=get_profile_picture()
    # Admin logic
    if is_admin:
        return render_template("admin_dashboard.html", user=user, profile_picture=profile_picture)

    wallet = CryptoWallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        return "Wallet not found", 404

    # Active & Completed investments
    active_investments = User_Investments.query.filter_by(user_id=user_id, is_active=1).all()
    completed_investments = User_Investments.query.filter_by(user_id=user_id, is_active=0).all()

    def calculate_progress(start_date, end_date):
        now = datetime.utcnow()
        total_duration = (end_date - start_date).total_seconds()
        elapsed = (now - start_date).total_seconds()
        percent = (elapsed / total_duration) * 100 if total_duration > 0 else 100
        return round(min(max(percent, 0), 100), 2)

    # Attach plan details to investments
    for inv in active_investments + completed_investments:
        plan = Investment_Plans.query.filter_by(plan_id=inv.plan_id).first()
        inv.name = plan.name if plan else "Delisted Plan"
        inv.monthly_roi = plan.monthly_roi if plan else 0
        inv.annual_roi = plan.annual_roi if plan else 0
        inv.progress_percent = (
            calculate_progress(inv.start_date, inv.end_date) 
            if inv.is_active and inv.start_date and inv.end_date else 100
        )
        inv.end_date_str = inv.end_date.strftime('%d/%m/%Y') if inv.end_date else 'N/A'

    return render_template("user_dashboard.html",
                           user=user,
                           profile_picture=profile_picture,
                           wallet=wallet,
                           active_investments=active_investments,
                           completed_investments=completed_investments)



@app.route('/investments')
@login_required
def investments():
    email=session.get("email")
    profile_picture=session.get("profile_picture")
    user=User.query.filter_by(email=email).first()
    user_id=User.query.filter_by(email=email).first().user_id
    print(user_id)
    print(email)
    plans = Investment_Plans.query.all()
    return render_template('investments.html',user=user,profile_picture=profile_picture, plans=plans, user_id=user_id)



@app.route('/submit_investment', methods=['GET', 'POST'])
@login_required
def submit_investment():
    email = session.get("email")
    profile_picture=session.get('profile_picture')
    if not email:
        return "Email parameter missing", 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return "User not found", 404

    user_id = user.user_id  # Keep this from session!
    wallet = CryptoWallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        return "Wallet not found", 404

    plan_id = request.args.get('plan_id')
    user_id_arg = request.args.get('user_id')  # Avoid overwriting session user_id

    if not plan_id or not user_id_arg:
        flash("Plan ID and User ID are required.", "danger")
        return redirect(url_for('plans'))

    balance = float(wallet.withdrawable_balance or 0.0)

    form = InvestmentForm()
    form.plan_id.data = plan_id

    plan = Investment_Plans.query.filter_by(plan_id=plan_id).first()
    if not plan:
        flash("Invalid plan selected.", "danger")
        return redirect(url_for('plans'))

    if form.validate_on_submit():
        amount = form.amount_invested.data

        if amount < plan.min_amount or amount > plan.max_amount:
            flash(f"Amount must be between ${plan.min_amount} and ${plan.max_amount}.", "danger")
            return render_template('submit_investment.html', form=form, plan=plan, wallet=wallet, user=user, profile_picture=profile_picture)
        elif amount > balance:
            flash("Amount exceeds your available balance.", "danger")
            return render_template('submit_investment.html', profile_picture=profile_picture,
                                   form=form, plan=plan, wallet=wallet, user=user)

        # Process investment
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=plan.period_in_days)

        new_investment = User_Investments(
            user_id=user_id,
            plan_id=plan.plan_id,
            amount_invested=amount,
            profit_earned=0.0,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            created_at=start_date
        )

        db.session.add(new_investment)

        wallet.total_balance_usd = float(wallet.total_balance_usd or 0.0) - amount
        wallet.total_invested_usd = float(wallet.total_invested_usd or 0.0) + amount
        wallet.active_investments_count = float(wallet.active_investments_count or 0.0) + 1
        wallet.last_investment_date = datetime.utcnow()
        wallet.withdrawable_balance = float(wallet.withdrawable_balance or 0.0) - amount
        
        transaction_copy= Transaction(user_id=user_id,
                                          type="Investment", amount=amount,
                                          status="Completed",
                                          description="Investments added")
        db.session.add(transaction_copy)
        db.session.commit()
        flash("Investment made successfully!", "success")
        return redirect(url_for('investments'))

    return render_template('submit_investment.html', form=form, plan=plan, wallet=wallet, user=user, profile_picture=profile_picture)

#with this we can easily use {{ email }} in jinja, but for routes it will still be session.get(email)
@app.context_processor
def inject_email():
    return dict(email=session.get('email'))




@app.route('/admin_manage_investments')
@login_required
def admin_manage_investments():
    email=session.get("email")
    plans = Investment_Plans.query.all()
    return render_template('admin_manage_investments.html', plans=plans)

@app.route('/delete_plan')
@login_required
def delete_plan():
    email=session.get("email")
    plan_id=request.args.get('plan_id')
    plan_to_delete=Investment_Plans.query.filter_by(plan_id=plan_id).first()
    db.session.delete(plan_to_delete)
    db.session.commit()
    plans = Investment_Plans.query.all()
    return render_template('admin_manage_investments.html', plans=plans)




@app.route("/deposit_success")
@login_required
def deposit_success():
    email=session.get('email')
    return render_template("deposit_success.html")

@app.route("/deposit_cancelled")
@login_required
def deposit_cancelled():
    email=session.get('email')
    return render_template("deposit_cancelled.html")



@app.route("/user_referral_page")
@login_required
def user_referral_page():
    email=session.get('email')
    profile_picture=session.get('profile_picture')
    user=User.query.filter_by(email=email).first()
    user_id=User.query.filter_by(email=email).first().user_id
    total_earnings=CryptoWallet.query.filter_by(user_id=user_id).first().referral_earnings_usd
    referral_link=user_id
    transaction_log=Transaction.query.filter_by(user_id=user_id, type="Referral").all()
    return render_template("user_referral_page.html", user_id=user_id, user=user,profile_picture=profile_picture, total_earnings=total_earnings, referral_link=referral_link,
                           transaction_log=transaction_log)


@app.route("/edit_crypto_wallet", methods=['GET', 'POST'])
@login_required
def edit_crypto_wallet():
    email=session.get('email')
    form = CryptoWalletForm()

    user_id = request.args.get('user_id') or form.user_id.data

    if not user_id:
        flash("User ID is required to edit a wallet.", "danger")
        return render_template("edit_crypto_wallet.html", form=form)

    wallet = CryptoWallet.query.filter_by(user_id=user_id).first()

    if not wallet:
        flash("No wallet found for the provided User ID.", "danger")
        return render_template("edit_crypto_wallet.html", form=form)

    if request.method == 'GET':
        # Pre-fill form with existing data
        form.user_id.data = wallet.user_id
        form.total_balance_usd.data = wallet.total_balance_usd
        form.total_earnings_usd.data = wallet.total_earnings_usd
        form.total_invested_usd.data = wallet.total_invested_usd
        form.referral_earnings_usd.data = wallet.referral_earnings_usd
        form.active_investments_count.data = wallet.active_investments_count
        form.last_investment_date.data = wallet.last_investment_date
        form.roi_percentage.data = wallet.roi_percentage
        form.withdrawable_balance.data = wallet.withdrawable_balance
        form.last_login_date.data = wallet.last_login_date
        form.account_status.data = wallet.account_status
        form.date_joined.data = wallet.date_joined
        form.last_updated.data = wallet.last_updated

    elif form.validate_on_submit():
        # Update wallet fields from form
        wallet.total_balance_usd = form.total_balance_usd.data
        wallet.total_earnings_usd = form.total_earnings_usd.data
        wallet.total_invested_usd = form.total_invested_usd.data
        wallet.referral_earnings_usd = form.referral_earnings_usd.data
        wallet.active_investments_count = form.active_investments_count.data
        wallet.last_investment_date = form.last_investment_date.data
        wallet.roi_percentage = form.roi_percentage.data
        wallet.withdrawable_balance = form.withdrawable_balance.data
        wallet.last_login_date = form.last_login_date.data
        wallet.account_status = form.account_status.data
        wallet.date_joined = form.date_joined.data
        wallet.last_updated = form.last_updated.data or datetime.utcnow()

        db.session.commit()
        flash("Wallet updated successfully.", "success")
        return redirect(url_for('edit_crypto_wallet', user_id=user_id))

    return render_template("edit_crypto_wallet.html", form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("You've been logged out", "success")
    return redirect(url_for('login'))

    
if __name__=='__main__':
	app.run(debug=True)

