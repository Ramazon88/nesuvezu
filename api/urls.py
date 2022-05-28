from django.urls import path

from api.views import *

urlpatterns = [
    path('post/', PostCreateApi.as_view()),
    path('put/', UpdateApi.as_view()),
    path('done/', UpdateApiDone.as_view())
]
