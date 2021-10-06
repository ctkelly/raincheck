from django.urls import path
from events import views


app_name = 'events'
urlpatterns = [
    path('', views.MainEventView.as_view(), name='all'),
    path('event/create', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete', views.EventDeleteView.as_view(), name='event_delete'),
    path('event/invitation/<int:pk>/update', views.InvitationUpdateView.as_view(), name='invitation_update'),
]
