import time
from time import sleep
import socket

from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response

from assets.models import Department, Cluster, Instance, InstanceDailyStat
from assets.serializers import DepartmentSerializer, ClusterSerializer, InstanceSerializer, \
    InstanceDailyStatSerializer


class DepartmentViewSet(ModelViewSet):
    """ 部门的CRUD """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        if keyword:
            qs = qs.filter(name__icontains=keyword)
        return qs


class ClusterViewSet(ModelViewSet):
    """ 集群的CRUD """

    queryset = Cluster.objects.select_related('department').all()  # 解决 n + 1
    serializer_class = ClusterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        department = self.request.query_params.get('department')
        if department:
            qs = qs.filter(department_id=department)
        return qs


class InstanceViewSet(ModelViewSet):
    """ 实例的CRUD """

    queryset = Instance.objects.select_related("cluster", "cluster__department").all()
    serializer_class = InstanceSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        cluster = self.request.query_params.get('cluster')
        is_active = self.request.query_params.get('is_active')
        if cluster:
            qs = qs.filter(cluster_id=cluster)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() in ('true', 'yes', '1'))
        return qs

    @action(detail=True, methods=['post'], url_path="probe")
    def probe(self, request, pk=None):
        """ 检查某个实例的 TCP 端口是否可达"""

        instance = self.get_object()
        start = time.perf_counter()  # 记录开始时间
        reachable = False  # 标记
        error = ""  # 错误信息

        try:
            with socket.create_connection((instance.host, instance.port), timeout=settings.PROBE_TIMEOUT):
                reachable = True
        except socket.timeout:
            error = "超时了"
        except OSError as exc:
            error = str(exc)

        return Response({
            "instance_id": instance.id,
            "host": instance.host,
            "port": instance.port,
            "reachable": reachable,
            "error": error,
            "time_seconds": settings.PROBE_TIMEOUT,
            "elapsed_ms": round((time.perf_counter() - start) * 1000, 2),
            "checked_at": timezone.now()
        }, status=status.HTTP_200_OK)


class InstanceDailyStatViewSet(ReadOnlyModelViewSet):
    """ 统计实例结果 """

    queryset = InstanceDailyStat.objects.all()
    serializer_class = InstanceDailyStatSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        stat_date = self.request.query_params.get('stat_date')
        if stat_date:
            qs = qs.filter(stat_date=stat_date)
        return qs
