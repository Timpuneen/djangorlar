# Django modules
from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    PROTECT,
    CASCADE,
)
from django.contrib.auth.models import User

# Project modules
from apps.abstracts.models import AbstractSoftDeletableModel


class Project(AbstractSoftDeletableModel):
    """
    Project database (table) model.
    """

    NAME_MAX_LEN = 100

    name = CharField(
        max_length=NAME_MAX_LEN,
        verbose_name="Project Name"
    )
    author = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name="owned_projects",
        verbose_name="Author"
    )
    users = ManyToManyField(
        to=User,
        blank=True,
        related_name="joined_projects",
        verbose_name="Team Members"
    )

    class Meta:
        """Meta options for Project model."""
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]

    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Project(id={self.id}, name={self.name})"

    def __str__(self) -> str:
        """Returns the string representation of the object."""
        return self.name


class Task(AbstractSoftDeletableModel):
    """
    Task database (table) model.
    """

    NAME_MAX_LEN = 200
    STATUS_TODO = 1
    STATUS_TODO_LABEL = "To Do"
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PROGRESS_LABEL = "In Progress"
    STATUS_DONE = 3
    STATUS_DONE_LABEL = "Done"
    
    STATUS_CHOICES = {
        STATUS_TODO: STATUS_TODO_LABEL,
        STATUS_IN_PROGRESS: STATUS_IN_PROGRESS_LABEL,
        STATUS_DONE: STATUS_DONE_LABEL,
    }

    name = CharField(
        max_length=NAME_MAX_LEN,
        db_index=True,
        verbose_name="Task Name"
    )
    description = TextField(
        blank=True,
        default="",
        verbose_name="Description"
    )
    status = IntegerField(
        default=STATUS_TODO,
        choices=STATUS_CHOICES,
        verbose_name="Status"
    )
    parent = ForeignKey(
        to="self",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="subtasks",
        verbose_name="Parent Task"
    )
    project = ForeignKey(
        to=Project,
        on_delete=CASCADE,
        related_name="tasks",
        verbose_name="Project"
    )
    assignees = ManyToManyField(
        to=User,
        through="UserTask",
        through_fields=("task", "user"),
        blank=True,
        related_name="assigned_tasks",
        verbose_name="Assignees"
    )

    class Meta:
        """Meta options for Task model."""
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Task(id={self.id}, name={self.name}, status={self.status})"

    def __str__(self) -> str:
        """Returns the string representation of the object."""
        return self.name


class UserTask(AbstractSoftDeletableModel):
    """
    UserTask database (table) model - through model for Task-User relationship.
    """

    task = ForeignKey(
        to=Task,
        on_delete=CASCADE,
        verbose_name="Task"
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        verbose_name="User"
    )

    class Meta:
        """Customization of the model's meta data."""
        verbose_name = "User Task Assignment"
        verbose_name_plural = "User Task Assignments"
        constraints = [
            UniqueConstraint(
                fields=["task", "user"],
                name="unique_task_user",
            ),
        ]
        ordering = ["-created_at"]

    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"UserTask(id={self.id}, task={self.task_id}, user={self.user_id})"

    def __str__(self) -> str:
        """Returns the string representation of the object."""
        return f"{self.user.username} - {self.task.name}"