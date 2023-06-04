from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load product data from a JSON file
with open("loopr/product.json") as f:
    products = json.load(f)

# Store cart data in a JSON file
CART_FILE = "cart.json"
cart_data = {}

# Read cart data from the JSON file
def get_cart_data():
    global cart_data
    try:
        with open(CART_FILE) as f:
            cart_data = json.load(f)
    except FileNotFoundError:
        cart_data = {}

# Write cart data to the JSON file
def write_cart_data():
    with open(CART_FILE, "w") as f:
        json.dump(cart_data, f)

# Get the total price and quantity of the items in the cart
def get_cart_summary():
    total_price = 0
    total_quantity = 0
    for product_id, quantity in cart_data.items():
        product = products.get(product_id)
        if product:
            total_price += product["price"] * quantity
            total_quantity += quantity
    return total_price, total_quantity

@app.route("/cart", methods=["GET"])
def view_cart():
    get_cart_data()
    total_price, total_quantity = get_cart_summary()
    # print(cart_data)
    return jsonify({
        "total_price": total_price,
        "total_quantity": total_quantity,
        "cart_data":cart_data
    })

@app.route("/cart", methods=["POST"])
def add_to_cart():
    get_cart_data()
   
    product_id = request.json.get("product_id")
    quantity = request.json.get("quantity", 1)

    if not product_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"message": "Invalid product_id or quantity"}), 400

    product = products.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    cart_data[product_id] = cart_data.get(product_id, 0) + quantity
    write_cart_data()
    return jsonify({"message": "Product added to cart"}), 200

@app.route("/cart/<product_id>", methods=["PUT"])
def update_cart_item(product_id):
    get_cart_data()
    quantity = request.json.get("quantity", 1)

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"message": "Invalid quantity"}), 400

    if product_id not in cart_data:
        return jsonify({"message": "Product not found in cart"}), 404

    cart_data[product_id] = quantity
    write_cart_data()
    return jsonify({"message": "Cart item updated"}), 200

@app.route("/cart/<product_id>", methods=["DELETE"])
def remove_from_cart(product_id):
    get_cart_data()
    if product_id not in cart_data:
        return jsonify({"message": "Product not found in cart"}), 404

    del cart_data[product_id]
    write_cart_data()
    return jsonify({"message": "Product removed from cart"}), 200

if __name__ == "__main__":
    app.run(debug=True)
