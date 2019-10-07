from django.db import models
from django.contrib.auth.models import User
from apps.catalog.models import Item
from django.utils.translation import ugettext_lazy as _
from django.core import validators
import re
from django.utils import timezone


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='social')
    photo = models.CharField(max_length = 255,blank = True)
    phone = models.CharField(max_length = 12,blank = True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    country = models.CharField (max_length = 75,blank = True)
    city = models.CharField (max_length = 75,blank = True)

    def get_email(self):
        return self.user.email
    def get_first_name(self):
        return self.user.first_name
    def get_last_name(self):
        return self.user.last_name
    email = property(get_email)
    first_name = property(get_first_name)
    last_name = property(get_last_name)

    def __unicode__(self):
        return self.user.email


class History(models.Model):
    user = models.ForeignKey(User, related_name='history')
    item = models.ForeignKey(Item, related_name='history')

    def __unicode__(self):
        return self.item.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlist')
    item = models.ForeignKey(Item, related_name='wishlist')
    uniq = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.item.name

'''
class SocialUser(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_admin = models.BooleanField(default=False)
    photo = models.CharField(max_length = 255,blank = True)
    phone = models.CharField(max_length = 10,blank = True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # objects = UserManager()
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False
        app_label="dachdoard"

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
    def get_group_permissions(self, obj=None):
        return set()
    def get_all_permissions(self, obj=None):
        return set()
    def has_perm(self, perm, obj=None):
        return False
    def has_perms(self, perm_list, obj=None):
        return False
    def has_module_perms(self, app_label):
        return False
    @property
    def is_staff(self):
        return self.is_admin
    def __unicode__(self):
        return self.username
'''
# class SocialUser(AbstractUser):
#     photo = models.TextField(blank = True)
#     phone = models.CharField(max_length = 10,blank = True)
#     class Meta:
#         app_label = 'auth'

'''
class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)
class SocialUser(models.Model):
    username = models.CharField(max_length=30)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    photo = models.TextField(blank = True)
    phone = models.CharField(max_length = 10,blank = True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    objects = CustomUserManager()

    def __unicode__(self):
        return self.username
    
    def is_authenticated(self):
        return True    
    
'''


'''
class AuthUserManager(BaseUserManager):
def create_user(self, username, email, password=None):
    if not email:
        raise ValueError('User must have email')
    if not username:
        raise ValueError('User must have username')
    user = self.model(username=username, email=self.normalize_email(email))
    user.is_active = True
    user.set_password(password)
    user.save(using=self._db)
    return user
 
def create_superuser(self, username, email, password):
    user = self.create_user(username=username, email=email, password=password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
 '''

