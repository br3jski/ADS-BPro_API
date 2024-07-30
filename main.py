from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

app = Flask(__name__)
# Development server path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Z:\\BaseStation.sqb'
# Production server path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Program Files (x86)\\Kinetic\\BaseStation\\BaseStation.sqb'

db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

class Aircraft(db.Model):
    AircraftID = db.Column(db.Integer, primary_key=True)
    FirstCreated = db.Column(db.DateTime, nullable=False)
    LastModified = db.Column(db.DateTime, nullable=False)
    ModeS = db.Column(db.String(6), unique=True, nullable=False)
    ModeSCountry = db.Column(db.String(24))
    Country = db.Column(db.String(24))
    Registration = db.Column(db.String(20))
    Manufacturer = db.Column(db.String(60))
    ICAOTypeCode = db.Column(db.String(10))
    Type = db.Column(db.String(40))
    SerialNo = db.Column(db.String(30))
    YearBuilt = db.Column(db.String(4))
    PictureURL1 = db.Column(db.String(150))
    PictureURL2 = db.Column(db.String(150))
    PictureURL3 = db.Column(db.String(150))
    OperatorFlagCode = db.Column(db.String(20))
    RegisteredOwners = db.Column(db.String(100))
    def serialize(self):
        return {
            'AircraftID': self.AircraftID,
            'ModeS': self.ModeS,
            'ModeSCountry': self.ModeSCountry,
            'Country': self.Country,
            'Registration': self.Registration,
            'Manufacturer': self.Manufacturer,
            'ICAOTypeCode': self.ICAOTypeCode,
            'Type': self.Type,
            'SerialNo': self.SerialNo,
            'YearBuilt': self.YearBuilt,
            'PictureURL1': self.PictureURL1,
            'PictureURL2': self.PictureURL2,
            'PictureURL3': self.PictureURL3,
            'OperatorFlagCode': self.OperatorFlagCode,
        }

@app.route('/aircraft', methods=['POST'])
def add_aircraft():
    data = request.get_json()
    new_aircraft = Aircraft(
        FirstCreated=datetime.now(),
        LastModified=datetime.now(),
        ModeS=data['ModeS'],
        ModeSCountry=data['ModeSCountry'],
        Country=data['Country'],
        Registration=data['Registration'],
        Manufacturer=data['Manufacturer'],
        ICAOTypeCode=data['ICAOTypeCode'],
        Type=data['Type'],
        SerialNo=data.get('SerialNo'),
        YearBuilt=data.get('YearBuilt'),
        PictureURL1=data.get('PictureURL1'),
        PictureURL2=data.get('PictureURL2'),
        PictureURL3=data.get('PictureURL3'),
        OperatorFlagCode=data['OperatorFlagCode'],
        RegisteredOwners=data.get('RegisteredOwners')
    )
    db.session.add(new_aircraft)
    db.session.commit()
    return {'message': 'Aircraft added successfully'}, 201

@app.route('/aircraft/<string:ModeS>', methods=['PUT'])
def update_aircraft(ModeS):
    data = request.get_json()
    aircraft = Aircraft.query.filter_by(ModeS=ModeS).first()
    if aircraft is None:
        return {'message': 'Aircraft not found'}, 404
    aircraft.ModeSCountry = data['ModeSCountry']
    aircraft.Country = data['Country']
    aircraft.Registration = data['Registration']
    aircraft.Manufacturer = data['Manufacturer']
    aircraft.ICAOTypeCode = data['ICAOTypeCode']
    aircraft.Type = data['Type']
    aircraft.SerialNo = data.get('SerialNo')
    aircraft.YearBuilt = data.get('YearBuilt')
    aircraft.PictureURL1 = data.get('PictureURL1')
    aircraft.OperatorFlagCode = data['OperatorFlagCode']
    aircraft.RegisteredOwners = data.get('RegisteredOwners')
    aircraft.LastModified = datetime.now()
    db.session.commit()
    return {'message': 'Aircraft updated successfully'}, 200

@app.route('/aircraft/<string:ModeS>', methods=['GET'])
def get_aircraft_by_ModeS(ModeS):
    logging.info(f"GET request received for ModeS: {ModeS}")
    aircraft = Aircraft.query.filter_by(ModeS=ModeS).first()
    if aircraft is None:
        logging.warning(f"Aircraft not found for ModeS: {ModeS}")
        return {'message': 'Aircraft not found'}, 404
    logging.info(f"Aircraft found for ModeS: {ModeS}")
    return {
        'AircraftID': aircraft.AircraftID,
        'ModeS': aircraft.ModeS,
        'ModeSCountry': aircraft.ModeSCountry,
        'Country': aircraft.Country,
        'Registration': aircraft.Registration,
        'Manufacturer': aircraft.Manufacturer,
        'ICAOTypeCode': aircraft.ICAOTypeCode,
        'Type': aircraft.Type,
        'SerialNo': aircraft.SerialNo,
        'YearBuilt': aircraft.YearBuilt,
        'PictureURL1': aircraft.PictureURL1,
        'PictureURL2': aircraft.PictureURL2,
        'PictureURL3': aircraft.PictureURL3,
        'OperatorFlagCode': aircraft.OperatorFlagCode,
        'RegisteredOwners': aircraft.RegisteredOwners
    }

@app.route('/aircraft/registration/<string:Registration>', methods=['GET'])
def get_aircraft_by_Registration(Registration):
    logging.info(f"GET request received for Registration: {Registration}")
    aircraft = Aircraft.query.filter_by(Registration=Registration).first()
    if aircraft is None:
        logging.warning(f"Aircraft not found for Registration: {Registration}")
        return {'message': 'Aircraft not found'}, 404
    logging.info(f"Aircraft found for Registration: {Registration}")
    return {
        'AircraftID': aircraft.AircraftID,
        'ModeS': aircraft.ModeS,
        'ModeSCountry': aircraft.ModeSCountry,
        'Country': aircraft.Country,
        'Registration': aircraft.Registration,
        'Manufacturer': aircraft.Manufacturer,
        'ICAOTypeCode': aircraft.ICAOTypeCode,
        'Type': aircraft.Type,
        'SerialNo': aircraft.SerialNo,
        'YearBuilt': aircraft.YearBuilt,
        'PictureURL1': aircraft.PictureURL1,
        'PictureURL2': aircraft.PictureURL2,
        'PictureURL3': aircraft.PictureURL3,
        'OperatorFlagCode': aircraft.OperatorFlagCode,
        'RegisteredOwners': aircraft.RegisteredOwners
    }

@app.route('/list', methods=['GET'])
def list_aircrafts():
    aircrafts = Aircraft.query.all()
    return jsonify([aircraft.serialize() for aircraft in aircrafts])

@app.route('/list/fleet/<string:OperatorFlagCode>', methods=['GET'])
def list_fleet_by_operator(OperatorFlagCode):
    aircrafts = Aircraft.query.filter_by(OperatorFlagCode=OperatorFlagCode).all()
    return jsonify([aircraft.serialize() for aircraft in aircrafts])

@app.route('/list/types/<string:ICAOTypeCode>', methods=['GET'])
def list_types_by_code(ICAOTypeCode):
    aircrafts = Aircraft.query.filter_by(ICAOTypeCode=ICAOTypeCode).all()
    return jsonify([aircraft.serialize() for aircraft in aircrafts])

@app.route('/list/types', methods=['GET'])
def list_types():
    types = Aircraft.query.with_entities(Aircraft.ICAOTypeCode).distinct().all()
    return jsonify([{'ICAOTypeCode': code[0]} for code in types])

@app.route('/airlines', methods=['GET'])
def list_airlines():
    airlines = Aircraft.query.with_entities(Aircraft.OperatorFlagCode, Aircraft.RegisteredOwners).distinct().all()
    return jsonify([{'OperatorFlagCode': code[0], 'RegisteredOwners': code[1]} for code in airlines])

@app.route('/aircraft/<string:ModeS>', methods=['DELETE'])
def delete_aircraft(ModeS):
    aircraft = Aircraft.query.filter_by(ModeS=ModeS).first()
    if aircraft is None:
        return {'message': 'Aircraft not found'}, 404
    db.session.delete(aircraft)
    db.session.commit()
    return {'message': 'Aircraft deleted successfully'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8333)