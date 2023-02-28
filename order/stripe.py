import json
import os
import requests
import stripe


stripe.api_key = os.environ["STRIPE_PRIVATE_KEY"]
orders_url = os.environ["STRIPE_PRODUCTS_URL"]
prices_url = os.environ["STRIPE_PRICES_URL"]


def create_stripe_order(data, price, key, first_name, last_name):
    """
    Function initializes new order instance (as product) on the Stripe API side.
    """

    headers = {
        "Authorization": f"Bearer {stripe.api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Initializing order instance.
    order_data = {
        "name": f"{first_name} {last_name}. Order #{data.get('id')}",
        "type": "service",
        "description": f"Order identifier: {key}",
    }

    response = requests.post(orders_url, headers=headers, data=order_data)
    if response.status_code == 200:
        print(f"STRIPE : Order '{data.get('id')}' successfully initialized.")
    else:
        raise Exception(response.text)

    # Adding price parameters.
    order_id = json.loads(response.text)["id"]
    price_data = {
        "product": order_id,
        "unit_amount": int(price * 100),
        "currency": "byn",
    }

    response = requests.post(prices_url, headers=headers, data=price_data)
    if response.status_code == 200:
        price_id = json.loads(response.text)["id"]
        print(f"STRIPE : Price info of order '{data.get('id')}' successfully added.")
    else:
        raise Exception(response.text)

    response = requests.get(f"{orders_url}/{order_id}", headers=headers)
    if response.status_code == 200:
        print(f"STRIPE : Order '{data.get('id')}' successfully added.")
        return price_id, order_id
    else:
        raise Exception(response.text)


def delete_stripe_product(order_id):
    """
    Deletes order instance (as product) on the Stripe API side.
    """

    product_data = {
        "active": False,
    }

    response = requests.post(f"{orders_url}/{order_id}", auth=(stripe.api_key, ""), data=product_data)
    if response.status_code == 200:
        print(f"Order {order_id} successfully deactivated.")
    else:
        raise Exception(response.text)
