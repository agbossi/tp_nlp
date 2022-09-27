
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from tp_nlp_app.exceptions import PlaceNotFoundException, TooManyPlaceCandidatesException, IllegalArgumentsException
from tp_nlp_app.models import Place
from tp_nlp_app.models import BlacklistedWord
from tp_nlp_app import response_helper
from tp_nlp_app import image_url_helper
from tp_nlp_app.serializers import PlaceSerializer, SummarySerializer, ResponseSummarySerializer, BlacklistSerializer, \
    PlaceInputSerializer
from tp_nlp_app import services
from tp_nlp_processing import processor


@api_view(['GET'])
def place_entry(request):
    _id = request.query_params.get("id") or None
    place = services.get_place_from_db(_id, None, None, None)
    if place is None:
        return response_helper.response_error(status=status.HTTP_404_NOT_FOUND, str_err='Place not in db')
    processor.generate_place_summary(place)
    place.summarized = True
    place.save()
    return response_helper.response_no_content()


@api_view(['GET', 'PUT'])
def place(request, placeId: str):
    if request.method == 'GET':
        return get_place(request, placeId)
    elif request.method == 'PUT':
        return add_review(request, placeId)


@api_view(['GET', 'PUT', 'DELETE'])
def blacklist(request, placeId: str):
    place = services.get_place_from_db(placeId, None, None, None)
    if place is None:
        return response_helper.response_error(status=status.HTTP_404_NOT_FOUND, str_err='Place not in db')
    if request.method == 'GET':
        return get_blacklist(request, place)
    elif request.method == 'PUT':
        return update_blacklist(request, place)
    elif request.method == 'DELETE':
        return delete_blacklist_word(request, place)


def delete_blacklist_word(request, place):
    word = request.query_params.get("word") or None
    word_elem = BlacklistedWord.objects.filter(place=place).filter(word=word).first()
    word_elem.delete()
    return response_helper.response_no_content()


def get_blacklist(request, place):
    serializer = BlacklistSerializer(data=BlacklistedWord.objects.filter(place=place), many=True)
    serializer.is_valid()
    return response_helper.response_get_or_not_found(item=serializer.data)


def update_blacklist(request, place):
    _data = JSONParser().parse(request)
    serializer = BlacklistSerializer(data=_data)
    if serializer.is_valid():
        word_data = serializer.data
        word = BlacklistedWord(word=word_data['word'].lower(), place=place)
        word.save()
        return response_helper.response_no_content()
    return response_helper.response_bad_request(errors={'message_error': 'not a word'})


@api_view(['GET', 'PUT'])
def place_summary(request):
    name = request.query_params.get("name") or None
    _id = request.query_params.get("id") or None
    lat = request.query_params.get("lat") or None
    lng = request.query_params.get("lng") or None
    place = services.get_place_from_db(_id, name, lat, lng)
    if place is None:
        return response_helper.response_error(status=status.HTTP_404_NOT_FOUND, str_err='Place not in db')
    if request.method == 'GET':
        return get_place_summary(request, place)
    elif request.method == 'PUT':
        return update_summary(request, place)


def update_summary(request, place):
    services.reset_summary(place)
    processor.generate_place_summary(place)
    place.summarized = True
    place.save()
    print('summary saved')
    return response_helper.response_no_content()


def get_place_summary(request, place):
    if not place.summarized:
        return response_helper.response_error(status=status.HTTP_403_FORBIDDEN, str_err='Summary not available yet')
    image_urls = image_url_helper.get_image_urls(place.placeId)
    summary = services.get_place_summary(place.placeId, None, None, None)
    serializer = SummarySerializer(summary)
    ret = ResponseSummarySerializer(data={'summary': serializer.data, 'goodImgUrl': image_urls['POS'], 'badImgUrl': image_urls['NEG'],'neutralImgUrl': image_urls['NEU']})
    ret.is_valid()
    return response_helper.response_get_or_not_found(item=ret.data)


def add_review(request, placeId):
    place = services.get_place_from_db(placeId, None, None, None)
    if place is None:
        return response_helper.response_error(status=status.HTTP_404_NOT_FOUND, str_err='Place not in db')
    services.add_reviews_to_place(place)
    services.reset_summary(place)
    processor.generate_place_summary(place)

    return response_helper.response_no_content()


@api_view(['GET', 'POST'])
def places(request):
    if request.method == 'GET':
        return get_places(request)
    elif request.method == 'POST':
        return post_place(request)


def get_place(request, placeId):
    place = services.get_place_from_db(placeId, None, None, None)
    if place is None:
        return response_helper.response_error(status=status.HTTP_404_NOT_FOUND, str_err='Place not in db')
    serializer = PlaceSerializer(place)
    return response_helper.response_get_or_not_found(item=serializer.data)


def get_places(request):
    serializer = PlaceSerializer(data=Place.objects.all(), many=True)
    serializer.is_valid()
    return response_helper.response_get_or_not_found(item=serializer.data)


def post_place(request):
    place_data = JSONParser().parse(request)
    place_data['latitude'] = float(place_data['latitude'])
    place_data['longitude'] = float(place_data['longitude'])
    serializer = PlaceInputSerializer(data=place_data)
    if serializer.is_valid():
        try:
            data = serializer.data
            services.create_place(Place(name=data["name"], latitude=data["latitude"], longitude=data["longitude"]))
        except (PlaceNotFoundException, TooManyPlaceCandidatesException, IllegalArgumentsException) as e:
            return response_helper.response_bad_request(errors=str(e))
        return response_helper.response_post(item=serializer.data)
    return response_helper.response_bad_request(errors=serializer.errors)
