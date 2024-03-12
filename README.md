# joshgervais-256A02 Pizza Delivery Service

Welcome to the `joshgervais-256A02` repository, the home of a rudimentary pizza delivery service web application developed with Flask. This application supports creating, reading, updating, and deleting pizza orders.

## Installation

Before running the application, ensure you have Python installed on your system. Then, follow these steps to get started:

1. Clone this repository:
```git clone https://github.com/joshgervais/joshgervais-256A02.git```

2. Navigate to the repository folder:
```cd joshgervais-256A02```

3. Install the required Python packages:
```pip install -r requirements.txt```

## Running the Application

To run the server, execute the following command:
```flask run --host=0.0.0.0 --port=8888```


The server will start on port 8888, and you can access the web interface by visiting `http://localhost:8888` in your web browser.

## Features

- User login and session management.
- Form for placing new pizza orders.
- List all orders, with the most recent ones at the top.
- Update and delete existing orders.
- Validation of user input using WTForms.

## Folder Structure

- `data/`: Contains JSON files like `pizzaorders.json` for storing pizza order data.
- `static/`: Stores static files such as CSS stylesheets.
- `templates/`: Contains HTML templates for rendering views.

## Usage

After starting the server, you can:

- Log in or create an account.
- Place a new pizza order.
- View all pizza orders.
- Select an order to update or delete it.

## License

No License

## Acknowledgements

- Flask, a micro web framework written in Python.
- WTForms for form handling.
- The developers and contributors of the Python language.
- ChatGPT for the tireless support.