from rest_framework.response import Response

from apiv1.utils.const import API_VERSION


def create(data, status_code=200, count=-1):
    response_data = {
        "api_version": API_VERSION,
        "status_code": status_code,
    }
    if count >= 0:
        response_data["count"] = count

    response_data["result"] = data
    return Response(response_data, status_code)
