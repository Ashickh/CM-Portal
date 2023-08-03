from django.urls import path
from .views import * 
urlpatterns = [
    path('request-space/',SpaceRequestView.as_view()),
    path('contract/',ContractView.as_view()),
    path('contract-details/<int:id>/',ContractDetailsView.as_view()),
    path('request-space/status-change/<int:id>/',SpaceRequestDetail.as_view()),
    # path('contract-pdf/',ContractPdfGeneration.as_view(), name='contract'),
    path('upload_contract_documents/',UploadContractDocuments.as_view()),
]