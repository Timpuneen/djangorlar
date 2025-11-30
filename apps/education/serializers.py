
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import models
from apps.education.models import Course, Lesson
from decimal import Decimal


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class LessonSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'content', 'order', 
            'indentation', 'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'order', 'indentation']
        read_only_fields = ['id', 'course', 'order', 'indentation']
    
    def create(self, validated_data):
        course = self.context.get('course')
        validated_data['course'] = course
        
        max_order = Lesson.objects.filter(
            course=course
        ).aggregate(models.Max('order'))['order__max']
        
        if max_order is not None:
            validated_data['order'] = max_order - Decimal('1.00')
        else:
            validated_data['order'] = Decimal('0.00')
        
        validated_data['indentation'] = 0
        
        return super().create(validated_data)


class LessonMoveSerializer(serializers.Serializer):
    before_lesson_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_before_lesson_id(self, value):
        if value is not None:
            lesson = self.context.get('lesson')
            try:
                before_lesson = Lesson.objects.get(id=value, course=lesson.course)
            except Lesson.DoesNotExist:
                raise serializers.ValidationError(
                    "Invalid before_lesson_id: Lesson does not exist in the same course."
                )
        return value


class CourseListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'is_active', 
            'created_at', 'updated_at', 'owner', 'lessons_count'
        ]
    
    def get_lessons_count(self, obj):
        return obj.lessons.filter(deleted_at__isnull=True).count()


class CourseDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'is_active', 
            'created_at', 'updated_at', 'owner', 'lessons_count'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_lessons_count(self, obj):
        return obj.lessons.filter(deleted_at__isnull=True).count()


class CourseCreateUpdateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)