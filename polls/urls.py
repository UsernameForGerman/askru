from django.urls import include, path

from .routings import router

app_name = 'polls'

urlpatterns = [
    path('', include(router.urls)),
]
