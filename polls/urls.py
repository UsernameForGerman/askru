from django.urls import include, path

from .routings import router

urlpatterns = [
    path('', include(router.urls)),
]
