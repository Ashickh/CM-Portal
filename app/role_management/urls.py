from django.urls import path
from app.feature import views

urlpatterns = [
  
  path('feature/',views.FeatureView.as_view()),
  path('feature/<int:id>/',views.FeatureDetailView.as_view()),
  path('role/',views.RoleView.as_view()),
  path('role/<int:id>/',views.RoleDetailView.as_view()),
  path('role_feature/',views.RoleFeatureView.as_view()),
  path('role_feature/<int:pk>/',views.RoleFeatureDetailView.as_view()),
  path('users/',views.UserView.as_view()),
  path('users/<int:id>',views.UserDetailView.as_view()),
  path('userrole/',views.UserRoleView.as_view()),
  path('emailtoken/',views.EmailTokenView.as_view()),
  path('passwordresetmail/',views.PasswordResetEmailView.as_view()),
  path('reset_password/',views.reset_passwordView.as_view()),


]


