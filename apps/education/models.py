from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from decimal import Decimal

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='owner_courses')

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes soft-deleted records

    class Meta:
        db_table = 'education_courses'
        ordering = ['-created_at']

    def soft_delete(self):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save()
        
        for lesson in self.lessons.all():
            lesson.soft_delete()

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    indentation = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes soft-deleted records

    class Meta:
        db_table = 'education_lessons'
        ordering = ['order', 'created_at']

    def soft_delete(self):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} ({self.course.title})"
