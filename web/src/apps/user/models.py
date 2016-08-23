import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser)
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from utils.utils.utils import get_extension, get_email_name
from .managers import UserManager


logger = logging.getLogger(__name__)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    """
    # Relations

    # Attributes
    email = models.EmailField(verbose_name='email',
                              max_length=255,
                              unique=True,
                              help_text='Required. 255 characters or fewer. Letters, digits, and @/./+/-/_ only.',
                              validators=[validators.EmailValidator(), ],
                              error_messages={'unique': "A user with that email address already exists.", }, )

    picture = models.ImageField(verbose_name='profile picture',
                                max_length=255)

    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)

    is_staff = models.BooleanField('staff status',
                                   default=False,
                                   help_text='Designates whether the user can log into this admin site.', )
    is_active = models.BooleanField('active',
                                    default=True,
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect instead of deleting accounts.', )

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    # Manager
    objects = UserManager()

    # Functions
    def get_picture_pretty_name(self):
        return "{}{}".format(slugify(get_email_name(self.email)), get_extension(self.picture))

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_email(self):
        """
        Returns the email for the user.
        """
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # Meta
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True
        db_table = 'auth_user'


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Username, password and email are required. Other fields are optional.
    """
    # class Meta(AbstractUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'
