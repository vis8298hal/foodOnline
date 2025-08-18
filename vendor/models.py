from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_accounts_email


# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="user_profile", on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=150)
    vendor_license = models.ImageField(upload_to='vendor/license',)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                if self.is_approved:
                    domain = "127.0.0.1:8000/"
                    subject = "Congratulations! Your Restraunt has been approved"
                    template = "accounts/emails/vendor_approval_email.html"
                    context = {
                        "user": self.user,
                        "is_approved": self.is_approved,
                        "domain": domain,
                    }
                else:
                    subject = "Sorry! Not Eligible for Partner"
                    template = "accounts/emails/vendor_approval_email.html"
                    context = {
                        "user": self.user,
                        "is_approved": self.is_approved,
                    }
                send_accounts_email(user=self.user, subject=subject, template=template, context=context)
        return super(Vendor, self).save(*args, **kwargs)