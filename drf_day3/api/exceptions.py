from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def execption_handler(exc, context):
    error = "%s %s %s"%(context["view"],context["request"].method,exc)
    print(error)
    # 先让DRF处理异常,根据处理异常的返回值来判断异常是否被处理
    res = drf_exception_handler(exc, context)

    # 如果返回值为None,代表DRF无法处理此异常,需要自定义处理
    if res is None:
        #或者是status
        return Response({"error_message": "你等会,出错了,我在修,别急"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 如果response不为空,说明异常已经被处理了
    return res
