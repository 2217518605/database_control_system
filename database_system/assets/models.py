from django.db import models

from common.models import BaseModel

class Department(BaseModel):
    """ 部门表 """

    name = models.CharField('部门名称', max_length=64, unique=True)

    class Meta:
        db_table = 't_department'
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['id']

class Cluster(BaseModel):
    """ 集群表 """

    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='集群所属部门',related_name='clusters')

    name = models.CharField('集群名称', max_length=64)
    description = models.TextField('集群描述', blank=True, null=True)


    class Meta:
        db_table = 't_cluster'
        verbose_name = '集群'
        verbose_name_plural = '集群'
        ordering = ['id']
        unique_together = ('department', 'name')

class Instance(BaseModel):
    """ 实例表 """

    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, verbose_name='实例所属集群',related_name='instances')

    host = models.CharField('主机地址', max_length=128)
    port = models.PositiveIntegerField('端口', default=3306)
    username = models.CharField('账号', max_length=64)
    password_enc = models.TextField('加密密码')
    password_updated_at = models.DateTimeField('密码更新时间')
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 't_instance'
        verbose_name = '实例'
        verbose_name_plural = verbose_name
        unique_together = ('cluster', 'host', 'port')
        ordering = ['id']

class InstanceDailyStat(BaseModel):
    """ 每日实例数量统计 """

    stat_date = models.DateField('统计日期')
    department_name = models.CharField('部门名称', max_length=64)
    cluster_name = models.CharField('集群名称', max_length=64)
    instance_count = models.IntegerField('实例数量')

    class Meta:
        db_table = 't_instance_daily_stat'
        verbose_name = '每日实例统计'
        verbose_name_plural = verbose_name
        unique_together = ('stat_date', 'department_name', 'cluster_name')
        ordering = ['-stat_date', 'department_name', 'cluster_name']
        indexes = [
            models.Index(fields=['stat_date'], name='idx_stat_date'),
        ]
