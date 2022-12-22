from django.db import models
from rest_framework import serializers

# Create your models here.


class Instructor(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    price = models.IntegerField()
    duration = models.IntegerField()
    discount = models.FloatField()
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name='course')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer):
    # This is nested serializer . Now when we list instructors , courses linked to instructor would be displayed
    course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = '__all__'
