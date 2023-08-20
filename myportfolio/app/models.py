from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    address = models.TextField("current address", max_length=200)
    text_about = models.TextField("text about", blank=True, null=True)

    github_profile_link = models.URLField("github", blank=True, null=True)
    linkedin_profile_link = models.URLField("linkedin", blank=True, null=True)
    telegram_username = models.CharField(
        "telegram username",
        blank=True,
        null=True,
        max_length=100,
    )

    # Please, adjust this data in templates/includes/about.html
    work_experience = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    # ------------------------------------------------------

    cv = models.FileField("cv", upload_to="media/user/", blank=True, null=True)
    home_image = models.ImageField(
        upload_to="user/",
    )
    about_image = models.ImageField(
        upload_to="user/",
    )

    def save(self, *args, **kwargs):
        """
        Save user to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)


class Project(models.Model):
    author = models.ForeignKey(
        User, related_name="projects", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
    )

    github_link = models.URLField()
    browse_link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = ("project")
        verbose_name_plural = ("projects")

    def __str__(self) -> str:
        return f"Project {self.name} by {self.author.get_full_name()}"


class Instrument(models.Model):
    INTERMEDIATE = "Intermediate"
    BASIC = "Basic"
    ADVANCED = "Advanced"
    LEVEL_CHOICES = (
        (BASIC, "Basic"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    FRONTEND = "Front"
    BACKEND = "Back"
    DEV_TYPE_CHOICES = (
        (FRONTEND, "Frontend"),
        (BACKEND,"Backend"),
    )

    owner = models.ForeignKey(
        User, related_name="instruments", on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name="name", max_length=50)
    level = models.CharField(
        choices=LEVEL_CHOICES,
        max_length=max([len(word) for word, _ in LEVEL_CHOICES]),
    )
    development_type = models.CharField(
        choices=DEV_TYPE_CHOICES,
        max_length=max([len(word) for word, _ in DEV_TYPE_CHOICES]),
    )

    class Meta:
        verbose_name = ("instrument")
        verbose_name_plural = ("instruments")

    def __str__(self) -> str:
        return f"Instrument {self.name}, {self.owner.get_full_name()}"


class Contact(models.Model):
    name = models.CharField(max_length=150)
    message = models.TextField()
    email = models.EmailField()

    class Meta:
        verbose_name = ("message")
        verbose_name_plural = ("messages")
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["email", "message"],
                name="unique_message",
            ),
        ]

    def __str__(self) -> str:
        return f"Message from {self.email}"
