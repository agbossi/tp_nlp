
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from tp_nlp_app.exceptions import PlaceNotFoundException, TooManyPlaceCandidatesException, IllegalArgumentsException
from tp_nlp_app.models import Place
from tp_nlp_app import response_helper
from tp_nlp_app.serializers import PlaceSerializer
from tp_nlp_app import services


@api_view(['GET'])
def place_summary(request):
    name = request.query_params.get("name") or None
    _id = request.query_params.get("id") or None
    lat = request.query_params.get("lat") or None
    lng = request.query_params.get("lng") or None
    try:
        summary = services.get_place_summary(_id, name, lat, lng)
    except (PlaceNotFoundException, TooManyPlaceCandidatesException, IllegalArgumentsException) as e:
        return response_helper.response_bad_request(errors=str(e))

    return response_helper.response_get_or_not_found(item=summary.data)


@api_view(['GET', 'POST'])
def places(request):
    if request.method == 'GET':
        return get_places(request)
    elif request.method == 'POST':
        return post_place(request)


def get_places(request):
    serializer = PlaceSerializer(data=Place.objects.all(), many=True)
    return response_helper.response_get_or_not_found(item=serializer.data)


def post_place(request):
    place_data = JSONParser().parse(request)
    serializer = PlaceSerializer(data=place_data)
    if serializer.is_valid():
        serializer.save()
        return response_helper.response_post(item=serializer.data)
    return response_helper.response_bad_request(errors=serializer.errors)
