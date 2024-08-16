from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    family_name = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    icon = models.ImageField(upload_to='user_icons/', null=True, blank=True)

    def __str__(self):
        return self.username

User = get_user_model()

class PocketMoney(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pocket_money')
    group = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    aproved_by = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.child.username} - {self.group} - {self.get_transaction_type_display()} of {self.amount} on {self.date}"
    
class JobCard(models.Model):
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_card')
    group = models.CharField(max_length=100, blank=True, null=True)
    job_name = models.CharField(max_length=100, blank=False, null=False)
    money = models.DecimalField(max_digits=10, decimal_places=0)
    job_image = models.ImageField(upload_to='job_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.child.username} - {self.group} - {self.job_name} - {self.money}"
    
class JobReport(models.Model):
    job_name = models.CharField(max_length=100, blank=False, null=False)
    money = models.DecimalField(max_digits=10, decimal_places=0)
    group = models.CharField(max_length=100, blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.job_name} - {self.money} - {self.reported_by.username} - {self.group} - {self.reported_at} - {self.status}"
    
class WithdrawalRequest(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    money = models.DecimalField(max_digits=10, decimal_places=0)
    group = models.CharField(max_length=100, blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.title} - {self.money} - {self.reported_by.username} - {self.group} - {self.reported_at} - {self.status}"