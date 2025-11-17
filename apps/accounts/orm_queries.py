"""50 ORM Queries for practice-7-orm"""

from django.contrib.auth import get_user_model
from django.db.models import Q, F, Count, Avg, Sum, Max, Min, Value, Case, When, ExpressionWrapper, fields
from django.utils import timezone
from django.db.models.functions import Concat, ExtractYear, Now

from datetime import timedelta, datetime

User = get_user_model()

def query_2_1():
    """Get all active users."""
    result = User.objects.filter(is_active=True)
    print(f'Query 2.1 count: {result.count()}')
    print(f'Query 2.1 Result: {result}')
    return result

def query_2_2():
    """Get users with email ends with @gmail.com."""
    result = User.objects.filter(email__iendswith="@gmail.com")
    print(f'Query 2.2 count: {result.count()}')
    print(f'Query 2.2 Result: {result}')
    return result

def query_2_3():
    """All users from Almaty city."""
    result = User.objects.filter(city__iexact="Almaty")
    print(f'Query 2.3 count: {result.count()}')
    print(f'Query 2.3 Result: {result}')
    return result

def query_2_4():
    """All users not from Almaty city."""
    result = User.objects.exclude(city__iexact="Almaty")
    print(f'Query 2.4 count: {result.count()}')
    print(f'Query 2.4 Result: {result}')
    return result

def query_2_5():
    """Users with salary greater than 500,000."""
    result = User.objects.filter(salary__gt=500000)
    print(f'Query 2.5 count: {result.count()}')
    print(f'Query 2.5 Result: {result}')
    return result

def query_2_6():
    """Users from IT department and country Kazakhstan."""
    result = User.objects.filter(department='IT', country__iexact='Kazakhstan')
    print(f'Query 2.6 count: {result.count()}')
    print(f'Query 2.6 Result: {result}')
    return result

def query_2_7():
    """Users withh null birth_date."""
    result = User.objects.filter(birth_date__isnull=True)
    print(f'Query 2.7 count: {result.count()}')
    print(f'Query 2.7 Result: {result}')
    return result

def query_2_8():
    """Users with firt name starting with A."""
    result = User.objects.filter(first_name__istartswith='A')
    print(f'Query 2.8 count: {result.count()}')
    print(f'Query 2.8 Result: {result}')
    return result

def query_2_9():
    """Get the total number of users."""
    result = User.objects.count()
    print(f'Query 2.9 Result: {result}')
    return result

def query_2_10():
    """First 20 users ordered by date joined descending."""
    result = User.objects.all().order_by('-date_joined')[:20]
    print(f'Query 2.10 count: {result.count()}')
    print(f'Query 2.10 Result: {result}')
    return result

def query_2_11():
    """Get distinct list of cities of all users"""
    result = User.objects.values_list('city', flat=True).distinct()
    print(f'Query 2.11 count: {result.count()}')
    print(f'Query 2.11 Result: {result}')
    return result

def query_2_12():
    """Count users from Sales department."""
    result = User.objects.filter(department='Sales').count()
    print(f'Query 2.12 Result: {result}')
    return result

def query_2_13():
    """Users who logged in within the last 7 days."""
    one_week_ago = timezone.now() - timedelta(days=7)
    result = User.objects.filter(last_login__gte=one_week_ago)
    print(f'Query 2.13 count: {result.count()}')
    print(f'Query 2.13 Result: {result}')
    return result

def query_2_14():
    """All users whose name or surname contains 'bek'."""
    result = User.objects.filter(Q(first_name__icontains='bek') | Q(last_name__icontains='bek'))
    print(f'Query 2.14 count: {result.count()}')
    print(f'Query 2.14 Result: {result}')
    return result

def query_2_15():
    """All users whose salary is between 300,000 and 700,000."""
    result = User.objects.filter(salary__gte=300000, salary__lte=700000)
    print(f'Query 2.15 count: {result.count()}')
    print(f'Query 2.15 Result: {result}')
    return result

def query_2_16():
    """All users from departments IT, HR, and Finance."""
    result = User.objects.filter(department__in=['IT', 'HR', 'Finance'])
    print(f'Query 2.16 count: {result.count()}')
    print(f'Query 2.16 Result: {result}')
    return result

def query_2_17():
    """Group users by department and count number of users in each department."""
    result = User.objects.values('department').annotate(user_count=Count('id'))
    print(f'Query 2.17 Result: {result}')
    return result

def query_2_18():
    """Same as query_2_17 but ordered by user_count descending."""
    result = User.objects.values('department').annotate(user_count=Count('id')).order_by('-user_count')
    print(f'Query 2.18 Result: {result}')
    return result

def query_2_19():
    """Top 5 cities with highest number of users."""
    result = User.objects.values('city').annotate(user_count=Count('id')).order_by('-user_count')[:5]
    print(f'Query 2.19 Result: {result}')
    return result

def query_2_20():
    """All users who never logged in."""
    result = User.objects.filter(last_login__isnull=True)
    print(f'Query 2.20 count: {result.count()}')
    print(f'Query 2.20 Result: {result}')
    return result

def query_2_21():
    """Average salary of all users"""
    result = User.objects.aggregate(average_salary=Avg('salary'))
    print(f'Query 2.21 Result: {result}')
    return result

def query_2_22():
    """Max and min salary among all users."""
    result = User.objects.aggregate(max_salary=Max('salary'), min_salary=Min('salary'))
    print(f'Query 2.22 Result: {result}')
    return result

def query_2_23():
    """All users with phone number containining '+7'."""
    result = User.objects.filter(phone__icontains='+7')
    print(f'Query 2.23 count: {result.count()}')
    print(f'Query 2.23 Result: {result}')
    return result

def query_2_24():
    """Annotate users with full name field."""
    result = User.objects.annotate(full_name=Concat(F('first_name'), Value(' '), F('last_name')))
    print(f'Query 2.24 count: {result.count()}')
    for user in result:
        print(f'User: {user.full_name}')
    return result

def query_2_25():
    """Annotate each user with birth year and order by birth year ascending."""
    result = User.objects.annotate(birth_year=ExtractYear('birth_date')).order_by('birth_year')
    print(f'Query 2.25 count: {result.count()}')
    for user in result:
        print(f'User: {user}, Birth Year: {user.birth_year}')
    return result

def query_2_26():
    """All users born in May"""
    result = User.objects.filter(birth_date__month=5)
    print(f'Query 2.26 count: {result.count()}')
    print(f'Query 2.26 Result: {result}')
    return result

def query_2_27():
    """Users with role 'manager' and salary greater than 400,000."""
    result = User.objects.filter(role='manager', salary__gt=400000)
    print(f'Query 2.27 count: {result.count()}')
    print(f'Query 2.27 Result: {result}')
    return result

def query_2_28():
    """Users with role 'employee' or from HR department."""
    result = User.objects.filter(Q(role='employee') | Q(department='HR'))
    print(f'Query 2.28 count: {result.count()}')
    print(f'Query 2.28 Result: {result}')
    return result

def query_2_29():
    """Count active users in each city"""
    result = User.objects.filter(is_active=True).values('city').annotate(active_user_count=Count('id'))
    print(f'Query 2.29 Result: {result}')
    return result

def query_2_30():
    """10 earliest joined users."""
    result = User.objects.all().order_by('date_joined')[:10]
    print(f'Query 2.30 count: {result.count()}')
    print(f'Query 2.30 Result: {result}')
    return result

def query_2_31():
    """Users with city starts with 'A' and salary more than 300000"""
    result = User.objects.filter(city__istartswith='A', salary__gt=300000)
    print(f'Query 2.31 count: {result.count()}')
    print(f'Query 2.31 Result: {result}')
    return result

def query_2_32():
    """Users with empty or null department field."""
    result = User.objects.filter(Q(department__isnull=True) | Q(department__exact=''))
    print(f'Query 2.32 count: {result.count()}')
    print(f'Query 2.32 Result: {result}')
    return result

def query_2_33():
    """Get stats by country: name, count of users, average salary."""
    result = User.objects.values('country').annotate(
        user_count=Count('id'),
        average_salary=Avg('salary')
    )
    print(f'Query 2.33 Result: {result}')
    return result

def query_2_34():
    """All users ordered by last_login descending."""
    result = User.objects.all().order_by('-last_login')
    print(f'Query 2.34 count: {result.count()}')
    print(f'Query 2.34 Result: {result}')
    return result

def query_2_35():
    """All users with email does not contain 'example.com'."""
    result = User.objects.exclude(email__icontains='example.com')
    print(f'Query 2.35 count: {result.count()}')
    print(f'Query 2.35 Result: {result}')
    return result

def query_2_36():
    """All users with salary higher than average salary."""
    average_salary = User.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
    result = User.objects.filter(salary__gt=average_salary)
    print(f'Query 2.36 count: {result.count()}')
    print(f'Query 2.36 Result: {result}')
    return result

def query_2_37():
    """Find emails used by more than one user."""
    result = User.objects.values('email').annotate(email_count=Count('id')).filter(email_count__gt=1)
    print(f'Query 2.37 Result: {result}')
    return result

def query_2_38():
    """Annotate users by salary level: High (>700k), Medium (400k-700k), Low (<400k). and order by salary level."""
    salary_level = Case(
        When(salary__gt=700000, then=Value('High')),
        When(salary__gte=400000, salary__lte=700000, then=Value('Medium')),
        When(salary__lt=400000, then=Value('Low')),
        default=Value('Unknown'),
        output_field=fields.CharField(),
    )
    result = User.objects.annotate(salary_level=salary_level).order_by('salary_level')
    print(f'Query 2.38 count: {result.count()}')
    for user in result:
        print(f'User: {user}, Salary Level: {user.salary_level}')
    return result

def query_2_39():
    """All users whose date_joined is within the current year."""
    current_year = timezone.now().year
    result = User.objects.filter(date_joined__year=current_year)
    print(f'Query 2.39 count: {result.count()}')
    print(f'Query 2.39 Result: {result}')
    return result

def query_2_40():
    """total payroll per department."""
    result = User.objects.values('department').annotate(total_payroll=Sum('salary'))
    print(f'Query 2.40 Result: {result}')
    return result

def query_2_41():
    """IT users who never logged in."""
    result = User.objects.filter(department='IT', last_login__isnull=True)
    print(f'Query 2.41 count: {result.count()}')
    print(f'Query 2.41 Result: {result}')
    return result

def query_2_42():
    """Users from Kazakhstan with null or empty city field."""
    result = User.objects.filter(country__iexact='Kazakhstan').filter(Q(city__isnull=True) | Q(city__exact=''))
    print(f'Query 2.42 count: {result.count()}')
    print(f'Query 2.42 Result: {result}')
    return result

def query_2_43():
    """Users born befor 1990 with non null salary."""
    result = User.objects.filter(birth_date__lt=datetime(1990, 1, 1), salary__isnull=False)
    print(f'Query 2.43 count: {result.count()}')
    print(f'Query 2.43 Result: {result}')
    return result

def query_2_44():
    """Annoutate users with year since joined."""
    result = User.objects.annotate(years_since_joined=ExpressionWrapper(
        Now() - F('date_joined'),
        output_field=fields.DurationField()
    ))
    print(f'Query 2.44 count: {result.count()}')
    for user in result:
        years = user.years_since_joined.days // 365
        print(f'User: {user}, Years Since Joined: {years}')
    return result

def query_2_45():
    """Get Sales users with gmail and salary > 350000."""
    result = User.objects.filter(
        department='Sales',
        email_ienswith="@gmail.com",
        salary__gt=350000
    )
    print(f'Query 2.45 count: {result.count()}')
    print(f'Query 2.45 Result: {result}')
    return result

def query_2_46():
    """Order users by country then by salary descending."""
    result = User.objects.all().order_by('country', '-salary')
    print(f'Query 2.46 count: {result.count()}')
    print(f'Query 2.46 Result: {result}')
    return result

def query_2_47():
    """Get users count per role, show only roles with more than 100 users."""
    result = User.objects.values('role').annotate(role_count=Count('id')).filter(role_count__gt=100)
    print(f'Query 2.47 Result: {result}')
    return result

def query_2_48():
    """Get users whose last_login is earlier than date_joined."""
    result = User.objects.filter(last_login__lt=F('date_joined'))
    print(f'Query 2.48 count: {result.count()}')
    print(f'Query 2.48 Result: {result}')
    return result
    
def query_2_49():
    """Annotate users with is_senior flag (True if birth_date is before 1985-01-01)."""
    result = User.objects.annotate(
        is_senior=Case(
            When(birth_date__lt=datetime(1985, 1, 1), then=Value(True)),
            default=Value(False),
            output_field=fields.BooleanField(),
        )
    )
    print(f'Query 2.49 count: {result.count()}')
    for user in result:
        print(f'User: {user}, Is Senior: {user.is_senior}')
    return result

def query_2_50():
    """Get departments sorted by average salary descending with at least 20 users."""
    result = User.objects.values('department').annotate(
        avg_salary=Avg('salary'),
        user_count=Count('id')
    ).filter(user_count__gte=20).order_by('-avg_salary')
    print(f'Query 2.50 Result: {result}')
    return result

def run_all():
    """Run all 50 queries."""
    print("="*20 + " Running All Queries " + "="*20)
    queries = [
        query_2_1, query_2_2, query_2_3, query_2_4, query_2_5, 
        query_2_6, query_2_7, query_2_8, query_2_9, query_2_10,
        query_2_11, query_2_12, query_2_13, query_2_14, query_2_15,
        query_2_16, query_2_17, query_2_18, query_2_19, query_2_20,
        query_2_21, query_2_22, query_2_23, query_2_24, query_2_25,
        query_2_26, query_2_27, query_2_28, query_2_29, query_2_30,
        query_2_31, query_2_32, query_2_33, query_2_34, query_2_35,
        query_2_36, query_2_37, query_2_38, query_2_39, query_2_40,
        query_2_41, query_2_42, query_2_43, query_2_44, query_2_45,
        query_2_46, query_2_47, query_2_48, query_2_49, query_2_50,
    ]
    
    for query in queries:
        print("\n" + "-"*10 + f" Executing {query.__name__} " + "-"*10)
        try:
            query()
        except Exception as e:
            print(f'Error executing {query.__name__}: {e}')
            
    print("="*20 + " Finished All Queries " + "="*20)

if __name__ == "__main__":
    run_all()