from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.forms.auth_forms import RegisterForm, LoginForm
from app.models.models import User, Order
from app import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Hash user password
        hashed_password = generate_password_hash(form.password.data)

        # Create new user object
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        try:
            # Save user to database
            db.session.add(user)
            db.session.commit()

            # Log user in immediately
            login_user(user)

            # Check pending standard order
            pending_order = session.pop('pending_order', None)
            if pending_order:
                order = Order(
                    user_id=user.id,
                    service_id=pending_order['service_id'],
                    company_name=pending_order['company_name'],
                    location=pending_order['location'],
                    email=pending_order['email'],
                    order_description=pending_order['order_description'],
                    status='pending'
                )
                db.session.add(order)
                db.session.commit()
                flash('Your order has been submitted successfully!', 'success')
                return redirect(url_for('main.home'))

            flash('Account created successfully!', 'success')
            return redirect(url_for('main.home'))

        except Exception as e:
            # Handle DB errors
            db.session.rollback()
            flash('An error occurred during registration.', 'danger')

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # Retrieve user by email
            user = User.query.filter_by(email=email).first()

            # Validate password
            if user and check_password_hash(user.password, password):
                login_user(user)

                # Check pending standard order
                pending_order = session.pop('pending_order', None)
                if pending_order:
                    new_order = Order(
                        user_id=user.id,
                        service_id=pending_order.get('service_id'),
                        company_name=pending_order.get('company_name'),
                        location=pending_order.get('location'),
                        email=pending_order.get('email'),
                        order_description=pending_order.get('order_description'),
                        status='pending'
                    )
                    db.session.add(new_order)
                    db.session.commit()
                    flash("Your pending order has been submitted.", "success")
                    return redirect(url_for('main.customerdashboard'))

                flash('Logged in successfully.', 'success')
                return redirect(url_for('main.customerdashboard'))

            else:
                flash('Invalid credentials')
        else:
            flash('Please fill in all required fields.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log out user
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
