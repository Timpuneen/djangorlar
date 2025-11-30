from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models
from decimal import Decimal

from apps.education.models import Course, Lesson
from apps.education.serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    CourseCreateUpdateSerializer,
    LessonSerializer,
    LessonCreateSerializer,
    LessonMoveSerializer,
)
from apps.education.permissions import IsCourseOwner


class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = Course.objects.all()
        
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)
        
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CourseCreateUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        
        if course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to update this course'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CourseCreateUpdateSerializer(
            course,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        
        if course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to delete this course'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        
        if course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to activate this course'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if course.is_active:
            return Response(
                {'detail': 'Already active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course.is_active = True
        course.save()
        
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        
        if course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to deactivate this course'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        course.is_active = False
        course.save()
        
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='lessons')
    def lessons(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        course_id = request.data.get('course')
        if not course_id:
            return Response(
                {'detail': 'course field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course = get_object_or_404(Course, pk=course_id)
        
        if course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to add lessons to this course'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = LessonCreateSerializer(
            data=request.data,
            context={'course': course, 'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        
        if lesson.course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to move this lesson'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = LessonMoveSerializer(
            data=request.data,
            context={'lesson': lesson}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        before_lesson_id = serializer.validated_data.get('before_lesson_id')
        
        if before_lesson_id is None:
            max_order = Lesson.objects.filter(
                course=lesson.course
            ).aggregate(models.Max('order'))['order__max']
            
            if max_order is not None:
                lesson.order = max_order + Decimal('1.00')
            else:
                lesson.order = Decimal('0.00')
            
            lesson.indentation = 0
        else:
            before_lesson = get_object_or_404(Lesson, pk=before_lesson_id)
            
            prev_lesson = Lesson.objects.filter(
                course=lesson.course,
                order__lt=before_lesson.order
            ).order_by('-order').first()
            
            if prev_lesson:
                lesson.order = (prev_lesson.order + before_lesson.order) / 2
                lesson.indentation = before_lesson.indentation
            else:
                lesson.order = before_lesson.order - Decimal('1.00')
                lesson.indentation = 0
        
        lesson.save()
        
        return Response({'order': float(lesson.order)})
    
    def destroy(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        
        if lesson.course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to delete this lesson'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        lesson.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        
        if lesson.course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to publish this lesson'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        lesson.is_published = True
        lesson.save()
        
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        if lesson.course.owner != request.user:
            return Response(
                {'detail': 'Not authorized to unpublish this lesson'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        lesson.is_published = False
        lesson.save()
        
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)