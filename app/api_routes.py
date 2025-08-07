from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import Product, User, CartItem
from . import db

api = Blueprint('api', __name__, url_prefix='/api')

# Helper function to serialize product
def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'brand': product.brand,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'image_url': product.image_url
    }

# All products
@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([serialize_product(p) for p in products])

# One product
@api.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(serialize_product(product))

# Register user
@api.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered.'}), 400

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

# Login user
@api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Login successful.'})
    return jsonify({'message': 'Invalid credentials.'}), 401

# Get cart
@api.route('/cart', methods=['GET'])
@login_required
def api_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart = []
    for item in cart_items:
        cart.append({
            'product_id': item.product.id,
            'product_name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'subtotal': item.quantity * item.product.price
        })
    total = sum(i['subtotal'] for i in cart)
    return jsonify({'cart': cart, 'total': total})

# Add to cart
@api.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def api_add_to_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    product = Product.query.get_or_404(product_id)

    if item:
        if item.quantity < product.stock:
            item.quantity += 1
        else:
            return jsonify({'message': 'Not enough stock'}), 400
    else:
        if product.stock < 1:
            return jsonify({'message': 'Out of stock'}), 400
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 200

# Remove from cart
@api.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
def api_remove_from_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'}), 200
    return jsonify({'message': 'Item not found'}), 404

# Checkout
@api.route('/checkout', methods=['POST'])
@login_required
def api_checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    order = []
    total = 0
    for item in cart_items:
        if item.quantity <= item.product.stock:
            item.product.stock -= item.quantity
            subtotal = item.quantity * item.product.price
            total += subtotal
            order.append({
                'product': item.product.name,
                'quantity': item.quantity,
                'price': item.product.price,
                'subtotal': subtotal
            })
            db.session.delete(item)
        else:
            return jsonify({'message': f'Not enough stock for {item.product.name}'}), 400

    db.session.commit()
    return jsonify({
        'message': 'Order confirmed',
        'order': order,
        'total': total
    })
