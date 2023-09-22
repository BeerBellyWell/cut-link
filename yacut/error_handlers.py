from flask import render_template, jsonify
from yacut import app, db
from yacut import constants as const


class InvalidAPIUsage(Exception):
    status_code = const.HTTP_400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> tuple:
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(const.HTTP_404)
def page_not_found(error) -> str:
    return render_template('404.html'), const.HTTP_404


@app.errorhandler(const.HTTP_500)
def internal_error(error) -> str:
    db.session.rollback()
    return render_template('500.html'), const.HTTP_500
