from django.contrib import admin

# Register your models here.

from .models import  *

class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'asset_no', 'organization', 'model','sn','idc']


class ServerAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'manage_ip','sub_asset_type', 'sn', 'os_type']

    def asset_name(self, obj):
        '''
        这个方法就是用来对asset_name这个字段做处理，把我们需要展示的前端内容截取出来。
        需要注意的是，方法名必须要和在list_display里面的一致，这样才可以调用。
        '''
        return obj.asset.asset_name  # asset是我们SaltGroup表中一对多的字段，asset_name是刚才我们自定义的字段，
    #asset_name.short_description = "Minion's ID "  # 对asset_name这个做个简短的title。

    def sn(self, obj):
       return obj.asset.sn

    def manage_ip(self, obj):
       return obj.asset.manage_ip


class SecurityDeviceAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'manage_ip', 'sub_asset_type', 'sn']

    def asset_name(self, obj):
        return obj.asset.asset_name

    def sn(self, obj):
        return obj.asset.sn

    def manage_ip(self, obj):
       return obj.asset.manage_ip

class StorageDeviceDeviceAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'manage_ip', 'sub_asset_type', 'sn']

    def asset_name(self, obj):
        return obj.asset.asset_name

    def sn(self, obj):
        return obj.asset.sn

    def manage_ip(self, obj):
       return obj.asset.manage_ip

class NetworkDeviceDeviceAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'manage_ip', 'sub_asset_type', 'sn']

    def asset_name(self, obj):
        return obj.asset.asset_name

    def sn(self, obj):
        return obj.asset.sn

    def manage_ip(self, obj):
       return obj.asset.manage_ip

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['parent_unit', 'name', 'memo']




admin.site.register(Asset, AssetAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(SecurityDevice,SecurityDeviceAdmin)
admin.site.register(StorageDevice,StorageDeviceDeviceAdmin)
admin.site.register(NetworkDevice,NetworkDeviceDeviceAdmin)
admin.site.register(Software)
admin.site.register(IDC)
admin.site.register(Vendor)
admin.site.register(Supplier)
admin.site.register(Organization,OrganizationAdmin)
admin.site.register(Contract)
admin.site.register(Tag)
admin.site.register(EventLog)
