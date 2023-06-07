from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            #username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('氏名'), max_length=50, blank=False,unique=False)
    kana_characters = models.CharField(_('カタカナ'), max_length=50, blank=True)
    nickname = models.CharField(_('ニックネーム'), max_length=50, blank=False)
    email = models.EmailField(_('email address'), unique=True)

    school_classification = models.CharField(_('学校区分'), max_length=10)
    school_name = models.CharField(_('学校名'), max_length=15)
    Department = models.CharField(_('学科'), max_length=10)
    student_number = models.CharField(_('学籍番号'), max_length=10)
    grade = models.CharField(_('学年'), max_length=1, blank=True)
    
    #icon = models.ImageField(upload_to="media",blank=True, null=True)
    introduction = models.CharField(max_length=75, blank=True, null=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    objects = UserManager()

    #EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)