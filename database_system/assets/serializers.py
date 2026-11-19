import secrets

from rest_framework import serializers
from django.utils import timezone

from .models import Department,Cluster,Instance,InstanceDailyStat
from .utils.crypto import encrypt


class DepartmentSerializer(serializers.ModelSerializer):
    """ 部门序列化器 """

    cluster_count = serializers.IntegerField(source='clusters.count', read_only=True)

    class Meta:
        model = Department
        fields = ['id','name','created_at','cluster_count']
        read_only_fields = ['created_at']

class ClusterSerializer(serializers.ModelSerializer):
    """ 集群序列化器 """

    department_name = serializers.CharField(source='department.name', read_only=True)
    instance_count = serializers.IntegerField(source='instances.count', read_only=True)

    class Meta:
        model = Cluster
        fields = ['id','name','created_at','department','department_name','instance_count']
        read_only_fields = ['created_at']

class InstanceSerializer(serializers.ModelSerializer):
    """ 实例序列化器 """

    cluster_name = serializers.CharField(source='cluster.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)
    # 只出的脱敏展示:
    password_display = serializers.SerializerMethodField()

    class Meta:
        model = Instance
        fields = ['id','host','port','username','is_active','password_updated_at','created_at','cluster','cluster_name','department_name','password_display']
        read_only_fields = ['created_at','password_updated_at','updated_at']

    def get_password_display(self, obj) -> str:
        """ 密码脱敏展示 """

        return '********'

    def validate_port(self, value) -> int:
        """ 端口校验 """

        if not 1 <= value <= 65535:
            raise serializers.ValidationError('端口必须在1-65535之间')
        return value

    def create(self, validated_data):
        # 未传明文密码则自动生成一个随机初始密码:
        plain = validated_data.pop('password', None) or secrets.token_urlsafe(24)
        validated_data['password_enc'] = encrypt(plain)
        validated_data['password_updated_at'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 改密码也走加密，不覆盖成明文:
        plain = validated_data.pop('password', None)
        if plain:
            validated_data['password_enc'] = encrypt(plain)
            validated_data['password_updated_at'] = timezone.now()
        return super().update(instance, validated_data)


class InstanceDailyStatSerializer(serializers.ModelSerializer):
    """ 统计的序列化器 """

    class Meta:
        model = InstanceDailyStat
        fields = '__all__'
        read_only_fields = ['created_at']

