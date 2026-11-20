from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import InstanceDailyStatViewSet, DepartmentViewSet, ClusterViewSet, InstanceViewSet

router = DefaultRouter()

router.register("department", DepartmentViewSet, basename="department")
router.register("cluster", ClusterViewSet, basename="cluster")
router.register("instance", InstanceViewSet, basename="instance")
router.register("instance-daily-stat", InstanceDailyStatViewSet, basename="instance-daily-stat")

urlpatterns = router.urls
