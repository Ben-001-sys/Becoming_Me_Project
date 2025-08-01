from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import Order, Message, Project, User, CustomOrder
from datetime import datetime

main = Blueprint('main', __name__)

# Home page route
@main.route('/')
def home():
    return render_template('home.html')

# About Me page
@main.route('/about-me')
def about_me():
    return render_template('about_me.html')

# About Company page
@main.route('/about-company')
def about_company():
    return render_template('about_company.html')

# Contact page
@main.route('/contact')
def contact():
    return render_template('contact.html')

# Services overview
@main.route('/service')
def service():
    return render_template('service.html')

# Portfolio page
@main.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# Dashboard for authenticated users
@main.route('/dashboard')
@login_required
def customerdashboard():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    user_messages = Message.query.filter_by(email=current_user.email).order_by(Message.created_at.desc()).all()
    custom_orders = CustomOrder.query.filter_by(email=current_user.email).all()
    total_cost = sum(order.service.price for order in orders)

    return render_template(
        'customerdashboard.html',
        orders=orders,
        total_cost=total_cost,
        user_messages=user_messages,
        custom_orders=custom_orders
    )

# Tiered service pages
@main.route('/Security Configuration & Hardening Services')
def Secureservice():
    return render_template('Secureservice.html')

@main.route('/Vulnerability & Penetration Testing Services')
def Tester():
    return render_template('Tester.html')

@main.route('/ Awareness, Compliance & Training Services')
def Compliance():
    return render_template('Compliance.html')

# Standard service order route
@main.route('/place_order', methods=['POST'])
def place_order():
    service_id = request.form.get('service_id')
    company_name = request.form.get('company_name')
    location = request.form.get('location')
    email = request.form.get('email')
    order_description = request.form.get('order_description')

    if current_user.is_authenticated:
        # Authenticated user: save order
        order = Order(
            user_id=current_user.id,
            service_id=service_id,
            company_name=company_name,
            location=location,
            email=email,
            order_description=order_description,
            status='pending'
        )
        db.session.add(order)
        db.session.commit()
        flash('Order submitted successfully!', 'success')
        return redirect(url_for('main.home'))

    # Unauthenticated: save order in session
    session['pending_order'] = {
        'service_id': service_id,
        'company_name': company_name,
        'location': location,
        'email': email,
        'order_description': order_description
    }

    # Handle account existence
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('You already have an account. Please log in to complete your order.', 'info')
        return redirect(url_for('auth.login'))
    else:
        flash('Please register to complete your order.', 'info')
        return redirect(url_for('auth.register'))

# Submit new portfolio project
@main.route('/submit_project', methods=['POST'])
def submit_project():
    title = request.form.get('title')
    description = request.form.get('description')
    link = request.form.get('link')
    image = request.form.get('image')

    new_project = Project(
        title=title,
        description=description,
        link=link,
        image=image
    )

    db.session.add(new_project)
    db.session.commit()
    flash("Project submitted successfully!", "success")
    return redirect(url_for('main.about_company'))

# Handle contact form submission
@main.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    body = request.form.get('body')

    new_message = Message(
        name=name,
        email=email,
        subject=subject,
        body=body
    )

    db.session.add(new_message)
    db.session.commit()
    flash("Your message was sent successfully!", "success")
    return redirect(url_for('main.contact'))

# Custom order submission route
@main.route('/custom_order', methods=['POST'])
def custom_order():
    company = request.form.get('company_name')
    location = request.form.get('location')
    email = request.form.get('email')
    description = request.form.get('order_description')
    price_range = request.form.get('price_range')

    if current_user.is_authenticated:
        # Authenticated user: save custom order
        new_order = CustomOrder(
            company_name=company,
            location=location,
            email=email,
            order_description=description,
            price_range=price_range
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Your custom order has been submitted!', 'success')
        return redirect(url_for('main.service'))

    # Guest: store in session
    session['pending_neworder'] = {
        'company_name': company,
        'location': location,
        'email': email,
        'order_description': description,
        'price_range': price_range
    }

    # Redirect based on user account check
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('You already have an account. Please log in to complete your order.', 'info')
        return redirect(url_for('auth.login'))
    else:
        flash('Please register to complete your order.', 'info')
        return redirect(url_for('auth.register'))
