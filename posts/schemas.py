from voluptuous import *

post_schema = {
    'GET': {
        # Optional('page', default=1): All(str, Range(min=1)),
        # Optional('per_size', default=15): All(str, Range(min=1))
        Optional('page'): str,
        Optional('per_size'): str
    },
    'POST': {
        Required('post_type'): All(int, Range(min=0, max=5)),
        Optional('post_title', default=''): str,
        Required('post_content'): str,
        Optional('label_ids', default=[]): list,
        Optional('images', default=[]): list,
        Optional('videos', default=[]): list
    }
}

post_label_schema = {
    'GET': {
        # Optional('page', default=1): All(str, Range(min=1)),
        # Optional('per_size', default=15): All(str, Range(min=1))
        Optional('page'): str,
        Optional('per_size'): str
    },
    'POST': {
        Required('user_id'): All(int, Range(min=1)),
        Required('label_name'): str
    }
}