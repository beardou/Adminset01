from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    """   所有资产的共有数据表   """
    asset_type_choice = (
        (str(1), u'物理机'),
        (str(2), u'虚拟机'),
        (str(3), u'容器'),
        (str(4), u'网络设备'),
        (str(5), u'安全设备'),
        (str(6), u'存储设备'),
        (str(7), u'其他'),
    )

    asset_status = (
        (str(1), u'使用中'),
        (str(2), u'未使用'),
        (str(3), u'故障'),
        (str(4), u'其它'),
    )

    network_choice = (
        (str(1), u'控制专网'),
        (str(2), u'业务内网'),
        (str(3), u'业务外网'),
    )


    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    asset_name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')  # 不可重复
    asset_no = models.CharField(max_length=50, unique=True, blank=True, verbose_name ='资产编号') # 不可重复
    network_location = models.CharField(choices=network_choice, max_length=64, verbose_name='所属网络')
    organization = models.ForeignKey('Organization', null=True, blank=True, on_delete=models.CASCADE, verbose_name='所属单位')
    status = models.CharField(max_length=50, choices=asset_status, default=0, verbose_name='设备状态')

    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.CASCADE)
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='设备型号')
    sn = models.CharField(max_length=128, unique=True, verbose_name='产品序列号')  # 不可重复

    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    tags = models.ManyToManyField('Tag', blank=True)
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='admin')
    idc = models.ForeignKey('IDC', null=True, blank=True, on_delete=models.CASCADE)

    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, null=True, blank=True)
    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='approved_by')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.asset_name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        ordering = ['-c_time']


class Server(models.Model):
    """  服务器设备  """

    sub_asset_type_choice = (
        (str(1), u'PC服务器'),
        (str(2), u'小型机'),
        (str(3), u'刀片机'),
    )

    created_by_choice = (
        (str(1), u'自动添加'),
        (str(2), u'手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name='添加方式')
    hosted_on = models.ForeignKey('self', on_delete=models.CASCADE, related_name='hosted_on_server',
                                  blank=True, null=True)  # 虚拟机专用字段

    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统类型')
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行版本')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统版本')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.asset_name, self.get_sub_asset_type_display(), self.asset.model,self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'


class SecurityDevice(models.Model):
    """  安全设备  """
    sub_asset_type_choice = (
        (str(1), u'防火墙'),
        (str(2), u'入侵检测设备'),
        (str(3), u'入侵防御设备'),
        (str(4), u'综合安全网关'),
        (str(5), u'数据库审计系统'),
        (str(6), u'运维审计系统'),
        (str(7), u'防病毒网关'),
        (str(8), u'WAF防火墙'),
        (str(9), u'安全配置核查'),
        (str(10), u'网络准入系统'),
        (str(11), u'网闸设备'),
        (str(12), u'VPN设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')

    def __str__(self):
        return self.asset.asset_name + '--' + self.get_sub_asset_type_display() + ' id:%s' % self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = '安全设备'


class StorageDevice(models.Model):
    """  存储设备  """
    sub_asset_type_choice = (
        (str(1), u'磁盘阵列'),
        (str(2), u'网络存储器'),
        (str(3), u'光纤交换机'),
        (str(4), u'磁带库'),
        (str(5), u'磁带机'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='存储设备类型')

    def __str__(self):
        return self.asset.asset_name + '--' + self.get_sub_asset_type_display() + ' id:%s' % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = '存储设备'


class NetworkDevice(models.Model):
    """   网络设备 """

    sub_asset_type_choice = (
        (str(1), u'路由器'),
        (str(2), u'交换机'),
        (str(3), u'工业交换机'),
        (str(4), u'无线控制器'),
        (str(5), u'无线AP'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(max_length=64, choices=sub_asset_type_choice, default=0, verbose_name='网络设备类型')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.asset_name, self.get_sub_asset_type_display(), self.asset.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'


class Software(models.Model):
    """  只保存付费购买的软件   """

    sub_asset_type_choice = (
        (str(1), '操作系统'),
        (str(2), '数据库'),
        (str(3), '中间件'),
    )

    sub_asset_type = models.CharField(max_length=64,choices=sub_asset_type_choice, default=0, verbose_name='软件类型')
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField(max_length=64, unique=True, help_text='例如: CentOS release 6.7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = '软件/系统'


class IDC(models.Model):
    """  机房  """
    name = models.CharField(max_length=64, unique=True, verbose_name='机房名称')
    address = models.CharField(max_length=64, unique=True, verbose_name='机房地址')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'


class Vendor(models.Model):
    """  生产厂商  """

    name = models.CharField(max_length=64, unique=True, verbose_name='厂商名称')
    telephone = models.CharField(max_length=30, blank=True, null=True, verbose_name='支持电话')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '生产厂商'
        verbose_name_plural = '生产厂商'



class Supplier(models.Model):
    """   供应商  """

    name = models.CharField(max_length=64, unique=True, verbose_name='供应商名称')
    telephone = models.CharField(max_length=30, blank=True, null=True, verbose_name='支持电话')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'



class Organization(models.Model):
    """ 组织机构  """

    parent_unit = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='parent_level')
    name = models.CharField(max_length=64, unique=True, verbose_name='机构')
    memo = models.CharField(max_length=64, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '所属单位'
        verbose_name_plural = '所属单位'



class Contract(models.Model):
    """  合同  """
    sn = models.CharField(max_length=128, unique=True, verbose_name='合同号')
    name = models.CharField(max_length=64, verbose_name='合同名称')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    detail = models.TextField(blank=True, null=True, verbose_name='合同详细')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'



class Tag(models.Model):
    """  标签  """
    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    c_day = models.DateField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """
    event_type_choice = (
        (str(1), '硬件变更'),
        (str(2), '新增配件'),
        (str(3), '设备下线'),
        (str(4), '设备上线'),
        (str(5), '定期维护'),
        (str(6), '业务上线\更新\变更'),
        (str(7), '其它'),
    )
    name = models.CharField(max_length=128, verbose_name='事件名称')
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    #new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.CharField(max_length=64, choices=event_type_choice, default=4, verbose_name='事件类型')
    component = models.CharField(max_length=256, blank=True, null=True, verbose_name='事件子项')
    detail = models.TextField(verbose_name='事件详情')
    date = models.DateTimeField(auto_now_add=True,verbose_name='事件时间')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = '事件纪录'
