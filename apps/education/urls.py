from django.urls import path
from .views import CourseViewSet, LessonViewSet

urlpatterns = [
    path('courses/', CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-list'),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='course-detail'),
    path('courses/<int:pk>/activate/', CourseViewSet.as_view({'post': 'activate'}), name='course-activate'),
    path('courses/<int:pk>/deactivate/', CourseViewSet.as_view({'post': 'deactivate'}), name='course-deactivate'),
    path('courses/<int:pk>/lessons/', CourseViewSet.as_view({'get': 'lessons'}), name='course-lessons'),
    path('lessons/', LessonViewSet.as_view({'post': 'create'}), name='lesson-create'),
    path('lessons/<int:pk>/move/', LessonViewSet.as_view({'put': 'move'}), name='lesson-move'),
    path('lessons/<int:pk>/', LessonViewSet.as_view({'delete': 'destroy'}), name='lesson-delete'),
    path('lessons/<int:pk>/publish/', LessonViewSet.as_view({'post': 'publish'}), name='lesson-publish'),
    path('lessons/<int:pk>/unpublish/', LessonViewSet.as_view({'post': 'unpublish'}), name='lesson-unpublish'),
]