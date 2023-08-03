from django.contrib import admin
from django.urls import path,include
from app.invoice_management import views


urlpatterns = [

    path('utility/',views.UtilityView.as_view()),
    path('utilityedit/<int:id>',views.UtilityEditView.as_view()),
    path('utilityreading/approval/<int:id>',views.UtilityReading_ApprovingView.as_view()),
    
    path('grievances/',views.GrievancesView.as_view()),
    # path('grievances/assigning/<int:id>',views.GrievancesAssigningView.as_view()),
    path('grievances/change_status/<int:id>',views.GrievancesStatusUpdateView.as_view()),
    path('grievances/<int:id>',views.GrievancesDetailView.as_view()),

    path('bill/',views.BillFilterView.as_view()),
    path('invoice/',views.InvoiceFilterView.as_view()),

    path('notification/',views.NotificationContent.as_view()),
    
    path('alertmessages/', views.SendAlertMessagesView.as_view()),

    path("security_payment/", views.SecurityPaymentView.as_view(), name="security_payment"),
    path('security_payment/paymenthandler/', views.SecurityPaymentCallbackView.as_view(), name='paymenthandler'),
]