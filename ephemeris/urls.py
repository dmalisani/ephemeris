from django.contrib import admin
from django.urls import path, include
from eph_calendar.viewsets import DatesViewSet
from eph_calendar.views import home

urlpatterns = [
    path('efemerides/', DatesViewSet.as_view()),
    path('admin/', admin.site.urls),
    path('/', home),
]
