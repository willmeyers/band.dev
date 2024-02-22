from django.db import models


class Shop(models.Model):
    user = models.OneToOneField("authusers.AuthUser", on_delete=models.CASCADE, related_name="shop")
