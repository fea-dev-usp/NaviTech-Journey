from urllib import request
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class PlanTable(Table):
    id = Col('Id')
    seller_id = Col('Seller')
    quantity_kwh = Col('Quantity of KwH')
    value = Col('Price')
    validity_time = Col('Validity time')
    maturity_date = Col('Maturity Date')
    plan_type = Col('Plan Type')
    status = Col('Status')

class PlanModel(db.Model):

    id =  db.Column(db.String(20), primary_key=True)
    seller_id = db.Column(db.String(100))
    quantity_kwh = db.Column(db.Float)
    value =db.Column(db.Float)
    validity_time = db.Column(db.String(100))
    maturity_date = db.Column(db.String(100))
    plan_type = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __repr__(self):
        return "Plataform(seller_id = {}, quantity_kwh = {}, value = {}, validity_time = {}, maturity_date = {}, plan_type = {}, status = {})".format(seller_id, quantity_kwh, value, validity_time, maturity_date, plan_type, status)

class OrderTable(Table):
    id = Col('Id')
    plan_id = Col('Plan Id')
    buyer_id = Col('Buyer')
    date = Col('Date')

class OrderModel(db.Model):
    id =  db.Column(db.String(20), primary_key=True)
    plan_id = db.Column(db.String(100))
    buyer_id = db.Column(db.String(100))
    date = db.Column(db.String(100))
   
    def __repr__(self):
        return "Order(plan_id = {}, buyer_id = {}, date = {})".format(plan_id, buyer_id, date)

db.create_all()

plan_post_args = reqparse.RequestParser()
plan_post_args.add_argument("id", type=str)
plan_post_args.add_argument("seller_id", type=str)
plan_post_args.add_argument("quantity_kwh", type=float)
plan_post_args.add_argument("value", type=float)
plan_post_args.add_argument("validity_time", type=str)
plan_post_args.add_argument("maturity_date", type=str)
plan_post_args.add_argument("plan_type", type=str)
plan_post_args.add_argument("status", type=str)

orders_post_args = reqparse.RequestParser()
orders_post_args.add_argument("id", type=str)
orders_post_args.add_argument("plan_id", type=str)
orders_post_args.add_argument("buyer_id", type=str)
orders_post_args.add_argument("date", type=str)

headings = ['id', 'seller_id', 'quantity_kwh', 'value', 'validity_time', 'maturity_date', 'plan_type', 'status']

@app.route('/plans', methods=['GET'])
def get_plans():
    result = PlanModel.query.all()
    return render_template("table.html", headings = headings, data = result)

@app.route('/plans', methods=['POST'])
def post_plans():
    args = plan_post_args.parse_args()
    result = PlanModel.query.filter_by(id = args['id']).first()
    if result:
        abort(409, message="Plan id taken...")

    plan = PlanModel(
        id = args["id"], 
        seller_id = args['seller_id'], 
        quantity_kwh = args['quantity_kwh'], 
        value = args['value'],
        validity_time = args['validity_time'],
        maturity_date = args['maturity_date'],
        plan_type = args['plan_type'],
        status = 'Disponível')

    db.session.add(plan)
    db.session.commit()
    # db.session.close()
    return jsonify(result), 201 # created

@app.route('/plans', methods=['PUT'])
def put_plans():
        args = plan_post_args.parse_args()
        result = PlanModel.query.filter_by(id = args['id']).first()
        if not result:
            abort(404, message="plan doesn't exist, cannot update")

        if args['seller_id']:
            result.seller_id = args['seller_id']
        if args["quantity_kwh"]:
            result.quantity_kwh = args['quantity_kwh']
        if args["value"]:
            result.value = args['value']
        if args["validity_time"]:
            result.validity_time = args['validity_time']
        if args["maturity_date"]:
            result.maturity_date = args['maturity_date']
        if args["plan_type"]:
            result.plan_type = args['plan_type']
        if args["status"]:
            result.plan_type = args['status']

        db.session.commit()

        return jsonify(result)

@app.route('/orders', methods=['GET'])
def get_orders():
    result = OrderModel.query.all()
    table = OrderTable(result)
    return table.__html__()
    
@app.route('/orders', methods=['POST'])
def post_orders():
    args = orders_post_args.parse_args()
    result = PlanModel.query.filter_by(id = args["plan_id"]).first()
    if not result:
        abort(404, message="Plan id does't exist...")

    result.status = "Vendido"

    order = OrderModel(
        id = args["id"], 
        plan_id = args['plan_id'], 
        buyer_id = args['buyer_id'], 
        date = args['date']
        )

    db.session.add(order)
    db.session.commit()
    return order, 201

if __name__ == "__main__":
    app.run(port=5001, debug=True)
    # http://127.0.0.1:5001/plans
    # http://127.0.0.1:5001/orders