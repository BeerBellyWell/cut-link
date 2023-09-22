from flask import jsonify, request, url_for

from . import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id
from yacut.validators import length_symbol_validate
from yacut import constants as const


@app.route('/api/id/', methods=('POST', ))
def create_short_link() -> tuple:
    data = request.get_json()
    print(data)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', const.HTTP_400)

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or data['custom_id'] is None:
        short_url = get_unique_short_id()
    else:
        short_url = data['custom_id']

    if not length_symbol_validate(short_url):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', const.HTTP_400)

    if URLMap.query.filter_by(short=short_url).first():
        raise InvalidAPIUsage(f'Имя "{short_url}" уже занято.')

    url_map = URLMap(original=data['url'], short=short_url)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for('short_url_redirect_view', short_url=short_url, _external=True)}
    ), const.HTTP_201


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_link(short_id: str) -> tuple:
    orig_url = URLMap.query.filter_by(short=short_id).first()
    if orig_url is None:
        raise InvalidAPIUsage('Указанный id не найден', const.HTTP_404)
    return jsonify({'url': orig_url.original}), const.HTTP_200
