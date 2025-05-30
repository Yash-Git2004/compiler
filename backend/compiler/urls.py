from django.urls import path            # Import the path function to define URL routes
from .views import CompileCodeView      # Import the view that will handle the 'compile' endpoint

# Define URL patterns for this app
urlpatterns = [
    path('compile/', CompileCodeView.as_view(), name='compile-code'),
]
