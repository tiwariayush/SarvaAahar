from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
import json

#TODO: Logout views on each page
# Create a header part and include in all pages

login_url = '/middaymeal/'

from models import *
from forms import *

@login_required(login_url=login_url)
def edit_child(request, child_id=None):

    if child_id:

        try:
            child = Child.objects.get(pk=child_id)
            child_data = {'name': child.name,
                          'date_of_birth': child.date_of_birth,
                          'aanganwadi': child.aanganwadi}
            childform = ChildEntryForm(initial=child_data)

            child_condition = ChildConditions.objects.filter(child=child)[0]
            child_condition_data  = {'weight': child_condition.weight,
                                    'height': child_condition.height,
                                    'age': child_condition.age,
                                    'body_mass_index': child_condition.body_mass_index,
                                    'date_of_entry': child_condition.date_of_entry}
            childconditionform = ChildConditionForm(initial=child_condition_data)

            child = Child.objects.get(pk=child_id)

        except ObjectDoesNotExist:
            messages.error(request, 'This child entry is not present')
    else:
        childform = ChildEntryForm()
        childconditionform = ChildConditionForm()

    if request.POST:

        childform = ChildEntryForm(request.POST)
        childconditionform = ChildConditionForm(request.POST)

        if childform.is_valid() and childconditionform.is_valid():
            if not child:
                child = childform.save()
            b = childconditionform.save(commit=False)
            b.child = child
            b.save()
            aanganwadi_name = request.POST['aanganwadi']
            return HttpResponseRedirect('/middaymeal/children/%s' %aanganwadi_name)

    return render_to_response('middaymeal/child_entry.html',{
        'childform': childform,
        'childconditionform': childconditionform,
}, context_instance=RequestContext(request))

def create_user(request):

    if request.POST:

        form = SignUpForm(request.POST)

        if form.is_valid():

            user_profile = form.save(commit=False)
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=name, password=password)
            user.save()

#            if not created:
#                messages.error(request, 'User already exists with same name ')

            category_form_data = {'super': 'super',
                             'district': form.cleaned_data['district'],
                             'block': form.cleaned_data['block'],
                             'panchayat': form.cleaned_data['panchayat'],
                             'village': form.cleaned_data['village'],
                             'aanganwadi': form.cleaned_data['aanganwadi']
                            }

            user_profile.category_data = json.dumps(category_form_data)
            user_profile.user = user
            user_profile.save()
            messages.success(request, 'Signup successful')
            return HttpResponseRedirect('/middaymeal/')

    else:
        form = SignUpForm()

    return render_to_response('middaymeal/signup.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))

def login_user(request):

    form = LoginForm(request.POST or None)

    if form.is_valid():

        username = form.cleaned_data['name']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)

            if user.is_staff:
                return HttpResponseRedirect('/middaymeal/districts')

            user_profile = UserProfile.objects.filter(user=user)[0]
            category = user_profile.category
            category_data = json.loads(user_profile.category_data)
            category_name = category_data[str(category)]
            return HttpResponseRedirect('/middaymeal/details/%s/%s' %(category, category_name))

        return HttpResponse('<html><head><body>Invaild username or password</body></head></html>')

    return render_to_response('middaymeal/login.html',
                             {'form': form},
                             context_instance=RequestContext(request))

@login_required(login_url=login_url)
def view_category_details(request, category=None, category_name=None):

        if category=='super':            
            return HttpResponseRedirect('/middaymeal/districts')
        if category=='district':
            return HttpResponseRedirect('/middaymeal/blocks/%s' %category_name)
        if category=='block':
            return HttpResponseRedirect('/middaymeal/panchayats/%s' %category_name)
        if category=='panchayat':
            return HttpResponseRedirect('/middaymeal/villages/%s' %category_name)
        if category=='village':
            return HttpResponseRedirect('/middaymeal/aanganwadis/%s' %category_name)
        if category=='aanganwadi':
            return HttpResponseRedirect('/middaymeal/children/%s' %category_name)

        return HttpResponse('<html><head><body>No category defined for user</body></head></html>')

@login_required(login_url=login_url)
def view_districts(request):

    districts = District.objects.filter(state='Uttarakhand')
    return render_to_response('middaymeal/districts.html',
                             {'districts': districts},
                             context_instance=RequestContext(request))

@login_required(login_url=login_url)
def view_blocks(request, district_name=None):

    if district_name:

        district = District.objects.get(pk=district_name)
        blocks = Block.objects.filter(district=district)
        return render_to_response('middaymeal/blocks.html',
                                 {'blocks': blocks},
                                 context_instance=RequestContext(request))

    return HttpResponse('<html><head><body>No blocks in this district</body></head></html>')

@login_required(login_url=login_url)
def view_panchayats(request, block_name=None):

    if block_name:

        block = Block.objects.get(pk=block_name)
        panchayats = Panchayat.objects.filter(block=block)
        return render_to_response('middaymeal/panchayats.html',
                                 {'panchayats': panchayats},
                                 context_instance=RequestContext(request))

    return HttpResponse('<html><head><body>No panchayat in this block</body></head></html>')

@login_required(login_url=login_url)
def view_villages(request, panchayat_name=None):

    if panchayat_name:

        panchayat = Panchayat.objects.get(pk=panchayat_name)
        villages = Village.objects.filter(panchayat=panchayat)
        return render_to_response('middaymeal/villages.html', 
                                 {'villages': villages}, 
                                 context_instance=RequestContext(request))

    return HttpResponse('<html><head><body>No villages in this panchayat</body></head></html>')

@login_required(login_url=login_url)
def view_aanganwadis(request, village_name=None):

    if village_name:

        village = Village.objects.get(pk=village_name)
        aanganwadis = Aanganwadi.objects.filter(village=village)
        return render_to_response('middaymeal/aanganwadis.html', 
                                 {'aanganwadis': aanganwadis}, 
                                 context_instance=RequestContext(request))

    return HttpResponse('<html><head><body>No panchayat in this block</body></head></html>')

@login_required(login_url=login_url)
def view_children(request, aanganwadi_name=None):

        if aanganwadi_name:

            try:
                aanganwadi = Aanganwadi.objects.filter(pk=aanganwadi_name)[0]
            except IndexError:
                return HttpResponse('<html><head><body>No such aanganwadi exists</body></head></html>')

            try:
                children = Child.objects.filter(aanganwadi=aanganwadi)
                children_info = []

                for child in children:
                    child_details = ChildConditions.objects.filter(child=child)
                    child_info = {}
                    child_info['child']={
                                         'id': child.pk,
                                         'name': child.name,
                                         'dob': child.date_of_birth
                                        }
                    child_info['conditions']=[]

                    for condition in child_details:
                        cond = {
                                'weight': condition.weight,
                                'height': condition.height,
                                'age': condition.age,
                                'bmi': condition.body_mass_index,
                                'doe': condition.date_of_entry
                                }
                        child_info['conditions'].append(cond)

                    children_info.append(child_info)

            except ObjectDoesNotExist:
                return HttpResponse('<html><head><body>No children in this aanganwadi</body></head></html>')

            return render_to_response('middaymeal/child_details.html', 
                                     {'children_info': children_info}, 
                                     context_instance=RequestContext(request))

@login_required(login_url=login_url)
def view_child_details(request, child_id=None):

    if child_id:
        child = Child.objects.get(pk=child_id)
        child_details = ChildConditions.objects.filter(child=child)

        child_info = {}
        child_info['child']={
                             'id': child.pk,
                             'name': child.name,
                             'dob': child.date_of_birth
                            }
        child_info['conditions']=[]

        for condition in child_details:
            cond = {
                    'weight': condition.weight,
                    'height': condition.height,
                    'age': condition.age,
                    'bmi': condition.body_mass_index,
                    'doe': condition.date_of_entry
                    }
            child_info['conditions'].append(cond)

        return render_to_response('middaymeal/child_track.html',
                                  {'child_info': child_info},
                                  context_instance=RequestContext(request))

@login_required(login_url=login_url)
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/middaymeal/')
