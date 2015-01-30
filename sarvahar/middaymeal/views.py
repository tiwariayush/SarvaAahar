from django.shortcuts import render

from models import .
# Create your views here.

def add_child(request):

  name = request.POST('name')
  DOB = request.POST('DOB')
  aanganwadi = request.POST('aanganwadi')
  
  new_child = Child(name = name , date_of_birth = DOB , aanganwadi = aanganwadi)
  new_child.save()

def get_locations(aanganwadi):

  village = Village.objects.get(id = aanganwadi.village)
  panchayat = Panchayat.objects.get(id = village.panchayat)
  block = Block.objects.get(id = panchayat.block)
  district = District.objects.get(id = block.district)

  locations = {'aanganwadi':aanganwadi,
               'village':village,
               'panchayat':panchayat,
               'block':block,
               'district':district }

  return locations
  
