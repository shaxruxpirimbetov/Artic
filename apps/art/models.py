from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
User = get_user_model()

class Art(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="art_user")
    title = models.CharField(
        max_length=124,
        validators=[MinLengthValidator(3), MaxLengthValidator(124)]
    )
    description = models.TextField(
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(500),
        ]
    )
    image = models.ImageField(upload_to="arts/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Art {self.title} by {self.user.first_name if self.user.first_name else '@' + self.user.username}"

    class Meta:
        verbose_name_plural = "Arts"
        ordering = ["-created_at"]