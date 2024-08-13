from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PocketMoney, JobCard, JobReport, WithdrawalRequest

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birthdate', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# PocketMoneyモデルのAdminクラスを作成（オプション）
class PocketMoneyAdmin(admin.ModelAdmin):
    list_display = ('child', 'group', 'amount', 'date', 'transaction_type', 'memo')  # 一覧表示で見たいフィールドを指定
    search_fields = ('child__username', 'transaction_type')  # 検索フィールドを指定
    list_filter = ('transaction_type', 'date')  # フィルタリングオプションを指定

# PocketMoneyモデルを管理サイトに登録
admin.site.register(PocketMoney, PocketMoneyAdmin)

class JobCardAdmin(admin.ModelAdmin):
    list_display = ('child', 'group', 'job_name', 'money', 'job_image')
    search_fields = ('child__username', 'job_name')

admin.site.register(JobCard, JobCardAdmin)

class JobReportAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'money', 'group', 'reported_by', 'reported_at', 'status')
    search_fields = ('reported_by__username', 'group', 'status')

admin.site.register(JobReport, JobReportAdmin)

class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'money', 'group', 'reported_by', 'reported_at', 'status')
    search_fields = ('reported_by__username', 'group', 'status')

admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
