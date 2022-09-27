from rest_framework.response import Response
from rest_framework import status


def response_get_or_not_found(*,
                         item) -> Response:
    return Response(item, status=status.HTTP_200_OK) if item else Response(status=status.HTTP_404_NOT_FOUND)


def response_post(**kwargs) -> Response:
    return Response(kwargs.get('item'), status=status.HTTP_201_CREATED) if kwargs.get('item') else Response(status=status.HTTP_201_CREATED)


def response_bad_request(*, errors) -> Response:
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def response_error(*, status=status, str_err: str) -> Response:
    return Response({'message_error': str_err}, status=status)


def response_no_content() -> Response:
    return Response(status=status.HTTP_204_NO_CONTENT)
