from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path("",views.index,name="index"),
    path("read/",views.read,name="read"),
    path("reada/",views.reada,name="reada"),
    path("del/",views.delete,name="delete"),
    path("add_session/",views.add_session,name="add_session"),
    path("read_session/",views.read_session,name="read_session"),
    path("del_session/",views.del_session,name="del_session"),
]