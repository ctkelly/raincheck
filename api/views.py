from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import json

from events.models import Event, Invitation
from events.serializers import EventSerializer
from django.db.models import Q
from datetime import date


class EventDetailAPIView(APIView):
    # The below mimics LoginRequiredMixIn behavior.  Check who the user is and that they're allowed to do stuff.
    authentication_classes = (SessionAuthentication,)  # A tuple
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(data=serializer.data, status=200)  # Need to pass data and status keyword args


#  Trying something
#  Need to set up a serializers.py to use the below? e.g. class EventSerializer(serializers.Serializer) etc...
class EventAPIView(APIView):

    authentication_classes = (SessionAuthentication,)  # A tuple
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        today = date.today()
        events = Event.objects.filter(
            Q(owner=self.request.user) |
            Q(invitee=self.request.user),
            date__gte=today
        ).order_by('date')  # Leave in "order_by('date')" part for this view?

        serializer = EventSerializer(events, many=True)
        return Response({"events": serializer.data})




