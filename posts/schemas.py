from voluptuous import *

get_post_schema = Schema({
    'q': str,
    'page': str,
    'page_size': str
})

label_schema = {
    'GET': {
        Optional('page', default=1): All(int, Range(min=1)),
        Optional('per_size', default=15): All(int, Range(min=1))
    },
    'POST': {
        Required('user_id'): All(int, Range(min=1)),
        Required('label_name'): str
    }
}