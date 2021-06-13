from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.article import Article
from techtest.models.author import Author
from techtest.models.region import Region


def generate_str_regions_already_exist(regions_input_intersection):
    str_regions_already_exist = ''
    for region in regions_input_intersection:
        if str_regions_already_exist == '':
            str_regions_already_exist += f'{region.code} with the id: {region.id}'
        else:
            str_regions_already_exist += f' and {region.code} with the id: {region.id}'
    return str_regions_already_exist


def generate_str_authors_already_exist(authors_input_intersection):
    str_authors_already_exist = ''
    for author in authors_input_intersection:
        if str_authors_already_exist == '':
            str_authors_already_exist += f'{author.first_name} {author.last_name} with the id: {author.id}'
        else:
            str_authors_already_exist += f' and {author.first_name} {author.last_name} with the id: {author.id}'
    return str_authors_already_exist


@db_session_wrap
def set_article_regions(article, region_ids, session):
    region_ids_without_duplicates = list(set(region_ids))

    region_query = session.query(
        Region,
    ).filter(
        Region.id.in_(region_ids_without_duplicates),
    )
    regions = region_query.all()
    if len(region_ids_without_duplicates) != len(regions):
        raise Exception('One or more regions don\'t exist')

    endpoint_name = request.endpoint

    if endpoint_name == "update_article" or endpoint_name == "create_article":
        article.regions = regions
    elif endpoint_name == "add_region_to_article":
        regions_input_intersection = set(regions).intersection(set(article.regions))
        str_regions_already_exist = generate_str_regions_already_exist(regions_input_intersection)

        if regions_input_intersection:
            raise Exception(f'The region/s {str_regions_already_exist} already exists in the article')

        article.regions += list(set(regions) - set(article.regions))


@db_session_wrap
def set_article_authors(article, authors_ids, session):
    author_ids_without_duplicates = list(set(authors_ids))
    author_query = session.query(
        Author,
    ).filter(
        Author.id.in_(author_ids_without_duplicates),
    )
    authors = author_query.all()
    if len(author_ids_without_duplicates) != len(authors):
        raise Exception('One or more authors don\'t exist')

    endpoint_name = request.endpoint

    if endpoint_name == "update_article" or endpoint_name == "create_article":
        article.authors = authors
    elif endpoint_name == "add_author_to_article":
        authors_input_intersection = set(authors).intersection(set(article.authors))
        str_authors_already_exist = generate_str_authors_already_exist(authors_input_intersection)

        if authors_input_intersection:
            raise Exception(f'The authors/s {str_authors_already_exist} already exists in the article')

        article.authors += list(set(authors) - set(article.authors))


@app.route('/articles', methods=['GET'])
@db_session_wrap
def get_articles(session):
    query = session.query(
        Article
    ).order_by(
        Article.id
    )
    return jsonify([article.asdict(follow=['regions', 'authors']) for article in query.all()])


@app.route('/articles', methods=['POST'])
@db_session_wrap
def create_article(session):
    request_data = request.get_json()
    article = Article.fromdict(Article(), request_data)
    session.add(article)
    session.flush()
    if 'regions' in request_data:
        set_article_regions(
            article, [x['id'] for x in request_data['regions']],
            session=session,
        )

    if 'authors' in request_data:
        set_article_authors(
            article, [x['id'] for x in request_data['authors']],
            session=session,
        )

    return jsonify(article.asdict(follow=['regions', 'authors']))


@app.route('/articles/<int:article_id>', methods=['GET'])
@db_session_wrap
def get_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    return jsonify(articles[0].asdict(follow=['regions', 'authors']))


@app.route('/articles/<int:article_id>', methods=['PUT'])
@db_session_wrap
def update_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )

    article = query.first()
    if not article:
        abort(404)

    # TODO maybe not the best approach? Instead check above
    # articles = query.all()
    # if not articles:
    #     abort(404)
    #
    # article = articles[0]

    request_data = request.get_json()
    article.fromdict(request_data)
    if 'regions' in request_data:
        set_article_regions(
            article,
            [x['id'] for x in request_data['regions']],
            session=session
        )

    if 'authors' in request_data:
        set_article_authors(
            article, [x['id'] for x in request_data['authors']],
            session=session,
        )

    return jsonify(article.asdict(follow=['regions', 'authors']))


@app.route('/articles/<int:article_id>', methods=['DELETE'])
@db_session_wrap
def delete_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    article = articles[0]

    session.delete(article)

    return jsonify(article.asdict(follow=['regions']))


@app.route('/add_region_to_article/<int:article_id>', methods=['PUT'])
@db_session_wrap
def add_region_to_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )

    article = query.first()
    if not article:
        abort(404)

    request_data = request.get_json()
    article.fromdict(request_data)
    if 'regions' in request_data:
        set_article_regions(
            article,
            [x['id'] for x in request_data['regions']],
            session=session
        )

    return jsonify(article.asdict(follow=['regions']))


@app.route('/add_author_to_article/<int:article_id>', methods=['PUT'])
@db_session_wrap
def add_author_to_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )

    article = query.first()
    if not article:
        abort(404)

    request_data = request.get_json()
    article.fromdict(request_data)
    if 'authors' in request_data:
        set_article_authors(
            article,
            [x['id'] for x in request_data['authors']],
            session=session
        )

    return jsonify(article.asdict(follow=['authors']))
