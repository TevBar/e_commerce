from flask import request, jsonify
from .models import Customer, Product, Order, CustomerAccount
from .database import db

def setup_routes(app):
    # Customer routes
    @app.route("/customers", methods=["POST"])
    def create_customer():
        data = request.get_json()
        customer = Customer(name=data["name"], email=data["email"], phone_number=data["phone_number"])
        db.session.add(customer)
        db.session.commit()
        return jsonify({"id": customer.id, "name": customer.name, "email": customer.email}), 201

    @app.route("/customers/<int:id>", methods=["GET"])
    def get_customer(id):
        customer = Customer.query.get(id)
        if customer:
            return jsonify({"id": customer.id, "name": customer.name, "email": customer.email})
        return jsonify({"error": "Customer not found"}), 404

    @app.route("/customers/<int:id>", methods=["PUT"])
    def update_customer(id):
        customer = Customer.query.get(id)
        if customer:
            data = request.get_json()
            customer.name = data.get("name", customer.name)
            customer.email = data.get("email", customer.email)
            customer.phone_number = data.get("phone_number", customer.phone_number)
            db.session.commit()
            return jsonify({"id": customer.id, "name": customer.name, "email": customer.email})
        return jsonify({"error": "Customer not found"}), 404

    @app.route("/customers/<int:id>", methods=["DELETE"])
    def delete_customer(id):
        customer = Customer.query.get(id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return jsonify({"message": "Customer deleted successfully"})
        return jsonify({"error": "Customer not found"}), 404

    # Product routes
    @app.route("/products", methods=["POST"])
    def create_product():
        data = request.get_json()
        product = Product(name=data["name"], price=data["price"])
        db.session.add(product)
        db.session.commit()
        return jsonify({"id": product.id, "name": product.name, "price": product.price}), 201

    @app.route("/products/<int:id>", methods=["GET"])
    def get_product(id):
        product = Product.query.get(id)
        if product:
            return jsonify({"id": product.id, "name": product.name, "price": product.price})
        return jsonify({"error": "Product not found"}), 404

    @app.route("/products/<int:id>", methods=["PUT"])
    def update_product(id):
        product = Product.query.get(id)
        if product:
            data = request.get_json()
            product.name = data.get("name", product.name)
            product.price = data.get("price", product.price)
            db.session.commit()
            return jsonify({"id": product.id, "name": product.name, "price": product.price})
        return jsonify({"error": "Product not found"}), 404

    @app.route("/products/<int:id>", methods=["DELETE"])
    def delete_product(id):
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully"})
        return jsonify({"error": "Product not found"}), 404

    # Order routes
    @app.route("/orders", methods=["POST"])
    def place_order():
        data = request.get_json()
        order = Order(customer_id=data["customer_id"], order_date=datetime.utcnow())
        for product_id in data["products"]:
            product = Product.query.get(product_id)
            order.products.append(product)
        db.session.add(order)
        db.session.commit()
        return jsonify({"order_id": order.id, "order_date": order.order_date}), 201

    @app.route("/orders/<int:id>", methods=["GET"])
    def get_order(id):
        order = Order.query.get(id)
        if order:
            return jsonify({"order_id": order.id, "order_date": order.order_date, "customer_id": order.customer_id})
        return jsonify({"error": "Order not found"}), 404
