from voluptuous import *

get_post_schema = Schema({
    'q': str,
    'page': str,
    'page_size': str
})