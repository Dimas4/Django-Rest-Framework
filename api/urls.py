from django.urls import path, re_path


from .views import PersonOneAPIView, PersonListAPIView, CompanyOneAPIView, CompanyListAPIView


urlpatterns = [
    re_path('^company/(?P<id>\d+)', CompanyOneAPIView.as_view(), name='one_company'),
    path('company/', CompanyListAPIView.as_view(), name='company'),

    re_path('^employee/(?P<id>\d+)', PersonOneAPIView.as_view(), name='one_employee'),
    path('employee/', PersonListAPIView.as_view(), name='employees')
]
