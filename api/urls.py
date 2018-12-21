from django.urls import path, re_path


from .views import (
    PersonOneAPIView,
    PersonListAPIView,
    CompanyOneAPIView,
    CompanyListAPIView,
    EmployeesByCompanyIdAPIView,
    SalaryListAPIView
)


urlpatterns = [
    re_path('^company/(?P<id>\d+)$', CompanyOneAPIView.as_view(),
            name='one_company'
            ),
    path('company/', CompanyListAPIView.as_view(),
         name='company'
         ),

    re_path('^employee/(?P<id>\d+)$', PersonOneAPIView.as_view(),
            name='one_employee'
            ),

    re_path('^company/(?P<id>\d+)/employee$',
            EmployeesByCompanyIdAPIView.as_view(),
            name='employees_by_company_id'),

    path('employee/', PersonListAPIView.as_view(), name='employees'),

    re_path('^salary/', SalaryListAPIView.as_view(), name='salary'),
]
