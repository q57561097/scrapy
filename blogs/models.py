from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from mysite import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16, default='', blank=True)
    sex = models.IntegerField(default=0)
    phone = models.CharField(max_length=16, default='', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserProfile'

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
            except UserProfile.DoesNotExist:
                pass

        super(UserProfile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)