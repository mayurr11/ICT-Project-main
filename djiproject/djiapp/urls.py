from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query.html/', views.query, name='query'),
    path('submit_enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('get_today_flights/', views.get_today_flights, name='get_today_flights'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('get_query/', views.get_query, name='get_query'),

    path('send_reply_email/', views.send_reply_email , name='send_reply_email'),
    # update Query.status = True... as in true resolved
    path('dismiss_message/', views.dismiss_message, name='dismiss_message'),
    # i'm not sure what the uuid:pk does Hiru????
    #path('reply_inquiry/<uuid:pk>/', reply_inquiry, name='reply_inquiry'),

]