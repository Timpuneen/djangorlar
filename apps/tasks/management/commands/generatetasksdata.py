# Python modules
import random
from typing import Any

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# Project modules
from apps.tasks.models import Project, Task, UserTask


class Command(BaseCommand):
    """Management command to generate test data for tasks app."""

    help = "Generate 20 test records for each model (Project, Task, UserTask)"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """Execute command."""
        self.stdout.write(self.style.SUCCESS("Starting data generation..."))

        # Create users if needed
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f"Users ready: {len(users)}"))

        # Create projects
        projects = self.create_projects(users)
        self.stdout.write(self.style.SUCCESS(f"Created {len(projects)} projects"))

        # Create tasks
        tasks = self.create_tasks(projects)
        self.stdout.write(self.style.SUCCESS(f"Created {len(tasks)} tasks"))

        # Create user-task assignments
        user_tasks = self.create_user_tasks(tasks, users)
        self.stdout.write(self.style.SUCCESS(f"Created {len(user_tasks)} user-task assignments"))

        self.stdout.write(self.style.SUCCESS("Data generation completed successfully!"))

    def create_users(self) -> list[User]:
        """Create or get existing users."""
        users = []
        usernames = [
            "john_doe", "jane_smith", "alice_wonder", "bob_builder",
            "charlie_brown", "diana_prince", "edward_stark", "fiona_apple",
            "george_martin", "hannah_montana"
        ]

        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": username.split("_")[0].capitalize(),
                    "last_name": username.split("_")[1].capitalize(),
                }
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        return users

    def create_projects(self, users: list[User]) -> list[Project]:
        """Create 20 projects."""
        projects = []
        project_names = [
            "E-commerce Platform", "Mobile Banking App", "Social Media Dashboard",
            "Healthcare Portal", "Education System", "Inventory Management",
            "Customer Support Tool", "Marketing Analytics", "HR Management System",
            "Real Estate Platform", "Travel Booking System", "Food Delivery App",
            "Fitness Tracker", "Music Streaming Service", "Video Conference Tool",
            "Project Management Suite", "Blog Platform", "Job Board",
            "Event Planning System", "Financial Dashboard"
        ]

        for i, name in enumerate(project_names):
            author = random.choice(users)
            project = Project.objects.create(
                name=name,
                author=author
            )
            # Add random team members
            team_members = random.sample(users, k=random.randint(2, 6))
            project.users.set(team_members)
            projects.append(project)

        return projects

    def create_tasks(self, projects: list[Project]) -> list[Task]:
        """Create 20 tasks."""
        tasks = []
        task_templates = [
            ("Design Homepage", "Create wireframes and mockups for the homepage"),
            ("Implement Authentication", "Set up user login and registration system"),
            ("Database Schema", "Design and implement database architecture"),
            ("API Development", "Build RESTful API endpoints"),
            ("Frontend Integration", "Connect frontend with backend APIs"),
            ("Unit Testing", "Write comprehensive unit tests"),
            ("Bug Fixes", "Fix reported bugs from QA team"),
            ("Performance Optimization", "Improve application performance"),
            ("Security Audit", "Conduct security vulnerability assessment"),
            ("Documentation", "Write technical and user documentation"),
            ("Code Review", "Review and refactor existing codebase"),
            ("Deploy to Production", "Deploy application to production server"),
            ("User Feedback Analysis", "Analyze and prioritize user feedback"),
            ("Feature Enhancement", "Add new features based on requirements"),
            ("Mobile Responsiveness", "Ensure mobile-friendly design"),
            ("Analytics Integration", "Integrate analytics tracking"),
            ("Payment Gateway", "Implement payment processing system"),
            ("Email Notifications", "Set up automated email system"),
            ("Search Functionality", "Implement advanced search feature"),
            ("Admin Dashboard", "Create admin control panel")
        ]

        statuses = [Task.STATUS_TODO, Task.STATUS_IN_PROGRESS, Task.STATUS_DONE]

        for i, (name, description) in enumerate(task_templates):
            project = random.choice(projects)
            task = Task.objects.create(
                name=name,
                description=description,
                status=random.choice(statuses),
                project=project,
                parent=None  # Can be updated later for subtasks
            )
            tasks.append(task)

        # Create some subtasks
        for _ in range(5):
            parent_task = random.choice(tasks)
            subtask = Task.objects.create(
                name=f"Subtask of {parent_task.name}",
                description=f"Additional work for {parent_task.name}",
                status=random.choice(statuses),
                project=parent_task.project,
                parent=parent_task
            )
            tasks.append(subtask)

        return tasks

    def create_user_tasks(self, tasks: list[Task], users: list[User]) -> list[UserTask]:
        """Create 20 user-task assignments."""
        user_tasks = []
        created_pairs = set()

        attempts = 0
        max_attempts = 100

        while len(user_tasks) < 20 and attempts < max_attempts:
            task = random.choice(tasks)
            user = random.choice(users)
            pair = (task.id, user.id)

            if pair not in created_pairs:
                try:
                    user_task = UserTask.objects.create(
                        task=task,
                        user=user
                    )
                    user_tasks.append(user_task)
                    created_pairs.add(pair)
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Could not create UserTask: {e}")
                    )

            attempts += 1

        return user_tasks