from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate 10,000 users with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        departments = ['IT', 'HR', 'Sales', 'Finance']
        roles = ['admin', 'manager', 'employee']
        
        batch_size = 1000
        total_users = 10000
        
        self.stdout.write(self.style.SUCCESS(f'Starting to generate {total_users} users...'))
        
        for batch_num in range(total_users // batch_size):
            users_to_create = []
            
            print(f'Generating batch {batch_num + 1}...')
            
            for i in range(batch_size):
                user_number = batch_num * batch_size + i + 1
                
                print(f'Creating user {user_number}...')
                
                first_name = fake.first_name()
                last_name = fake.last_name()
                username = f"user_{user_number}"
                email = fake.unique.email()
                phone = fake.phone_number()
                city = fake.city()
                country = fake.country()
                department = random.choice(departments)
                role = random.choice(roles)
                
                birth_date = fake.date_of_birth(minimum_age=20, maximum_age=50)
                
                
                salary = random.randint(200000, 1000000)
                
                
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    city=city,
                    country=country,
                    department=department,
                    role=role,
                    birth_date=birth_date,
                    salary=salary,
                    is_active=True,
                )
                
                user.set_password('12345')
                
                users_to_create.append(user)
            
            User.objects.bulk_create(users_to_create, batch_size=batch_size)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Batch {batch_num + 1}/{total_users // batch_size} completed '
                    f'({(batch_num + 1) * batch_size} users created)'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated {total_users} users!'
            )
        )