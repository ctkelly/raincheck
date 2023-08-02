from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.serializers import EventSerializer


class EventDetailAPIView(APIView):
    # The below mimics LoginRequiredMixIn behavior.  Check who the user is and that they're allowed to do stuff.
    authentication_classes = (SessionAuthentication,)  # A tuple
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(data=serializer.data, status=200)  # Need to pass data and status keyword args

