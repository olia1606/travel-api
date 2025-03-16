from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from travels.models import TravelPackage, Destination
from travels.serializers import TravelPackageSerializer, DestinationSerializer


# Create your views here.

class TravelViewSet(viewsets.ModelViewSet):
    queryset = TravelPackage.objects.all()
    serializer_class = TravelPackageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['destination', 'price', 'duration']
    search_fields = ['destination__name', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()

        order_by = self.request.query_params.get("orderBy")
        search_query = self.request.query_params.get("search")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        if order_by in ["price", "-price"]:
            queryset = queryset.order_by(order_by)

        return queryset

    @action(detail=False, methods=['GET'], url_path='by-price-and-dest')
    def by_price_and_dest(self, request):
        price = request.query_params.get('price')
        dest = request.query_params.get('dest')
        if price is None:
            return Response({'error': 'Parameter price is required'}, status=400)

        if dest is None:
            return Response({'error': 'Parameter dest is required'}, status=400)

        travels = TravelPackage.objects.filter(Q(price__lte=price) | (Q(destination_id=dest) & ~Q(price__lte=price)))
        serializer = TravelPackageSerializer(travels, many=True)
        return Response(serializer.data)


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
