from django.db import models
from datetime import timedelta

'''
   Models are created in decreasing order of their 
   number of students.Each model points(foreign key)
   to its immediate super Model
'''

class District(models.Model):

  name = models.CharField(max_length=100 , unique = True)

class Block(models.Model):

  name = models.CharField(max_length=100)
  district = models.ForeignKey(District)
  
class Panchayat(models.Model):

  name = models.CharField(max_length=100)
  block = models.ForeignKey(Block)

class Village(models.Model):
  '''
        Stores info about specific villages
  '''
  name = models.CharField(max_length=100)
  panchayat = models.ForeignKey(Panchayat)


class Aanganwadi(models.Model):

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

        self.age = timedelta(self.date_of_entry.date-self.child.date_of_birth)
        super(ChildConditions, self).save(**kwargs)

