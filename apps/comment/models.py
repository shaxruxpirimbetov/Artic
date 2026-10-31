from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from apps.art.models import Art
User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    art = models.ForeignKey(Art, on_delete=models.CASCADE, related_name='comment_art')
    content = models.TextField(
        validators=[MinLengthValidator(5)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment to Art({self.art}) by {self.user.first_name if self.user.first_name else f'@{self.user.username}'}"

    class Meta:
        verbose_name_plural = "Comments"
        ordering = ['-created_at']