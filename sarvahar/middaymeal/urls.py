from django.conf.urls import url, patterns, include
from middaymeal import views

urlpatterns = patterns('',
    url(r'^$',                                              views.login_user,           name="login_user"),
    url(r'signup',                                          views.create_user,          name="create_user"),
    url(r'edit/(?P<child_id>\d+)',                          views.edit_child,           name="edit_child"),
    url(r'details/(?P<category>\w+)/(?P<category_name>\w+)',views.view_category_details,name="view_category_details"),
    url(r'districts/',                                      views.view_districts,       name="view_districts"),
    url(r'blocks/(?P<district_name>\w+)',                   views.view_blocks,          name="view_blocks"),
    url(r'panchayats/(?P<block_name>\w+)',                  views.view_panchayats,      name="view_panchayats"),
    url(r'villages/(?P<panchayat_name>\w+)',                views.view_villages,        name="view_villages"),
    url(r'aanganwadis/(?P<village_name>\w+)',               views.view_aanganwadis,     name="view_aanaganwadis"),
    url(r'children/(?P<aanganwadi_name>\w+)',               views.view_children,        name="view_children"),
)
