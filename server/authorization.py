from utils import MessageUtil
from flask import abort
from flask import request


def check_authorization(flaskrequest):
    def warpper(*args, **kwargs):
        if MessageUtil().check_headers_authorization(request.headers) is False:
            return abort(403)
        return flaskrequest(*args, **kwargs)

    warpper.__name__ = flaskrequest.__name__
    return warpper


def check_sign(flaskrequest):
    def warpper(*args, **kwargs):
        if MessageUtil().check_data_sign(request.headers, request.form) is False:
            return abort(403)
        return flaskrequest(*args, **kwargs)

    warpper.__name__ = flaskrequest.__name__
    return warpper
