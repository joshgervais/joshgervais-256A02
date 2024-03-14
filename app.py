"""
ITAS 256 - Web Development II
Assignment 2 – Flask Web Server for Pizza Delivery Service
Josh Gervais

This application is a Flask web server designed for a basic pizza delivery service

The web server operates on port 8888 and is accessible at http://localhost:8888

"""

from flask import Flask, render_template, url_for, flash, redirect, session, request
from functools import wraps
from forms import LoginForm, RegistrationForm, OrderForm
from data_handler import add_user, load_data, add_pizza_order, update_pizza_order, delete_pizza_order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'

# Route for home page
@app.route('/')
def index():
    return 'Welcome to the Pizza Delivery Service!'

# Route for handling login with form validation and session management
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = load_data('users.json')
        user = next((user for user in users if user['email'] == form.email.data and user['password'] == form.password.data), None)
        if user:
            session['email'] = user['email']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Route for new user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        add_user(form.email.data, form.password.data, form.role.data)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Decorator to enforce login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to enforce specific roles for access
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash('You do not have permission to view this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Route to display orders with price formatting
@app.route('/orders')
@login_required
def orders():
    orders = load_data('pizzaorders.json')
    sorted_orders = sorted(orders, key=lambda x: x['order_date'], reverse=True)
    for order in sorted_orders:
        order['price_per_formatted'] = f"${order['price_per']:.2f}"
        order['subtotal_formatted'] = f"${(order['quantity'] * order['price_per']):.2f}"
        order['delivery_charge_formatted'] = f"${(order['quantity'] * order['price_per']) * 0.1:.2f}"
        order['total_formatted'] = f"${(order['quantity'] * order['price_per']) * 1.1:.2f}"
    return render_template('orders.html', orders=sorted_orders)

# Route for adding or editing pizza orders
@app.route('/pizza', methods=['GET', 'POST'])
@login_required
def add_pizza():
    form = OrderForm()
    init_data = load_data('init.json')
    form.type.choices = [(item, item) for item in init_data['type']]
    form.crust.choices = [(item, item) for item in init_data['crust']]
    form.size.choices = [(item, item) for item in init_data['size']]

    if form.validate_on_submit():
        add_pizza_order(form.type.data, form.crust.data, form.size.data, form.quantity.data, form.price_per.data, form.order_date.data.strftime('%Y-%m-%d'))
        flash('Your order has been placed!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('add_order.html', title='New Order', form=form)

# Route for editing orders, accessible by staff
@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
@role_required('s')
def edit_order(order_id):
    order_to_edit = next((order for order in load_data('pizzaorders.json') if order['id'] == order_id), None)
    if not order_to_edit:
        flash('Order not found.', 'danger')
        return redirect(url_for('orders'))

    form = OrderForm(obj=order_to_edit)
    init_data = load_data('init.json')
    form.type.choices = [(item, item) for item in init_data['type']]
    form.crust.choices = [(item, item) for item in init_data['crust']]
    form.size.choices = [(item, item) for item in init_data['size']]

    if form.validate_on_submit():
        update_pizza_order(order_id, form.type.data, form.crust.data, form.size.data, form.quantity.data, form.price_per.data, form.order_date.data.strftime('%Y-%m-%d'))
        flash('Order updated successfully!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('edit_order.html', form=form, order_id=order_id)

# Route for order deletion
@app.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
@role_required('s')
def delete_order(order_id):
    delete_pizza_order(order_id)
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('orders'))

# Confirmation dialog for order deletion
@app.route('/confirm_delete', methods=['GET', 'POST'])
@login_required
@role_required('s')
def confirm_delete():
    order_id = request.args.get('order_id', type=int) if request.method == 'GET' else request.form.get('order_id', type=int)
    
    if not order_id:
        flash('Order ID is missing.', 'danger')
        return redirect(url_for('orders'))

    if request.method == 'POST' and request.form.get('confirm') == 'Yes':
        delete_pizza_order(order_id)
        flash('Order deleted successfully!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('confirm_delete.html', order_id=order_id) if request.method == 'GET' else redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
