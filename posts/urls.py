from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^get_posts/$', get_posts),
    url(r'^posts/$', PostView.as_view())
]
