import time
import datetime
from tp_nlp_app import selectors
from tp_nlp_app.exceptions import IllegalArgumentsException, PlaceNotFoundException
from tp_nlp_app.models import Place, Summary, Review, ReviewQuery
from requests_futures.sessions import FuturesSession
from tp_nlp_processing import processor


def create_place(place):
    full_place = get_place_from_google(place.name, place.latitude, place.longitude)
    full_place.save()
    add_reviews_to_place(full_place)
    place = get_place_from_db(place.placeId, None, None, None)
    processor.generate_place_summary(place)
    full_place.summarized = True
    full_place.save()
    print('summary saved')


def reset_summary(place):
    summary = get_place_summary(place.placeId, None, None, None)
    summary.delete()
    place.summarized = False
    place.save()


def add_reviews_to_place(place):
    good_reviews = get_reviews_from_scrapper(place, 10, sort_by='highest_rating')
    bad_reviews = get_reviews_from_scrapper(place, 10, sort_by='lowest_rating')
    reviews = good_reviews + bad_reviews
    Review.objects.bulk_create(reviews, ignore_conflicts=True)


def get_place_summary(_id, name, lat, lng):
    if lat is not None:
        lat = round(float(lat), 3)
    if lng is not None:
        lng = round(float(lng), 3)
    place = get_place_from_db(_id, name, lat, lng)
    if place is None:
        raise PlaceNotFoundException("Place not in db")
    return selectors.get_summary_by_id(_id)


def get_place_from_db(_id, name, lat, lng):
    if _id is None and name is None:
        raise IllegalArgumentsException("id and name are null")
    if _id is not None:
        place = selectors.get_place_by_id(_id)
    else:
        place = selectors.get_place_by_name(name, lat, lng)
    return place


def get_place_from_google(name, lat, long):
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    sanitized_name = name.replace(" ", "%20")
    params = "input=" + sanitized_name + "&inputtype=textquery"
    location_bias = "&locationbias=circle%3A3000%40" + lat + "%2C" + long
    fields = "&fields=name%2Cplace_id%2Crating%2Cgeometry"
    key = "&key=" + selectors.get_maps_token().value
    url = base_url + params + location_bias + fields + key
    hooks = {'response': response_hook}
    response = async_get(url=url, hooks=hooks)

    place_info = response.data["candidates"]
    if len(place_info) > 1:
        raise Exception("More than one place found with those parameters")
    if len(place_info) == 0:
        raise Exception("No place found at radius of 2000m of coord")
    place_info = place_info[0]
    place = Place(name=place_info["name"], rate=place_info["rating"], placeId=place_info["place_id"],
                  latitude=round(float(place_info["geometry"]["location"]["lat"]), 3),
                  longitude=round(float(place_info["geometry"]["location"]["lng"]), 3))
    return place


#  parametros skip y sort podrian ser utiles
    #  sort permite hacer ordenamiento de maps, para buscar buenas y malas no a ciegas
    #  skip "util para paginacion" saltea N items -> se podria asumir que es lineal para una misma query
def get_reviews_from_scrapper(place, amount, sort_by='most_relevant'):
    query_history = selectors.get_search_history_for_query(place, sort_by)
    if query_history is None:
        query_history = ReviewQuery(place=place, sortType=selectors.get_query_type_by_name(sort_by))
        query_history.save()
    base_url = "https://api.app.outscraper.com/maps/reviews-v3?"
    query = "query=" + place.placeId
    ignore_empty = "&ignoreEmpty=true"
    language = "&language=es"
    reviews_amount = "&reviewsLimit=" + str(amount)
    sort = "&sort=" + query_history.sortType.sortBy
    skip = "&skip=" + str(query_history.searchIndex)
    is_async = "&async=true"
    url = base_url + query + ignore_empty + reviews_amount + language + sort + skip + is_async
    headers = {'X-API-KEY': selectors.get_scrapper_token().value}
    hooks = {'response': response_hook}
    response = async_get(url=url, headers=headers, hooks=hooks)

    query_history.searchIndex += amount
    query_history.save()
    if response.status_code == 200:
        reviews_info = response.data['data'][0]['reviews_data']
    else:
        while response.data['status'] != 'Success':
            time.sleep(10)
            response = async_get('https://api.app.outscraper.com/requests/' + response.data['id'], headers=headers, hooks=hooks)
        reviews_info = response.data['data'][0]['reviews_data']
    reviews = [Review(text=reviews_info[i]["review_text"],
                      date=format_scrapper_datetime(reviews_info[i]["review_datetime_utc"]),
                      rating=reviews_info[i]["review_rating"], place=place,
                      reviewId=reviews_info[i]["review_id"],
                      likes=reviews_info[i]["review_likes"]) for i in range(len(reviews_info))]
    return reviews


def format_scrapper_datetime(dt):
    return datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')


def async_get(url, headers=None, hooks=None):
    session = FuturesSession()
    future = session.get(url=url, headers=headers, hooks=hooks)
    response = future.result()
    if 199 < response.status_code < 300:
        return response
    raise Exception(f'Response status code: {response.status_code}')


def response_hook(resp, *args, **kwargs):
    # parse the json storing the result on the response object
    resp.data = resp.json()
