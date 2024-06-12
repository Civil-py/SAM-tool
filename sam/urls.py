from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
path('software/', views.software, name="software"),
path('insights/', views.insights, name="insights"),
path('software/<str:software_id>', views.software_view, name="software_view"),
path('staff/', views.staff, name="staff"),
path('add-staff/', views.add_staff, name="add_staff"),


path('add-user/<str:software_id>', views.add_users, name="add_user"),
path('user-view/<str:software_id>', views.users_view, name="users_view"),
path('staff-view/<str:employee_id>/', views.staff_view, name="staff_view"),
path('allocated-user-view/<str:software_id>/<str:employee_id>', views.user_allocated_view, name="allocated_user_view"),
path('delete-user/<str:software_id>/<int:id>', views.delete_user, name="delete_user"),

path('delete-staff/<str:employee_id>/', views.delete_staff, name="delete_staff"),
path('edit-staff/<str:employee_id>/', views.edit_staff, name="edit_staff"),

path('edit/<str:software_id>/', views.edit_software, name="edit_software"),
path('delete/<str:software_id>/', views.delete_software, name="delete_software"),
path('add-software', views.add_software, name='addsoftware')

,

path('contract-view/<str:software_id>/<int:id>', views.contract_view, name="contract_view"),
path('contract-edit/<str:software_id>/<int:id>', views.edit_contract, name="edit_contract"),
path('delete-contract/<str:software_id>/<int:id>', views.delete_contract, name="delete_contract"),
path('<str:software_id>/add-contract', views.add_contract, name='add_contract')
]