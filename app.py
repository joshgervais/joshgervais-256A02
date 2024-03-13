from flask import Flask, render_template, url_for, flash, redirect, session, request
from functools import wraps
from forms import LoginForm, RegistrationForm, OrderForm
from data_handler import add_user, load_data, add_pizza_order, update_pizza_order, delete_pizza_order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'

@app.route('/')
def index():
    return 'Welcome to the Pizza Delivery Service!'

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        add_user(form.email.data, form.password.data, form.role.data)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/orders')
@login_required
def orders():
    orders = load_data('pizzaorders.json')
    sorted_orders = sorted(orders, key=lambda x: x['order_date'], reverse=True)
    return render_template('orders.html', orders=sorted_orders)

@app.route('/pizza', methods=['GET', 'POST'])
@login_required
def add_pizza():
    form = OrderForm()
    init_data = load_data('init.json')
    form.type.choices = [(item, item) for item in init_data['type']]
    form.crust.choices = [(item, item) for item in init_data['crust']]
    form.size.choices = [(item, item) for item in init_data['size']]

    if form.validate_on_submit():
        order_date_str = form.order_date.data.strftime('%Y-%m-%d')
        add_pizza_order(form.type.data, form.crust.data, form.size.data, form.quantity.data, form.price_per.data, order_date_str)
        flash('Your order has been placed!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('add_order.html', title='New Order', form=form)

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
@role_required('s')
def edit_order(order_id):
    orders = load_data('pizzaorders.json')
    order_to_edit = next((order for order in orders if order['id'] == order_id), None)
    if order_to_edit is None:
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

@app.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
@role_required('s')
def delete_order(order_id):
    delete_pizza_order(order_id)
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('orders'))
@app.route('/confirm_delete', methods=['GET', 'POST'])
@login_required
@role_required('s')
def confirm_delete():
    if request.method == 'GET':
        order_id = request.args.get('order_id', type=int)
    else:
        order_id = request.form.get('order_id', type=int)
    
    if order_id is None:
        flash('Order ID is missing.', 'danger')
        return redirect(url_for('orders'))
    
    # Now 'order_id' is correctly obtained for both GET and POST methods
    if request.method == 'POST' and request.form.get('confirm') == 'Yes':
        delete_pizza_order(order_id)
        flash('Order deleted successfully!', 'success')
    
    return redirect(url_for('orders')) if request.method == 'POST' else render_template('confirm_delete.html', order_id=order_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
