# Python modules
from typing import Optional

# Django modules
from django.contrib.admin import ModelAdmin, register, TabularInline
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.utils.html import format_html

# Project modules
from apps.tasks.models import Task, UserTask, Project


class UserTaskInline(TabularInline):
    """Inline for UserTask in Task admin."""
    model = UserTask
    extra = 1
    fields = ("user", "created_at")
    readonly_fields = ("created_at",)
    verbose_name = "Assignee"
    verbose_name_plural = "Assignees"


@register(Project)
class ProjectAdmin(ModelAdmin):
    """
    Project admin configuration class.
    """

    list_display = (
        "id",
        "name",
        "author",
        "team_members_count",
        "tasks_count",
        "status_badge",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "name",
        "author__username",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    filter_horizontal = (
        "users",
    )
    save_on_top = True
    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "name",
                    "author",
                    "users",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
                "classes": ("collapse",),
            }
        )
    )
    actions = ["soft_delete_selected", "restore_selected", "hard_delete_selected"]

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        """Show all objects including soft-deleted."""
        return self.model.objects.all()

    def team_members_count(self, obj: Project) -> int:
        """Get count of team members."""
        return obj.users.count()
    team_members_count.short_description = "Team Members"

    def tasks_count(self, obj: Project) -> int:
        """Get count of tasks."""
        return obj.tasks.count()
    tasks_count.short_description = "Tasks"

    def status_badge(self, obj: Project) -> str:
        """Display status badge."""
        if obj.is_deleted:
            return format_html(
                '<span style="background-color: #dc3545; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Deleted</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; '
            'padding: 3px 10px; border-radius: 3px;">Active</span>'
        )
    status_badge.short_description = "Status"

    def soft_delete_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Soft delete selected objects."""
        count = queryset.alive().count()
        queryset.alive().delete()
        self.message_user(request, f"{count} project(s) soft deleted successfully.")
    soft_delete_selected.short_description = "Soft delete selected projects"

    def restore_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Restore selected soft-deleted objects."""
        count = 0
        for obj in queryset.dead():
            obj.restore()
            count += 1
        self.message_user(request, f"{count} project(s) restored successfully.")
    restore_selected.short_description = "Restore selected projects"

    def hard_delete_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Hard delete selected objects permanently."""
        count = queryset.count()
        for obj in queryset:
            obj.hard_delete()
        self.message_user(request, f"{count} project(s) permanently deleted.")
    hard_delete_selected.short_description = "Permanently delete selected projects"


@register(Task)
class TaskAdmin(ModelAdmin):
    """
    Task admin configuration class.
    """

    list_display = (
        "id",
        "name",
        "project",
        "status_display",
        "parent",
        "assignees_count",
        "status_badge",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "name",
        "description",
        "project__name",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "status",
        "project",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    save_on_top = True
    inlines = [UserTaskInline]
    fieldsets = (
        (
            "Task Information",
            {
                "fields": (
                    "name",
                    "description",
                    "status",
                    "project",
                    "parent",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
                "classes": ("collapse",),
            }
        )
    )
    actions = ["soft_delete_selected", "restore_selected", "hard_delete_selected", "mark_as_done"]

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        """Show all objects including soft-deleted."""
        return self.model.objects.all()

    def status_display(self, obj: Task) -> str:
        """Display status as text."""
        return obj.get_status_display()
    status_display.short_description = "Status"

    def assignees_count(self, obj: Task) -> int:
        """Get count of assignees."""
        return obj.assignees.count()
    assignees_count.short_description = "Assignees"

    def status_badge(self, obj: Task) -> str:
        """Display status badge."""
        if obj.is_deleted:
            return format_html(
                '<span style="background-color: #dc3545; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Deleted</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; '
            'padding: 3px 10px; border-radius: 3px;">Active</span>'
        )
    status_badge.short_description = "Status"

    def soft_delete_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Soft delete selected objects."""
        count = queryset.alive().count()
        queryset.alive().delete()
        self.message_user(request, f"{count} task(s) soft deleted successfully.")
    soft_delete_selected.short_description = "Soft delete selected tasks"

    def restore_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Restore selected soft-deleted objects."""
        count = 0
        for obj in queryset.dead():
            obj.restore()
            count += 1
        self.message_user(request, f"{count} task(s) restored successfully.")
    restore_selected.short_description = "Restore selected tasks"

    def hard_delete_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Hard delete selected objects permanently."""
        count = queryset.count()
        for obj in queryset:
            obj.hard_delete()
        self.message_user(request, f"{count} task(s) permanently deleted.")
    hard_delete_selected.short_description = "Permanently delete selected tasks"

    def mark_as_done(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Mark selected tasks as done."""
        count = queryset.update(status=Task.STATUS_DONE)
        self.message_user(request, f"{count} task(s) marked as done.")
    mark_as_done.short_description = "Mark as Done"


@register(UserTask)
class UserTaskAdmin(ModelAdmin):
    """
    UserTask admin configuration class.
    """

    list_display = (
        "id",
        "user",
        "task",
        "task_project",
        "task_status",
        "status_badge",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "user__username",
        "task__name",
        "task__project__name",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "task__status",
        "task__project",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    save_on_top = True
    fieldsets = (
        (
            "Assignment Information",
            {
                "fields": (
                    "task",
                    "user",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
                "classes": ("collapse",),
            }
        )
    )
    actions = ["soft_delete_selected", "restore_selected", "hard_delete_selected"]

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        """Show all objects including soft-deleted."""
        return self.model.objects.all().select_related("task", "user", "task__project")

    def task_project(self, obj: UserTask) -> str:
        """Get task's project name."""
        return obj.task.project.name
    task_project.short_description = "Project"

    def task_status(self, obj: UserTask) -> str:
        """Get task's status."""
        return obj.task.get_status_display()
    task_status.short_description = "Task Status"

    def status_badge(self, obj: UserTask) -> str:
        """Display status badge."""
        if obj.is_deleted:
            return format_html(
                '<span style="background-color: #dc3545; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Deleted</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; '
            'padding: 3px 10px; border-radius: 3px;">Active</span>'
        )
    status_badge.short_description = "Status"

    def soft_delete_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Soft delete selected objects."""
        count = queryset.alive().count()
        queryset.alive().delete()
        self.message_user(request, f"{count} assignment(s) soft deleted successfully.")
    soft_delete_selected.short_description = "Soft delete selected assignments"

    def restore_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Restore selected soft-deleted objects."""
        count = 0
        for obj in queryset.dead():
            obj.restore()
            count += 1
        self.message_user(request, f"{count} assignment(s) restored successfully.")
    restore_selected.short_description = "Restore selected assignments"

    def hard_delete_selected(self, request: WSGIRequest, queryset: QuerySet) -> None:
        """Hard delete selected objects permanently."""
        count = queryset.count()
        for obj in queryset:
            obj.hard_delete()
        self.message_user(request, f"{count} assignment(s) permanently deleted.")
    hard_delete_selected.short_description = "Permanently delete selected assignments"