import logging
import secrets

from django.db.models import Count
from django.utils import timezone
from celery import shared_task

from assets.models import Instance, InstanceDailyStat
from assets.utils.crypto import encrypt

logger = logging.getLogger(__name__)


@shared_task
def random_instance_password():
    """ 每隔12小时就随机轮换每个实例的密码并且进行加密记录 """

    now_time = timezone.now()
    instance_list = list(
        Instance.objects.filter(is_active=True).only("id", "password_enc")
    )

    if not instance_list:
        logger.info(f"没有需要轮换密码的实例")
        return 0

    for instance in instance_list:
        instance.password_enc = encrypt(secrets.token_hex(16))
        instance.password_updated_at = now_time

    Instance.objects.bulk_update(instance_list, ["password_enc", "password_updated_at"], batch_size=200)
    logger.info(f"成功轮换{len(instance_list)}个实例的密码")
    return len(instance_list)


@shared_task
def daily_instance_stats():
    """ 每天00:00按照部门和集群维度统计实例数量 """

    today = timezone.localdate()

    rows = (
        Instance.objects.values("cluster__department__name", "cluster__name").annotate(cnt=Count("id")).
        order_by("cluster__department__name", "cluster__name")
    )

    objs = [(
        InstanceDailyStat(
            stat_date=today,
            department_name=row["cluster__department__name"],
            cluster_name=row["cluster__name"],
            instance_count=row["cnt"],
        )
    )
        for row in rows]

    if not objs:
        logger.info(f"没有需要统计的实例")
        return 0

    InstanceDailyStat.objects.bulk_create(objs, ignore_conflicts=True)
    logger.info(f"每日统计完成，一共成功统计{len(objs)}个实例")
    return len(objs)
