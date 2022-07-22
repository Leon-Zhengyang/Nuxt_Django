import logging

from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError
from rest_framework.views import exception_handler

from apiv1.utils.const import API_VERSION

# from apiv1.utils.item_label import ItemLabel


def exception_handler(exc, context):
    """例外ハンドラ"""
    logging.error(f"{exc.__class__.__name__}: {exc}")

    if isinstance(exc, AuthenticationFailed) or isinstance(exc, NotAuthenticated):
        return err_unauth_401()
    if isinstance(exc, NotAuthenticated):
        return err_unauth_401()
    if isinstance(exc, PermissionDenied):
        return err_forbidden_403()
    if isinstance(exc, ValidationError):
        return err_validation(exc, context)

    response = exception_handler(exc, context)
    if response is not None:
        # etc(405:MethodNotAllowed, 406:NotAcceptable, 415:UnsupportedMediaType, 429:Throttled)
        response.data["api_version"] = API_VERSION
        response.data["status_code"] = response.status_code
        response.data["error"] = {"error_code": "E004", "messages": ["処理中にエラーが発生しました。"]}
    return response


def err_validation(exc, context):
    """バリデーションエラー"""
    messages = []
    view_name = context["view"].__class__.__name__
    for key, details in exc.detail.items():
        for detail in details:
            if key == "email" and detail == "この項目は一意でなければなりません。":
                messages.append("このメールアドレスはすでに使われているため、")
                messages.append("別のメールアドレスを入力してください")
            else:
                messages.append(ItemLabel.getLabel(view_name, key) + ":" + detail)
    return JsonResponse(
        {
            "api_version": API_VERSION,
            "status_code": 400,
            "error": {"error_code": "E001", "messages": messages},
        },
        status=400,
    )


def err_unauth_401():
    """401(AuthenticationFailed, NotAuthenticated)"""
    return JsonResponse(
        {
            "api_version": API_VERSION,
            "status_code": 401,
            "error": {"error_code": "E002", "messages": ["ログインされていないか権限がありません。"]},
        },
        status=401,
    )


def err_forbidden_403():
    """403(PermissionDenied)"""
    return JsonResponse(
        {
            "api_version": API_VERSION,
            "status_code": 403,
            "error": {"error_code": "E002", "messages": ["ログインされていないか権限がありません。"]},
        },
        status=403,
    )



