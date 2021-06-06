from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.region import Region


@app.route('/regions', methods=['GET'])
@db_session_wrap
def get_regions(session):
    query = session.query(
        Region
    ).order_by(
        Region.id
    )
    return jsonify([region.asdict() for region in query.all()])


@app.route('/regions', methods=['POST'])
@db_session_wrap
def create_region(session):
    request_data = request.get_json()
    region = Region.fromdict(Region(), request_data)
    session.add(region)
    session.flush()
    return jsonify(region.asdict())


@app.route('/regions/<int:region_id>', methods=['GET'])
@db_session_wrap
def get_region_route(region_id, session):
    query = session.query(
        Region
    ).filter(
        Region.id == region_id
    ).order_by(
        Region.id
    )
    regions = query.all()
    if not regions:
        abort(404)
    return jsonify(regions[0].asdict())


@app.route('/regions/<int:region_id>', methods=['PUT'])
@db_session_wrap
def update_region(region_id, session):
    query = session.query(
        Region
    ).filter(
        Region.id == region_id
    ).order_by(
        Region.id
    )
    regions = query.all()
    if not regions:
        abort(404)

    region = regions[0]

    request_data = request.get_json()
    region.fromdict(request_data)

    return jsonify(region.asdict())


@app.route('/regions/<int:region_id>', methods=['DELETE'])
@db_session_wrap
def delete_region(region_id, session):
    query = session.query(
        Region
    ).filter(
        Region.id == region_id
    ).order_by(
        Region.id
    )
    regions = query.all()
    if not regions:
        abort(404)

    region = regions[0]

    session.delete(region)

    return jsonify(region.asdict())
