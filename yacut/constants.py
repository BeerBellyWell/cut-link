import string

from http import HTTPStatus

LETTER_AND_DIGITS = string.ascii_letters + string.digits
MAX_LENGTH = 6
MIN_VAL_LEN = 1
MAX_VAL_LEN = 16
HTTP_404 = HTTPStatus.NOT_FOUND
HTTP_500 = HTTPStatus.INTERNAL_SERVER_ERROR
HTTP_400 = HTTPStatus.BAD_REQUEST
HTTP_200 = HTTPStatus.OK
HTTP_201 = HTTPStatus.CREATED
