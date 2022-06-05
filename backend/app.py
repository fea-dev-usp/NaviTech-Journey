from urllib import request
from flask import Flask, render_template
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class ItemTable(Table):
    id = Col('Id')
    seller_id = Col('Seller')
    quantity_kwh = Col('Quantity of KwH')
    value = Col('Price')
    validity_time = Col('Validity time')
    maturity_date = Col('Maturity Date')
    plan_type = Col('Plan Date')
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

class OrderModel(db.Model):

    id =  db.Column(db.String(20), primary_key=True)
    plan_id = db.Column(db.String(100))
    buyer_id = db.Column(db.String(100))
    date = db.Column(db.String(100))
   
    def __repr__(self):
        return "Plataform(plan_id = {}, buyer_id = {}, date = {})".format(plan_id, buyer_id, date)

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

# serialize objects
resource_fields = {
    'id': fields.String,
    'seller_id': fields.String,  
    'quantity_kwh': fields.Float, 
    'value': fields.Float, 
    'validity_time': fields.String,
    'maturity_date': fields.String,
    'plan_type': fields.String,
    'status': fields.String
}


@marshal_with(resource_fields)
@app.route('/plans', methods=['GET'])
def get_plans():
    result = PlanModel.query.all()
    table = ItemTable(result)
    return table.__html__()


@app.route('/plans', methods=['POST'])
@marshal_with(resource_fields)
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
        status = args['status']
        )

    db.session.add(plan)
    db.session.commit()
    # db.session.close()
    return plan, 201 # created

class Plans(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = PlanModel.query.all()
        table = ItemTable(result)
        #print(table.__html__())
        #return table.__html__()
        template = _endpoint_templates['default']
        return render_template(template)

    @marshal_with(resource_fields)
    def post(self):
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
            status = args['status']
            )

        db.session.add(plan)
        db.session.commit()
        # db.session.close()
        return plan, 201 # created

    @marshal_with(resource_fields)
    def put(self, plan_id):
        args = plan_post_args.parse_args()
        result = PlanModel.query.filter_by(id = plan_id).first()
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

        return result

resource_fields_ex =  {
    'id': fields.String,
    'plan_id': fields.String,  
    'buyer_id': fields.String,
    'date': fields.String
}

class Orders(Resource):
    @marshal_with(resource_fields_ex)
    def get(self):
        result = OrderModel.query.all()
        return result
    
    @marshal_with(resource_fields_ex)
    def post(self):
        args = orders_post_args.parse_args()
        result = PlanModel.query.filter_by(id = args["plan_id"]).first()
        if not result:
            abort(404, message="Plan id does't exist...")

        result.status = "vendido"

        order = OrderModel(
            id = args["id"], 
            plan_id = args['plan_id'], 
            buyer_id = args['buyer_id'], 
            date = args['date']
            )

        db.session.add(order)
        db.session.commit()
        return order, 201

#api.add_resource(Plans, "/plans")
#api.add_resource(Orders, "/orders")

if __name__ == "__main__":
    app.run(debug=True)