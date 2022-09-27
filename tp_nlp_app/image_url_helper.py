import os


def get_image_urls(place_id):
    urls = {}
    base_path = os.path.dirname(os.path.abspath('summaries'))
    place_path = 'summaries/' + place_id + '/'
    full_path = base_path + "/" + place_path
    fmt = '.png'
    urls['POS'] = full_path + 'POS' + fmt
    urls['NEG'] = full_path + 'NEG' + fmt
    urls['NEU'] = full_path + 'NEU' + fmt
    return urls
