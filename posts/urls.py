from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^posts/$', PostView.as_view()),
    url(r'^post_label/$', PostLabelView.as_view())
]
