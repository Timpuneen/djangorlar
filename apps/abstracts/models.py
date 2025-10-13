# Python modules
from typing import Any

# Django modules
from django.db.models import Model, DateTimeField, QuerySet, Manager
from django.utils import timezone as django_timezone


class SoftDeletableQuerySet(QuerySet):
    """Custom QuerySet for soft-deletable models."""

    def delete(self) -> tuple[int, dict[str, int]]:
        """Soft delete all objects in queryset."""
        return self.update(deleted_at=django_timezone.now())

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        """Permanently delete all objects in queryset."""
        return super().delete()

    def alive(self) -> QuerySet:
        """Return only non-deleted objects."""
        return self.filter(deleted_at__isnull=True)

    def dead(self) -> QuerySet:
        """Return only deleted objects."""
        return self.filter(deleted_at__isnull=False)


class SoftDeletableManager(Manager):
    """Custom Manager for soft-deletable models."""

    def get_queryset(self) -> QuerySet:
        """Return custom queryset."""
        return SoftDeletableQuerySet(self.model, using=self._db)

    def alive(self) -> QuerySet:
        """Return only non-deleted objects."""
        return self.get_queryset().alive()

    def dead(self) -> QuerySet:
        """Return only deleted objects."""
        return self.get_queryset().dead()


class AbstractBaseModel(Model):
    """
    Abstract base model with common timestamp fields.
    """

    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        """Meta class for AbstractBaseModel."""
        abstract = True


class AbstractSoftDeletableModel(AbstractBaseModel):
    """
    Abstract model with soft delete functionality.
    """

    deleted_at = DateTimeField(
        null=True,
        blank=True,
        verbose_name="Deleted At"
    )

    objects = SoftDeletableManager()

    class Meta:
        """Meta class for AbstractSoftDeletableModel."""
        abstract = True

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        """Soft delete the object by setting deleted_at timestamp."""
        self.deleted_at = django_timezone.now()
        self.save(update_fields=["deleted_at"])
        return (0, {})

    def hard_delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        """Permanently delete the object."""
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        """Restore soft-deleted object."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    @property
    def is_deleted(self) -> bool:
        """Check if object is soft-deleted."""
        return self.deleted_at is not None