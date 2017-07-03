from voluptuous import *

comment_schema = {
    'GET': {
        Required('post_id'): str,
        Optional('page'): str,
        Optional('per_size'): str
    },
    'POST': {
        Required('comment_type'): All(int, In((0, 1))),
        Optional('post_id'): All(int, Range(min=0)),
        Optional('post_comment_id'): All(int, Range(min=0)),
        Optional('comment_from_id'): All(int, Range(min=0)),
        Optional('comment_to_id'): All(int, Range(min=0))
    },

}

follower_schema = {
    'GET': {
        Required('post_id'): str,
        Optional('page'): str,
        Optional('per_size'): str
    },
    'POST': {
        Required('post_id'): All(int, Range(min=1)),
        Required('user_id'): All(int, Range(min=1))
    },
    'DELETE': {
        Required('post_id'): All(int, Range(min=1)),
        Required('user_id'): All(int, Range(min=1))
    }
}

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
    },
    'DELETE': {
        Required('post_id'): All(int, Range(min=1))
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