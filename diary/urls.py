from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('create/', views.create_entry, name='create_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('search/', views.search_entries, name='search_entries'),
    path('export/<int:entry_id>/pdf/', views.export_entry_pdf, name='export_entry_pdf'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]