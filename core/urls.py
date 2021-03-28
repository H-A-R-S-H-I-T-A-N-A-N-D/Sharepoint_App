from django.urls import path
from .views import SignUpView, ProfileView, users, documents, upload, download, delete, share
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('users', users, name='users'),
    path('documents', documents, name='documents'),
    path('upload', upload, name='upload'),
    path('download/<int:document_id>/', download, name='download'),
    path('delete/<int:document_id>/', delete, name='delete'),
    path('share/<int:document_id>/', share, name='share'),

    # path('userDocumentMapping', userDocumentMapping, name='userDocumentMapping'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
