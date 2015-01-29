from django.db import models
from datetime import timedelta

class Child(models.Model):
    '''
        A child model to store information about unique child
    '''

    name = models.CharField(max_length=250)
    date_of_birth = models.DateField()

    def __unicode__(self):
        return self.name

class ChildConditions(models.Model):
    '''
        Stores conditions and its entry date, has a foreign
        key relation to Child model, means one child can have 
        multiple conditions which can be sorted by date_of_entry
        to find if the condition is detoriating or getting better.
    '''
    
    weight = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    body_mass_index = models.CharField(max_length=50)
    date_of_entry = models.DateTimeField(auto_now_add=True)
    child = models.ForeignKey(Child)

    def __unicode__(self):
        return  ('Child name:' %s, 
                 'BMI:' %s, 
                 'Date of entry:'%s)
                %(self.child, 
                  self.body_mass_index, 
                  self.date_of_entry)

    def save(self, **kwargs):
        '''
            Overriding save to find actual age of the child
            during time of entry
        '''

        self.age = timedelta(self.date_of_entry.date-self.child.date_of_birth)
        super(ChildConditions, self).save(**kwargs)

class Village(models.Model):
    '''
        Stores info about specific villages
    '''
    pass
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District)

class District(models.Model):

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class Aaganbadi(models.Model):

    name = models.CharField(max_length=100)
    village = models.ForeignKey(max_length=100) 
