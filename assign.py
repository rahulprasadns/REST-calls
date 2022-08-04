from flask import Flask, Response, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import urllib
import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class FeeDue(db.Model):
    __tablename__ = "feedue"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    date_of_birth = db.Column(db.String(10))
    amount_due = db.Column(db.Integer)

    def json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'amount_due': self.amount_due
        }

    def add_feedue(_id, _student_id, _first_name, _last_name, _date_of_birth, _amount_due):
        new_feedue = FeeDue(id = _id, student_id= _student_id, first_name = _first_name, last_name = _last_name, date_of_birth = _date_of_birth, amount_due = _amount_due)
        db.session.add(new_feedue)
        db.session.commit()

    def get_all_feedue():
        return [FeeDue.json(feedue) for feedue in FeeDue.query.all()]

    def get_feedue(_id):
        return [FeeDue.json(FeeDue.query.filter_by(id=_id).first())]

    def update_feedue(_id,_student_id, _first_name, _last_name, _date_of_birth, _amount_due):
        feedue = FeeDue.query.filter_by(id=_id).first()
        feedue.student_id = _student_id
        feedue.first_name = _first_name
        feedue.last_name = _last_name
        feedue.date_of_birth = _date_of_birth
        feedue.amount_due = _amount_due
        db.session.commit()
    
    def delete_feedue(_id):
        feedue = FeeDue.query.filter_by(id=_id).first()
        db.session.delete(feedue)
        db.session.commit()
        return feedue

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    # def __init__(self, student_id, first_name, last_name, date_of_birth, amount_due):
    #     self.student_id = student_id
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.date_of_birth = date_of_birth
    #     self.amount_due = amount_due

    def __repr__(self):
        return f"{self.id}"

db.create_all()

class FeeDueSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
       model = FeeDue
       sqla_session = db.session
    id = fields.Number(dump_only=True)
    student_id = fields.Number(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    date_of_birth = fields.String(required=True)
    amount_due = fields.Number(required=True)


@app.route('/api/v1/feedue', methods=['POST'])
def create_feedue():
    request_data = request.get_json()
    FeeDue.add_feedue(request_data['id'], request_data['student_id'], request_data['first_name'], request_data['last_name'], request_data['date_of_birth'], request_data['amount_due'])
    response = Response("Fee Due Added",status=201, mimetype='application/json')
    return response

@app.route('/api/v1/feedue', methods=['GET'])
def get_feedue():
    return jsonify({"feedue": FeeDue.get_all_feedue()})

@app.route('/api/v1/feedue/<int:id>', methods=['GET'])
def get_feedue_by_id(id):
    return jsonify({"feedue": FeeDue.get_feedue(id)})

@app.route('/api/v1/feedue/<int:id>', methods=['PUT'])
def update_feedue(id):
    request_data = request.get_json()
    FeeDue.update_feedue(id, request_data['student_id'], request_data['first_name'], request_data['last_name'], request_data['date_of_birth'], request_data['amount_due'])
    response = Response("Fee Due Updated",status=201, mimetype='application/json')
    return response

@app.route('/api/v1/feedue/<int:id>', methods=['DELETE'])
def delete_feedue(id):
    FeeDue.delete_feedue(id)
    response = Response("Fee Due Deleted",status=201, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)