from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
import json

#TODO: Use child details model as history(to show , show the newest data entry)

from models import *
from forms import *

def edit_child(request, child_id=None):

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

            return HttpResponse('<html><body>Success</body></html>')

    else:
        form = SignUpForm()

    return render_to_response('middaymeal/signup.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
        

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
        category_data = json.loads(user_profile.category_data)
        category_name = category_data[str(category)]

        return HttpResponseRedirect('/middaymeal/details/%s/%s' %(category, category_name))

def view_category_details(request, category=None, category_name=None):

        if category=='super':

            children = Child.objects.all()
            children_data = []

            for child in children_data:
                child_condition = ChildConditions.objects.filter(child=child)
                child_info = {'child': child,
                              'child_condition': child_condition }
                children_data.append(child_info)

            return render_to_response('middaymeal/children.html', 
                                      {'children_info'=children_info}, 
                                      context_instance=RequestContext(request))

def view_aanganwadi_children(request, aanganwadi_name=None):

        if not aanganwadi_name:

            aanganwadi = Aanganwadi.objetcs.filter(name=str(aanganwadi_name))[0]
            children = Child.objects.filter(aanganwadi=aanganwadi)
            children_info = []

            for child in children:
                child_details = ChildConditions.objetcs.filter(child=child)
                child_info = {}
                child_info['child']={
                                     'name': child.name,
                                     'dob': child.date_of_birth
                                    }
                child_info['conditions']=[]

                for condition in child_details:
                    cond = {
                            'weight': condiion.weight,
                            'height': condition.height,
                            'age': condition.age,
                            'bmi': condition.body_mass_index,
                            'doe': condition.date_of_entry
                            }
                    child_info['conditions'].append(cond)

                children_info.append(child_info)

            return render_to_response('child_details.html', {'children_info': children_info})
