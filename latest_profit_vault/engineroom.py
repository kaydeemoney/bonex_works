from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, BooleanField,HiddenField, SelectField, DateField, TextAreaField, RadioField, FloatField, IntegerField
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

    id = db.Column(db.Integer, primary_key=True)
    erc20_address = db.Column(db.String(255))
    trc20_address = db.Column(db.String(255))
    sol_address = db.Column(db.String(255))
    bep20_address = db.Column(db.String(255))
    polygon_pos_address = db.Column(db.String(255))
    ton_address = db.Column(db.String(255))
    arbitrum_one_address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    user_id = db.Column(db.Integer,  nullable=False)
    reference_id = db.Column(db.Integer,  nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, etc.
    amount = db.Column(db.Float, nullable=False)
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
    estimated_time_of_sending = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)  # 0 = pending, 1 = rejected, 2 = confirmed

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
    erc20_address = StringField('ERC20 Address', validators=[Optional()])
    trc20_address = StringField('TRC20 Address', validators=[Optional()])
    sol_address = StringField('Solana Address', validators=[Optional()])
    bep20_address = StringField('BEP20 Address', validators=[Optional()])
    polygon_pos_address = StringField('Polygon POS Address', validators=[Optional()])
    ton_address = StringField('TON Address', validators=[Optional()])
    arbitrum_one_address = StringField('Arbitrum One Address', validators=[Optional()])
    submit = SubmitField('Save Wallet Addresses')



class InvestmentForm(FlaskForm):
    plan_id = HiddenField('Plan ID', validators=[DataRequired()])
    amount_invested = FloatField('Amount to Invest', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit Investment')


#these are the routes for pages pertaining to the landing page    
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template('admin_dashboard.html')
    


@app.route("/admin_investment_plan", methods=['GET', 'POST'])
def admin_investment_plan():
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

        investment=Investment_Plans(name=name, min_amount=min_amount,max_amount=max_amount, period_in_days=period_in_days,monthly_roi=monthly_roi,
                                    annual_roi=annual_roi, comment=comment)
        try:
            db.session.add(investment)
            db.session.commit()
            flash(f"Investment plan added!", 'success')
            return redirect(url_for('admin_investment_plan', form=form))
        except IntegrityError as e:
            db.session.rollback()
            flash("Investment plan added successfully!", "success")
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
                return redirect(url_for('user_dashboard', email=email))
            else:
                flash("Invalid user credentials", "danger")
                return render_template('login.html', form=form)
        else:
            flash("Email not found", "danger")
            print("email not found ")
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)





@app.route("/login_to_invest", methods=['GET', 'POST'])
def login_to_invest():
    form = LoginForm()  # Use the WTForm here
    user_id = request.args.get('user_id')
    if form.validate_on_submit():
        print("validated")
        email = form.email.data
        password = form.password.data
        got_user_email = User.query.filter_by(email=email).first()
        
        if got_user_email:
            print("email valid")
            user_id=got_user_email.user_id
            full_details = got_user_email
            if full_details.password_hash == password:  # For now, direct compare (should hash in production)
                print("going to dashboard")
                return redirect(url_for('submit_investment', user_id=user_id))
            else:
                flash("Invalid user credentials", "danger")
                return render_template('login.html', form=form)
        else:
            flash("Email not found", "danger")
            print("email not found ")
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)






@app.route("/admin_manage_referrals", methods=['GET', 'POST'])
def admin_manage_referrals():
    if request.method == 'POST':
        user_id = request.form.get('referee_id')

        current_user=User.query.filter_by(user_id=user_id).first()
        refree_id=current_user.registration_referral_id

        try:
            reward = Decimal(request.form.get('reward_amount', '0.00'))
        except InvalidOperation:
            flash("Invalid reward amount", 'danger')
            return redirect(url_for('admin_manage_referrals'))


        wallet = CryptoWallet.query.filter_by(user_id=refree_id).first()

        if wallet:
            wallet.total_balance_usd += reward
            wallet.total_earnings_usd += reward
            wallet.referral_earnings_usd += reward
            wallet.withdrawable_balance += reward
            wallet.last_updated = datetime.utcnow()
            user_id.registration_referral_id=None
            db.session.commit()
            flash(f"Reward of ${reward} confirmed for user {user_id}, refered by {refree_id} ", 'success')

            


        else:
            flash(f"Wallet not found for user {user_id}", 'danger')

        return redirect(url_for('admin_manage_referrals'))

    # GET: show all users with a valid referral
    referees = User.query.filter(User.registration_referral_id.isnot(None)).all()
    return render_template('admin_manage_referrals.html', referees=referees)


@app.route("/admin_wallet_addresses", methods=["GET", "POST"])
def admin_wallet_addresses():
    existing = AdminWalletAddress.query.first()
    form = AdminWalletAddressForm(obj=existing)

    if form.validate_on_submit():
        if existing:
            form.populate_obj(existing)
            flash("Wallet addresses updated successfully.", "success")
        else:
            new_entry = AdminWalletAddress()
            form.populate_obj(new_entry)
            db.session.add(new_entry)
            flash("Wallet addresses saved successfully.", "success")

        db.session.commit()
        return redirect(url_for("admin_wallet_addresses"))

    return render_template("admin_wallet_addresses.html", form=form)



@app.route("/admin_manage_deposits", methods=["GET", "POST"])
def admin_manage_deposits():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        action = request.form.get("action")

        deposit = Deposit.query.filter_by(user_id=user_id, status=0).first()

        if deposit:
            if action == "confirm":
                deposit.status = 2
                flash(f"Deposit by {user_id} confirmed.", "success")
            elif action == "reject":
                deposit.status = 1
                flash(f"Deposit by {user_id} rejected.", "danger")
            db.session.commit()
        else:
            flash(f"No pending deposit found for user {user_id}.", "warning")

        return redirect(url_for("admin_manage_deposits"))

    deposits = Deposit.query.filter_by(status=0).all()
    return render_template("admin_manage_deposits.html", deposits=deposits)


@app.route("/admin_users_list")
def admin_users_list():
    users = User.query.all()
    return render_template("users.html", users=users)

# Show edit form
@app.route("/edit_user/<string:user_id>", methods=["GET"])
def edit_user(user_id):
    user = User.query.filter_by(user_id=user_id).first_or_404()
    return render_template("edit_user.html", user=user)

# Handle user update
@app.route("/update_user/<string:user_id>", methods=["POST"])
def update_user(user_id):
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
        
        db.session.commit()
        flash("User updated successfully.", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Update failed: {str(e)}", "danger")

    return redirect(url_for("admin_users_list"))

# Delete user
@app.route("/delete_user/<string:user_id>", methods=["POST"])
def delete_user(user_id):
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
def user_dashboard():
    email = request.args.get('email', '').strip()
    if not email:
        return "Email parameter missing", 400

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
        inv.name = plan.name if plan else "Unknown Plan"
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
def investments():
    plans = Investment_Plans.query.all()
    return render_template('investments.html', plans=plans)

@app.route('/submit_investment/<int:plan_id>', methods=['GET', 'POST'])
def submit_investment(plan_id):
    plan = Investment_Plans.query.get_or_404(plan_id)
    form = InvestmentForm(plan_id=plan_id)  # Pre-fill plan_id

    if form.validate_on_submit():
        # Assuming you have a current_user system in place (like Flask-Login)
        user_id = 1  # Replace with current_user.id

        amount = form.amount_invested.data
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=plan.period_in_days)

        new_investment = User_Investments(
            user_id=user_id,
            plan_id=plan.id,
            amount_invested=amount,
            profit_earned=0.0,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            created_at=start_date
        )
        db.session.add(new_investment)
        db.session.commit()
        flash('Investment submitted successfully!', 'success')
        return redirect(url_for('investments'))

    return render_template('submit_investment.html', form=form, plan=plan)


if __name__=='__main__':
	app.run(debug=True)

