import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from apps.education.models import Course, Lesson


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()


@pytest.fixture
def user():
    """Фикстура для создания пользователя"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def other_user():
    """Фикстура для создания другого пользователя"""
    return User.objects.create_user(
        username='otheruser',
        password='otherpass123',
        email='other@example.com'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Фикстура для аутентифицированного клиента"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def course(user):
    """Фикстура для создания курса"""
    return Course.objects.create(
        title='Test Course',
        description='Test Description',
        owner=user
    )


@pytest.fixture
def inactive_course(user):
    """Фикстура для создания неактивного курса"""
    return Course.objects.create(
        title='Inactive Course',
        description='Inactive Description',
        owner=user,
        is_active=False
    )


@pytest.fixture
def lesson(course):
    """Фикстура для создания урока"""
    return Lesson.objects.create(
        course=course,
        title='Test Lesson',
        content='Test Content',
        order=Decimal('1.00')
    )


# ==================== JWT AUTHENTICATION TESTS ====================

@pytest.mark.django_db
class TestJWTAuthentication:
    """Тесты для JWT аутентификации"""
    
    def test_obtain_token_success(self, api_client, user):
        """Тест успешного получения токена"""
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_obtain_token_invalid_credentials(self, api_client, user):
        """Тест получения токена с неверными данными"""
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_refresh_token_success(self, api_client, user):
        """Тест успешного обновления токена"""
        # Получаем токены
        url = '/api/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        refresh_token = response.data['refresh']
        
        # Обновляем токен
        url = '/api/token/refresh/'
        data = {'refresh': refresh_token}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_refresh_token_invalid(self, api_client):
        """Тест обновления токена с неверным refresh токеном"""
        url = '/api/token/refresh/'
        data = {'refresh': 'invalid_token'}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ==================== COURSE TESTS ====================

@pytest.mark.django_db
class TestCourseList:
    """Тесты для списка курсов"""
    
    def test_list_courses_success(self, authenticated_client, course):
        """Тест успешного получения списка курсов"""
        url = '/api/v1/education/courses/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Test Course'
        assert 'lessons_count' in response.data[0]
    
    def test_list_courses_unauthenticated(self, api_client, course):
        """Тест получения списка курсов без аутентификации"""
        url = '/api/v1/education/courses/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_courses_filter_active(self, authenticated_client, course, inactive_course):
        """Тест фильтрации курсов по is_active"""
        url = '/api/v1/education/courses/?is_active=true'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['is_active'] is True


@pytest.mark.django_db
class TestCourseCreate:
    """Тесты для создания курса"""
    
    def test_create_course_success(self, authenticated_client):
        """Тест успешного создания курса"""
        url = '/api/v1/education/courses/'
        data = {
            'title': 'New Course',
            'description': 'New Description'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Course'
        assert Course.objects.filter(title='New Course').exists()
    
    def test_create_course_missing_title(self, authenticated_client):
        """Тест создания курса без обязательного поля"""
        url = '/api/v1/education/courses/'
        data = {
            'description': 'Description without title'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCourseRetrieve:
    """Тесты для получения детальной информации о курсе"""
    
    def test_retrieve_course_success(self, authenticated_client, course):
        """Тест успешного получения курса"""
        url = f'/api/v1/education/courses/{course.id}/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Course'
    
    def test_retrieve_course_not_found(self, authenticated_client):
        """Тест получения несуществующего курса"""
        url = '/api/v1/education/courses/999/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCourseUpdate:
    """Тесты для обновления курса"""
    
    def test_update_course_success(self, authenticated_client, course):
        """Тест успешного обновления курса"""
        url = f'/api/v1/education/courses/{course.id}/'
        data = {
            'title': 'Updated Course',
            'description': 'Updated Description'
        }
        response = authenticated_client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Course'
    
    def test_update_course_not_owner(self, api_client, course, other_user):
        """Тест обновления курса не владельцем"""
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/courses/{course.id}/'
        data = {
            'title': 'Hacked Course',
            'description': 'Hacked Description'
        }
        response = api_client.put(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCourseDelete:
    """Тесты для удаления курса"""
    
    def test_delete_course_success(self, authenticated_client, course):
        """Тест успешного удаления курса"""
        url = f'/api/v1/education/courses/{course.id}/'
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Проверяем мягкое удаление
        course.refresh_from_db()
        assert course.deleted_at is not None
    
    def test_delete_course_not_owner(self, api_client, course, other_user):
        """Тест удаления курса не владельцем"""
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/courses/{course.id}/'
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCourseActivate:
    """Тесты для активации курса"""
    
    def test_activate_course_success(self, authenticated_client, inactive_course):
        """Тест успешной активации курса"""
        url = f'/api/v1/education/courses/{inactive_course.id}/activate/'
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_active'] is True
    
    def test_activate_already_active_course(self, authenticated_client, course):
        """Тест активации уже активного курса"""
        url = f'/api/v1/education/courses/{course.id}/activate/'
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCourseDeactivate:
    """Тесты для деактивации курса"""
    
    def test_deactivate_course_success(self, authenticated_client, course):
        """Тест успешной деактивации курса"""
        url = f'/api/v1/education/courses/{course.id}/deactivate/'
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_active'] is False
    
    def test_deactivate_course_not_owner(self, api_client, course, other_user):
        """Тест деактивации курса не владельцем"""
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/courses/{course.id}/deactivate/'
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCourseLessons:
    """Тесты для получения уроков курса"""
    
    def test_list_course_lessons_success(self, authenticated_client, course, lesson):
        """Тест успешного получения уроков курса"""
        url = f'/api/v1/education/courses/{course.id}/lessons/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Test Lesson'
    
    def test_list_course_lessons_empty(self, authenticated_client, course):
        """Тест получения уроков курса без уроков"""
        url = f'/api/v1/education/courses/{course.id}/lessons/'
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


# ==================== LESSON TESTS ====================

@pytest.mark.django_db
class TestLessonCreate:
    """Тесты для создания урока"""
    
    def test_create_lesson_success(self, authenticated_client, course):
        """Тест успешного создания урока"""
        url = '/api/v1/education/lessons/'
        data = {
            'course': course.id,
            'title': 'New Lesson',
            'content': 'New Content'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Lesson'
        assert Lesson.objects.filter(title='New Lesson').exists()
    
    def test_create_lesson_not_course_owner(self, api_client, course, other_user):
        """Тест создания урока не владельцем курса"""
        api_client.force_authenticate(user=other_user)
        url = '/api/v1/education/lessons/'
        data = {
            'course': course.id,
            'title': 'Hacked Lesson',
            'content': 'Hacked Content'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_lesson_missing_title(self, authenticated_client, course):
        """Тест создания урока без обязательного поля"""
        url = '/api/v1/education/lessons/'
        data = {
            'course': course.id,
            'content': 'Content without title'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLessonMove:
    """Тесты для перемещения урока"""
    
    def test_move_lesson_to_position_success(self, authenticated_client, course):
        """Тест успешного перемещения урока"""
        # Создаем несколько уроков
        lesson1 = Lesson.objects.create(
            course=course,
            title='Lesson 1',
            content='Content 1',
            order=Decimal('1.00')
        )
        lesson2 = Lesson.objects.create(
            course=course,
            title='Lesson 2',
            content='Content 2',
            order=Decimal('2.00')
        )
        lesson3 = Lesson.objects.create(
            course=course,
            title='Lesson 3',
            content='Content 3',
            order=Decimal('3.00')
        )
        
        # Перемещаем lesson3 перед lesson2
        url = f'/api/v1/education/lessons/{lesson3.id}/move/'
        data = {'before_lesson_id': lesson2.id}
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'order' in response.data
        
        # Проверяем, что order изменился
        lesson3.refresh_from_db()
        assert lesson3.order < lesson2.order
        assert lesson3.order > lesson1.order
    
    def test_move_lesson_to_end_success(self, authenticated_client, course, lesson):
        """Тест перемещения урока в конец"""
        url = f'/api/v1/education/lessons/{lesson.id}/move/'
        data = {'before_lesson_id': None}
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_move_lesson_not_owner(self, api_client, course, lesson, other_user):
        """Тест перемещения урока не владельцем"""
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/lessons/{lesson.id}/move/'
        data = {'before_lesson_id': None}
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_move_lesson_invalid_before_id(self, authenticated_client, course, lesson):
        """Тест перемещения урока с неверным before_lesson_id"""
        url = f'/api/v1/education/lessons/{lesson.id}/move/'
        data = {'before_lesson_id': 9999}
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLessonDelete:
    """Тесты для удаления урока"""
    
    def test_delete_lesson_success(self, authenticated_client, lesson):
        """Тест успешного удаления урока"""
        url = f'/api/v1/education/lessons/{lesson.id}/'
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Проверяем мягкое удаление
        lesson.refresh_from_db()
        assert lesson.deleted_at is not None
    
    def test_delete_lesson_not_owner(self, api_client, lesson, other_user):
        """Тест удаления урока не владельцем"""
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/lessons/{lesson.id}/'
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestLessonPublish:
    """Тесты для публикации урока"""
    
    def test_publish_lesson_success(self, authenticated_client, lesson):
        """Тест успешной публикации урока"""
        url = f'/api/v1/education/lessons/{lesson.id}/publish/'
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_published'] is True
        
        lesson.refresh_from_db()
        assert lesson.is_published is True
    
    def test_publish_lesson_not_owner(self, api_client, lesson, other_user):
        """Тест публикации урока не владельцем"""
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/lessons/{lesson.id}/publish/'
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestLessonUnpublish:
    """Тесты для снятия урока с публикации"""
    
    def test_unpublish_lesson_success(self, authenticated_client, lesson):
        """Тест успешного снятия урока с публикации"""
        # Сначала публикуем урок
        lesson.is_published = True
        lesson.save()
        
        url = f'/api/v1/education/lessons/{lesson.id}/unpublish/'
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_published'] is False
        
        lesson.refresh_from_db()
        assert lesson.is_published is False
    
    def test_unpublish_lesson_not_owner(self, api_client, lesson, other_user):
        """Тест снятия урока с публикации не владельцем"""
        lesson.is_published = True
        lesson.save()
        
        api_client.force_authenticate(user=other_user)
        url = f'/api/v1/education/lessons/{lesson.id}/unpublish/'
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

