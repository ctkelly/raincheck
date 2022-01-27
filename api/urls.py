from django.urls import path
from api import views


app_name = 'api'
urlpatterns = [
    path('events/<int:pk>', views.EventDetailAPIView.as_view(), name='event_detail'),
    path('events/', views.EventAPIView.as_view(), name='event_view')
]

