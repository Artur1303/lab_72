from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, VoteApiView

router = DefaultRouter()
router.register('quote', QuoteViewSet, basename='quote')


app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('quote/<int:pk>/ratingdown/', VoteApiView.as_view(), name='quote_ratingdown'),
    path('quote/<int:pk>/ratingup/', VoteApiView.as_view(), name='quote_dratingup')
]
