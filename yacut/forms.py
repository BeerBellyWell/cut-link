from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators

from yacut import constants as const


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=(
            validators.DataRequired(message='Обязательное поле'),
        ))
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(validators.Length(const.MIN_VAL_LEN, const.MAX_VAL_LEN),
                    validators.Optional())
    )
    submit = SubmitField('Создать')
