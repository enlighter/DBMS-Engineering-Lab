from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import URLValidator #for dealing with urls
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_marks(value):
    if (value < 0) or (value > 100) :
        raise ValidationError(
            _('%(value) is not a valid mark'),
            params={'value': value},
        )


def validate_status(value):
    if value not in ('audit','attempted','completed'):
        raise ValidationError(
            _('%(value) is not a valid status'),
            params={'value': value},
        )


class MyUserManager(BaseUserManager):
    def _create_user(self, email, firstname, password=None, **other_fields):
        """
        Creates and saves a User with the given email, firstname and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        if not firstname:
            raise ValueError('Users must have a first name')

        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname,
                          last_login=now,
                          date_joined=now, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, firstname, **other_fields):
        return self._create_user(email=email, firstname=firstname, password=password,
                                 **other_fields)

    def create_superuser(self, email, password, firstname, **other_fields):
        return self._create_user(email=email, firstname=firstname, password=password,
                                 **other_fields)


class MyUser(AbstractBaseUser):
    '''MyUser is a custom User model for our website
    '''
    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    REQUIRED_FIELDS = ['firstname']

    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30, null=True, blank=True)
    website = models.TextField(validators=[URLValidator()], null=True, blank=True)
    email = models.EmailField(max_length=69, unique=True, primary_key=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def get_full_name(self):
        return self.firstname+" "+self.email
    def get_short_name(self):
        return self.firstname
    def __str__(self):
        return self.firstname+" "+self.email

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return self.is_active


class Course(models.Model):
    course_name = models.CharField(max_length=42)
    courseID = models.AutoField(unique=True, primary_key=True)
    about = models.CharField(max_length=999)
    provided_by_institute = models.CharField(max_length=99, default="freelance", blank=True)
    domain = models.CharField(max_length=33)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.course_name


class Learners(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    nick = models.CharField(max_length=12, unique=True)
    #Many to Many relationship with course
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Accomplishment(models.Model):
    status = models.CharField(max_length=9, default='audit', validators=[validate_status], blank=True)
    performance = models.FloatField(null=True, blank=True, default=0)
    #Many to one relationship with course content
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #one to one relationship with a learner
    student = models.OneToOneField(Learners, on_delete=models.CASCADE, unique=True, primary_key=True)


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    instructorID = models.AutoField(unique=True, primary_key=True)
    #Many to many relationship with course
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class CourseContent(models.Model):
    #Many to one relationship with course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    partID = models.AutoField(unique=True, primary_key=True)
    #url path to the content
    content_location = models.TextField(validators=[URLValidator()])
    content_name = models.CharField(max_length=30)
    content_type = models.CharField(max_length=18)
    has_evaluation = models.BooleanField()

    def __str__(self):
        return self.content_type+" : "+self.content_name


class Performance(models.Model):
    score = models.IntegerField(validators=[validate_marks], default=0)
    #Many to one relationship with course content
    course_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    #one to one relationship wwith a learner
    student = models.OneToOneField(Learners, on_delete=models.CASCADE, unique=True, primary_key=True)
