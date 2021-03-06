from django.db.models import query
from .models import Flight, Reservation
from .serializers import FlightSerializer, ReservationSerializer
from rest_framework import viewsets, filters
from .permission import IsStuffOrReadOnly
from datetime import datetime, date


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStuffOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('departureCity', 'arrivalCity', 'dateOfDepature')
    
    def get_serializer_class (self):
      if self.request.user.is_staff:
        return super().get_serializer_class()
      else:
        return FlightSerializer
    
    def get_queryset(self):
      now = datetime.now()
      current_time = now.strftime('%H:%M:%S')
      print('Current Time:', current_time)
      today = date.today()
      
      if self.request.user.is_staff:
        return super().get_request()
      else:
        queryset = Flight.objects.filter(dateOfDepature__gt=today)
        if Flight.objects.filter(dateOfDepature=today):
            today_qs = Flight.objects.filter(dateOfDepature=today).filte(estimatedTimeOfDeparture__gt=now)
            queryset = queryset.union(today_qs)
        return queryset
  
class ReservationView(viewsets.ModelViewSet):
  queryset = Reservation.objects.all()
  serializer_class = ReservationSerializer
  
  def get_queryset(self):
    queryset=super().get_queryset()
    if self.request.user.is_staff:
      return queryset
    return queryset.filter(user=self.request.user)

