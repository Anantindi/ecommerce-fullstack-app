from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import Product, User, CartItem
from .forms import LoginForm, RegisterForm
from . import db, mail
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    selected_brands = request.args.getlist('brand')
    selected_price = request.args.get('price')
    search_query = request.args.get('search', '').strip().lower()

    query = Product.query

    if selected_brands:
        query = query.filter(Product.brand.in_(selected_brands))

    if selected_price:
        if selected_price == '0-10000':
            query = query.filter(Product.price <= 10000)
        elif selected_price == '10000-25000':
            query = query.filter(Product.price > 10000, Product.price <= 25000)
        elif selected_price == '25000-50000':
            query = query.filter(Product.price > 25000, Product.price <= 50000)
        elif selected_price == '50000+':
            query = query.filter(Product.price > 50000)

    if search_query:
        query = query.filter(
            (Product.name.ilike(f"%{search_query}%")) |
            (Product.brand.ilike(f"%{search_query}%")) |
            (Product.description.ilike(f"%{search_query}%"))
        )

    products = query.all()
    return render_template('index.html', products=products)

@main.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'warning')
            return redirect(url_for('main.register'))
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))

@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        if existing_item.quantity < existing_item.product.stock:
            existing_item.quantity += 1
        else:
            flash('You cannot add more than available stock.', 'warning')
            return redirect(request.referrer or url_for('main.cart'))
    else:
        product = Product.query.get_or_404(product_id)
        if product.stock < 1:
            flash('This product is out of stock.', 'danger')
            return redirect(request.referrer or url_for('main.index'))
        new_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(new_item)

    db.session.commit()

    # Correct redirection: only show flash if you came from product page exactly
    referrer = request.referrer or ""
    if f"/product/{product_id}" in referrer:
        flash('Item added to cart!', 'success')
        return redirect(url_for('main.product', product_id=product_id))

    return redirect(url_for('main.cart'))


@main.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
    return redirect(request.referrer or url_for('main.cart'))

@main.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@main.route('/buy_now/<int:product_id>')
@login_required
def buy_now(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('checkout.html', product=product)

@main.route('/checkout', methods=['GET'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@main.route('/confirm_order', methods=['POST'])
@login_required
def confirm_order():
    email = request.form.get("email")
    product_id = request.form.get("product_id")

    if not email:
        flash("Please enter a valid email address.", "danger")
        return redirect(request.referrer or url_for("main.index"))

    # -------------------------
    # For Buy Now (Single Product)
    # -------------------------
    if product_id:
        product = Product.query.get_or_404(product_id)
        if product.stock > 0:
            product.stock -= 1
            db.session.commit()

            msg = Message("Order Confirmation",
                          sender="hulkandtheagentsofsmash2@gmail.com",
                          recipients=[email])
            msg.body = (
                f"Your order for {product.name} has been confirmed!\n\n"
                f"Order Details:\n"
                f"- Product: {product.name}\n"
                f"- Brand: {product.brand}\n"
                f"- Price: ₹{product.price}\n"
                f"Thank you for shopping with Phone-Verse!"
            )
            mail.send(msg)
        else:
            flash("This product is out of stock.", "danger")
            return redirect(url_for('main.product', product_id=product_id))

    # -------------------------
    # For Cart Checkout
    # -------------------------
    else:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            flash("Your cart is empty.", "warning")
            return redirect(url_for('main.cart'))

        order_lines = []
        for item in cart_items:
            if item.quantity <= item.product.stock:
                item.product.stock -= item.quantity
                order_lines.append(
                    f"- {item.product.name} (x{item.quantity}) | ₹{item.product.price} each | Brand: {item.product.brand}"
                )
                db.session.delete(item)
            else:
                flash(f"Not enough stock for {item.product.name}.", "danger")
                return redirect(url_for('main.cart'))

        db.session.commit()

        msg = Message("Order Confirmation",
                      sender="hulkandtheagentsofsmash2@gmail.com",
                      recipients=[email])
        msg.body = (
            "Your cart order has been confirmed!\n\n"
            "Order Summary:\n" +
            "\n".join(order_lines) +
            "\n\nThank you for shopping with Phone-Verse!"
        )
        mail.send(msg)

    return redirect(url_for('main.thank_you'))

@main.route('/thankyou')
@login_required
def thank_you():
    return render_template('thankyou.html')
