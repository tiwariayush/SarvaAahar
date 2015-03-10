from django.contrib import admin
from django.db.models import get_models, get_app
from .models import ChildConditions

for model in get_models(get_app('middaymeal')):
    if model==ChildConditions:
        continue
    admin.site.register(model)

class ChildConditionsAdmin(admin.ModelAdmin):
    exclude = ('body_mass_index', 'age',)

admin.site.register(ChildConditions, ChildConditionsAdmin)
