from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homePage, name="homePage"),
    path('registerPage/',registerPage, name="registerPage"),
    path('loginPage/',loginPage, name="loginPage"),
    path('logoutPage/',logoutPage, name="logoutPage"),
    path('profilePage/',profilePage, name="profilePage"),
    path('editProfile/',editProfile, name="editProfile"),
    path('addSkill/',addSkill, name="addSkill"),
    path('addCompany/',addCompany, name="addCompany"),
    path('editCompany/',editCompany, name="editCompany"),
    path('editSkill/<int:seeker_id>',editSkill, name="editSkill"),
    path('createdJob/',createdJob, name="createdJob"),
    path('addJob/',addJob, name="addJob"),
    path('deleteJob/<int:job_id>',deleteJob, name="deleteJob"),
    path('editJob/<int:job_id>',editJob, name="editJob"),
    path('viewJob/<int:job_id>',viewJob, name="viewJob"),
    path('applyJob/<int:job_id>',applyJob, name="applyJob"),
    path('appliedJob/',appliedJob, name="appliedJob"),
    path('searchJob/',searchJob, name="searchJob"),
    path('skillMatchingPage/',skillMatchingPage, name="skillMatchingPage"),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)