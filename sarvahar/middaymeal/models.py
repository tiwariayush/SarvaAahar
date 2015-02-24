from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import timedelta, datetime

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

    def __unicode__(self):
       return str(self.name)

class Block(models.Model):

    name = models.CharField(max_length=100)
    district = models.ForeignKey(District)

    def __unicode__(self):
       return str(self.name)

 
class Panchayat(models.Model):
    '''
        Panchayat data and the block it lies
        in
    '''
    name = models.CharField(max_length=100)
    block = models.ForeignKey(Block)

    def __unicode__(self):
       return str(self.name)

class Village(models.Model):
    '''
        Stores info about specific villages
        and F.K. to panchayat it lies in 
    '''
    name = models.CharField(max_length=100)
    panchayat = models.ForeignKey(Panchayat)

    def __unicode__(self):
       return str(self.name)

class Aanganwadi(models.Model):
    '''
        Data on unique aaganwadi and the 
        village it lies in 
    '''
    name = models.CharField(max_length=100)
    village = models.ForeignKey(Village)

    def __unicode__(self):
       return str(self.name)

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
        self.date_of_entry = datetime.now()
        age_diff = self.date_of_entry.date()-self.child.date_of_birth
        self.age = str(age_diff.days/float(365))
        super(ChildConditions, self).save(**kwargs)
