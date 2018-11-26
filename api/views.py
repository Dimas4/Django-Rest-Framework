from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

from .serializers import PersonOneSerializer, PersonListSerializer, PersonPutSerializer, CompanyOneSerializer, CompanyListSerializer, CompanyPutSerializer


from .models import Company, Person


class CompanyOneAPIView(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, id):
        profile = Company.objects.get(id=id)
        serializer = CompanyOneSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = CompanyPutSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyListAPIView(APIView):
    def get(self, request):
        profiles = Company.objects.all()
        paginator = Paginator(profiles, 3)
        page = request.GET.get('page')

        try:
            cart_details = paginator.page(page)
        except PageNotAnInteger:
            cart_details = paginator.page(1)
        except EmptyPage:
            cart_details = paginator.page(paginator.num_pages)

        serializer = CompanyListSerializer(cart_details, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanyOneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonOneAPIView(APIView):
    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, id):
        profile = Person.objects.get(id=id)
        serializer = PersonOneSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = PersonPutSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonListAPIView(APIView):
    def get(self, request):
        profiles = Person.objects.all()
        serializer = PersonListSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonOneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
