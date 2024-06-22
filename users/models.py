from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role='staff', password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name=None,last_name=None, email=None, password=None, phone=None, role=None, **kwargs
    ):
        """
        This is the method that creates superusers in the database.
        """
        admin = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role="admin",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        return admin
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('staff', 'staff'),
        ('lead', 'lead'),
        ('admin', 'admin'),
        ('management', 'management'),
        ('tech_lead', 'tech_lead'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='staff')
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


class Profile(models.Model):
    #create profile with signals
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
    profile_picture = models.ImageField(upload_to="media/documents/profile/", null=True, blank=True)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.user_profile.save()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
