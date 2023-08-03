from django.contrib import admin
from django.urls import path,include
from app.user_authentication import views
from .views import ChangePasswordView
from .views import UserLoginView
from .views import ResetPasswordView,PasswordResetEmailView,EmailTokenView



urlpatterns = [
    path('customer/register',views.CustomerRegistrationView.as_view()),
    path('user/changepassword', ChangePasswordView.as_view()),
    # path('user/<int:id>',views.UserDetailView.as_view()),
    path('login', UserLoginView.as_view()),
    path('user/createtoken', EmailTokenView.as_view()),
    path('sendpasswordresetemail', PasswordResetEmailView.as_view()),
    path('verifyemailtoken', views.VerifyEmailTokenView.as_view()),
    path('resetpassword', ResetPasswordView.as_view()),

    path('role/',views.RoleView.as_view()),
    path('roleswithoutadmin/',views.RoleListWithoutAdminView.as_view()),
    path('role/<int:id>/',views.RoleDetailView.as_view()),
    path('rolefeatures/<int:role_id>/',views.RoleFeaturesView.as_view()),
    path('sidebar/<int:role_id>/',views.SideBarView.as_view()),

    path('register/',views.UserView.as_view()),
    path('<int:id>',views.UserDetailView.as_view()),

    path('customer/detail/<int:id>',views.CustomerDetailView.as_view()),
    path('customerlist',views.CustomerListView.as_view()),
    

]
