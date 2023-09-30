from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('confirm', views.confirm, name='confirm'),
    path('book-appointment', views.bookAppointment, name='book-appointment'),
    path('appointment-details', views.appointmentDetails,
         name='appointment-details'),
    path('blog', views.blog, name='blog'),
    path('blog/<str:slug>', views.postDetail, name='post-details'),
    path('drafts', views.drafts, name='drafts'),
    path('my-posts', views.myPosts, name='my-posts'),
    path('create-post', views.createPost, name='create-post'),
    path('edit-post/<str:slug>', views.editPost, name='edit-post'),
    path('delete-post/<str:slug>',
         views.deletePost, name='delete-post'),

    path('doctor-signin', views.doctorSignin, name='doctor-signin'),
    path('doctor-signup', views.doctorSignup, name='doctor-signup'),
    path('doctor-dashboard', views.doctorDashboard, name='doctor-dashboard'),

    path('patient-signin', views.patientSignin, name='patient-signin'),
    path('patient-signup', views.patientSignup, name='patient-signup'),
    path('patient-dashboard', views.patientDashboard, name='patient-dashboard'),

    path('signout', views.signout, name='signout'),
]
