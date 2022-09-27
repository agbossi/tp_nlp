
from tp_nlp_app.models import Summary, Token, ReviewQuery, QueryType, Place


def get_summary_by_id(_id):
    return Summary.objects.filter(place__placeId=_id).first()


def get_summary_by_place_name(name, lat, lng):
    return Summary.objects.filter(place__name=name)\
        .filter(place__latitude=lat)\
        .filter(place__longitude=lng).first()


def get_search_history_for_query(place, sort_by):
    return ReviewQuery.objects.filter(place=place).filter(sortType__sortBy=sort_by).first()


def get_query_type_by_name(name):
    return QueryType.objects.filter(sortBy=name).first()


def get_maps_token():
    return Token.objects.filter(auth_to="maps.googleapis.com").first()


def get_scrapper_token():
    return Token.objects.filter(auth_to="api.app.outscraper.com").first()


def get_place_by_id(_id):
    return Place.objects.filter(placeId=_id).first()


def get_place_by_name(name, lat, lng):
    return Place.objects.filter(name=name).filter(latitude=lat).filter(longitude=lng).first()
