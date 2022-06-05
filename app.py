from flask import Flask
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PlanModel(db.Model):
    id =  db.Column(db.String(20), primary_key=True)
    seller_id = db.Column(db.String(100))
    quantity_kwh = db.Column(db.Float)
    value =db.Column(db.Float)
    validity_time = db.Column(db.String(100))
    maturity_date = db.Column(db.String(100))
    plan_type = db.Column(db.String(100))
   
    def __repr__(self):
        return "Plataform(seller_id = {}, quantity_kwh = {}, value = {}, validity_time = {}, maturity_date = {}, plan_type = {})".format(seller_id, quantity_kwh, value, validity_time, maturity_date, plan_type)

db.create_all()

# plan_post_args = reqparse.RequestParser()
# plan_post_args.add_argument("id", type=str)
# plan_post_args.add_argument("seller_id", type=str)
# plan_post_args.add_argument("quantity_kwh", type=float)
# plan_post_args.add_argument("value", type=float)
# plan_post_args.add_argument("validity_time", type=str)
# plan_post_args.add_argument("maturity_date", type=str)
# plan_post_args.add_argument("plan_type", type=str)

# # serialize objects
# resource_fields = {
#     'id': fields.String,
#     'seller_id': fields.String,  
#     'quantity_kwh': fields.Float, 
#     'value': fields.Float, 
#     'validity_time': fields.String,
#     'maturity_date': fields.String,
#     'plan_type': fields.String
# }

class Plans(Resource):
   # @marshal_with(resource_fields) # when we return, take the result value and serialize it with resource_fields
    def get(self):
        #result = PlanModel.query.filter_by(id = plan_id).first() #all()
        result = PlanModel.query.all()
        if not result:
            abort(404, message="Coult not find plan with that id")
        return result

   # @marshal_with(resource_fields)
    def post(self, plan_id):
        args = plan_post_args.parse_args()
        result = PlanModel.query.filter_by(id = plan_id).first()
        if result:
            abort(409, message="Plan id taken...")

        plan = PlanModel(
            id = plan_id, 
            seller_id = args['seller_id'], 
            quantity_kwh = args['quantity_kwh'], 
            value = args['value'],
            validity_time = args['validity_time'],
            maturity_date = args['maturity_date'],
            plan_type = args['plan_type']
            )

        db.session.add(plan)
        db.session.commit()
        # db.session.close()
        return plan, 201 # created

   # @marshal_with(resource_fields)
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

        db.session.commit()

        return result

api.add_resource(Plans, "/plans")
api.add_resource(Plans, "/plans/<string:plan_id>")

if __name__ == "__main__":
    app.run(debug=True)