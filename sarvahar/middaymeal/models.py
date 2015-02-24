from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import timedelta

'''
   Models are created in decreasing order of their 
   number of students.Each model points(foreign key)
   to its immediate super Model
'''

USER_CATEGORY = (
        ('super', 'super'),
        ('district', 'district'),
        ('block', 'block'),
        ('panchayat', 'panchayat'),
        ('village', 'village'),
        ('aaganwadi', 'aaganwadi'),
)


class UserProfile(models.Model):
    '''
        User profile for login
    '''
    user = models.OneToOneField(User)
    category = models.CharField(max_length=100, choices=USER_CATEGORY)

    def __unicode__(self):
        return str(self.user.username)

class District(models.Model):
    '''
        Name of district in specific state
    '''
    name = models.CharField(max_length=100 , unique = True)
    state = models.CharField(max_length=100)

class Block(models.Model):

    name = models.CharField(max_length=100)
    district = models.ForeignKey(District)
  
class Panchayat(models.Model):
    '''
        Panchayat data and the block it lies
        in
    '''
    name = models.CharField(max_length=100)
    block = models.ForeignKey(Block)

class Village(models.Model):
    '''
        Stores info about specific villages
        and F.K. to panchayat it lies in 
    '''
    name = models.CharField(max_length=100)
    panchayat = models.ForeignKey(Panchayat)

class Aanganwadi(models.Model):
    '''
        Data on unique aaganwadi and the 
        village it lies in 
    '''
    name = models.CharField(max_length=100)
    village = models.ForeignKey(Village)

class Child(models.Model):
    '''
        A child model to store information about unique child
        and the aanganwadi he/she belongs to
    '''

    name = models.CharField(max_length=250)
    date_of_birth = models.DateField()
    aanganwadi = models.ForeignKey(Aanganwadi)
    
    def __unicode__(self):
        return self.name

class ChildConditions(models.Model):
    '''
        Stores conditions and its entry date, has a foreign
        key relation to Child model, means one child can have 
        multiple conditions which can be sorted by date_of_entry
        to find if the condition is detoriating or getting better.
    '''
    
    child = models.ForeignKey(Child)
    weight = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    body_mass_index = models.CharField(max_length=50)
    date_of_entry = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):

        return self.body_mass_index
        '''return  ('Child name:' %s, 
                     'BMI:' %s, 
                     'Date of entry:'%s),
                     %(self.child, 
                    self.body_mass_index, 
                    self.date_of_entry)'''

    def save(self, **kwargs):
        '''
            Overriding save to find actual age of the child
            during time of entry
        '''
        try:
            self.body_mass_index = self.weight/pow(self.height, 2)
        except Exception as e:
            pass
        self.age = timedelta(self.date_of_entry.date-self.child.date_of_birth)
        super(ChildConditions, self).save(**kwargs)

"""
class MyUserManager(BaseUserManager):
    '''
        Credits: http://stackoverflow.com/a/12648124/2080890
    '''
    def create_user(self, email, date_of_birth, password=None):
        '''
        Creates and saves a User with the given email, date of
        birth and password.
        '''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, password):
        '''
        Creates and saves a superuser with the given email, date of
        birth and password.
        '''
        u = self.create_user(username,
                        password=password,
                        date_of_birth=date_of_birth
                    )
        u.is_admin = True
        u.save(using=self._db)
        return u

class UserProfile(AbstractBaseUser):
    email = models.CharField(
                        verbose_name='username',
                        max_length=255,
                        unique=True,
                    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    category = models.CharField(max_length=100,choices=USER_CATEGORY )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
"""

