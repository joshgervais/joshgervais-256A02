import json
import os

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')

def get_file_path(file_name):
    """Returns the absolute path of a file in the data directory."""
    return os.path.join(DATA_FOLDER, file_name)

def load_data(file_name):
    """Load data from a JSON file located in the data folder."""
    file_path = get_file_path(file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(file_name, data):
    """Save data to a JSON file located in the data folder."""
    file_path = get_file_path(file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def add_user(email, password, role):
    """Add a new user to users.json."""
    users = load_data('users.json')
    users.append({
        'email': email,
        'password': password,
        'role': role
    })
    save_data('users.json', users)

def add_pizza_order(type, crust, size, quantity, price_per, order_date):
    """Add a new pizza order to pizzaorders.json."""
    orders = load_data('pizzaorders.json')
    new_id = max([order['id'] for order in orders], default=0) + 1
    orders.append({
        'id': new_id,
        'type': type,
        'crust': crust,
        'size': size,
        'quantity': quantity,
        'price_per': price_per,
        'order_date': order_date
    })
    save_data('pizzaorders.json', orders)

def update_pizza_order(order_id, type, crust, size, quantity, price_per, order_date):
    """Update an existing pizza order in pizzaorders.json."""
    orders = load_data('pizzaorders.json')
    for order in orders:
        if order['id'] == order_id:
            order.update({
                'type': type,
                'crust': crust,
                'size': size,
                'quantity': quantity,
                'price_per': price_per,
                'order_date': order_date
            })
            break
    save_data('pizzaorders.json', orders)

def delete_pizza_order(order_id):
    """Delete a pizza order from pizzaorders.json."""
    orders = load_data('pizzaorders.json')
    orders = [order for order in orders if order['id'] != order_id]
    save_data('pizzaorders.json', orders)
