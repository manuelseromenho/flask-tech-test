from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author


@app.route('/authors', methods=['GET'])
@db_session_wrap
def get_authors(session):
    query = session.query(
        Author
    ).order_by(
        Author.id
    )
    print("OLAÀAAAA ZÈHH")
    return jsonify([author.asdict() for author in query.all()])


@app.route('/authors', methods=['POST'])
@db_session_wrap
def create_author(session):
    request_data = request.get_json()
    author = Author.fromdict(Author(), request_data)
    session.add(author)
    session.flush()
    return jsonify(author.asdict())


@app.route('/authors/<int:author_id>', methods=['PUT'])
@db_session_wrap
def update_author(author_id, session):
    query = session.query(
        Author
    ).filter(
        Author.id == author_id
    ).order_by(
        Author.id
    )
    authors = query.all()
    if not authors:
        abort(404)

    author = authors[0]

    request_data = request.get_json()
    author.fromdict(request_data)

    return jsonify(author.asdict())


@app.route('/authors/<int:author_id>', methods=['DELETE'])
@db_session_wrap
def delete_author(author_id, session):
    query = session.query(
        Author
    ).filter(
        Author.id == author_id
    ).order_by(
        Author.id
    )
    authors = query.all()
    if not authors:
        abort(404)

    author = authors[0]

    session.delete(author)

    return jsonify(author.asdict())



