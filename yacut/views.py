import random

from flask import flash, redirect, render_template

from . import app, db
from yacut.models import URLMap
from yacut.forms import URLMapForm
from yacut import constants as const
from yacut.validators import length_symbol_validate


def get_unique_short_id() -> str:
    '''Сгенерировать короткую ссылку'''
    short_link = ''.join(random.sample(const.LETTER_AND_DIGITS, const.MAX_LENGTH))
    while URLMap.query.filter_by(short=short_link).first():
        short_link = ''.join(random.sample(const.LETTER_AND_DIGITS, const.MAX_LENGTH))
    return short_link


@app.route('/', methods=('POST', 'GET'))
def index_view() -> str:
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    custom_id = form.custom_id.data

    if not custom_id:
        custom_id = get_unique_short_id()

    if URLMap.query.filter_by(short=custom_id).first():
        flash(f'Имя {custom_id} уже занято!')
        return render_template('index.html', form=form)

    if not length_symbol_validate(custom_id):
        flash('Указано недопустимое имя для короткой ссылки')
        return render_template('index.html', form=form)

    url_map = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    return render_template('index.html', form=form, short_url=custom_id)


@app.route('/<string:short_url>', methods=('GET',))
def short_url_redirect_view(short_url: str):
    url_map = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url_map.original)
