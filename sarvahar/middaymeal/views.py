from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from models import *
from forms import *

def EditChild(request, child_id=None):
    if child_id:
        try:
            child = Child.objects.get(pk=child_id)
            child_data = {'name': child.name,
                          'date_of_birth': child.date_of_birth,
                          'aanganwadi': child.aanganwadi}
            childform = ChildEntryForm(initial=child_data)

            child_condition = ChildConditions.objects.get(child=child)
            child_condition_data  = {'weight': child_condition.weight,
                                    'height': child_condition.height,
                                    'age': child_condition.age,
                                    'body_mass_index': child_condition.body_mass_index,
                                    'date_of_entry': child_condition.date_of_entry}
            childconditionform = ChildConditionForm(initial=child_condition_data)
        except ObjectDoesNotExist:
            messages.error(request, 'This child entry is not present')
    else:
        childform = ChildEntryForm()
        childconditionform = ChildConditionForm()

    if request.POST:
        childform = ChildEntryForm(request.POST)
        childconditionform = ChildConditionForm(request.POST)
        if childform.is_valid() and childconditionform.is_valid():
            a = childform.save()
            b = childconditionform.save(commit=False)
            b.child = a
            b.save()
            return HttpResponseRedirect(reverse('middaymeal.EditChild'))

    return render_to_response('middaymeal/child.html',{
        'childform': childform,
        'childconditionform': childconditionform,
}, context_instance=RequestContext(request))

def AddUser(request):
    if request.POST:
        pass
    else:
        pass
               
'''
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
'''

def create_user(request):

    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user, created = User.objects.get_or_create(username=name, password=password)
            user.save()
            if not created:
                messages.error(request, 'User already exists with same name ')
            user_profile.user = user
            user_profile.save()
            return HttpResponse('<html><body>Success</body></html>')
    else:
        form = SignUpForm()
    return render_to_response('middaymeal/signup.html', {'form': form}, context_instance=RequestContext(request))
        

def login_user(request):

    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
        user_profile = UserProfile.objects.filter(user=user)
        category = user_profile.category

def category_view(request, category, cat_id):
        if category=='super':
            children = Child.objects.all()
            children_data = []
            for child in children_data:
                child_condition = ChildConditions.objects.filter(child=child)
                child_info = {'child': child,
                              'child_condition': child_condition }
                children_data.append(child_info)
            return render_to_response('middaymeal/children.html', {'children_info'=children_info}, context_instance=RequestContext(request))
