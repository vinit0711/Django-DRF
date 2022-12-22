from django.shortcuts import render
from .models import Course, CourseSerializer, Instructor, InstructorSerializer
from rest_framework.views import APIView
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

from rest_framework.response import Response

from rest_framework import mixins, generics

from rest_framework.permissions import IsAuthenticated, BasePermission

from rest_framework.authentication import TokenAuthentication, BasicAuthentication
# Create your views here.


class CustomPermissionClass(BasePermission):
    def has_permission(self, request, view):
        # get user and if user is required user return true
        # Also we can check here if request is get , post , delete
        return True


class InstructorListView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class CourseListView(generics.ListAPIView, generics.CreateAPIView):

    # Token based authenctication
    authenctication_classes = [TokenAuthentication]

    # # Basic Authenctication based authenctication
    # authenctication_classes = [BasicAuthentication]

    # NOte here you can have any custome permission class
    permission_classes = [IsAuthenticated, CustomPermissionClass]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# also in combination you can use generics.RereiveUpdateDestroyView

class CourseDetailView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


'''
# BELOW 2 classed use Mixins and generics view

class CourseListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class CourseDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    # not retirve used for getting 1 object only

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
'''

'''
# BELOW 2 CLass use API VIEW without generics and mixins
# This is used for normal get ,post requests with API VIEW


class CourseListView(APIView):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        courseSerializer = CourseSerializer(data=request.data)
        if courseSerializer.is_valid():
            courseSerializer.save()
            return Response(courseSerializer.data, status=status.HTTP_201_CREATED)
        return Response(courseSerializer.errors)

# Primary key Based Operations with API VIEW


class CourseDetailView(APIView):
    def get_course(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404("Not Found")

    def get(self, request, pk):
        course = self.get_course(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def delete(self, request, pk):
        course = self.get_course(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        course = self.get_course(pk)
        serializerOutput = CourseSerializer(course, data=request.data)
        if serializerOutput.is_valid():
            serializerOutput.save()
            return Response(serializerOutput.data)
        else:
            return Response(serializerOutput._errors)



'''
