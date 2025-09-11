from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_accounts_email
from datetime import time, datetime


# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="user_profile", on_delete=models.CASCADE)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=150)
    vendor_license = models.FileField(upload_to='vendor/license',)
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
    @property
    def is_open(self):
        is_open = None
        def_time_format = "%H:%M:%S"
        today = datetime.now()
        current_time = today.strftime(def_time_format)
        today = today.strftime("%u")
        today_opening_hour = OpeningHour.objects.filter(vendor=self, day=today)
        for hour in today_opening_hour:
            if not hour.is_closed:
                start_time = str(datetime.strptime(hour.from_hour, "%I:%M %p").time())
                end_time = str(datetime.strptime(hour.to_hour, "%I:%M %p").time())
                print(self.vendor_name,start_time, end_time, current_time)
                if current_time > start_time and current_time < end_time:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open
DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]
HOUR_OF_DAY_24 = [(time(h,m).strftime("%I:%M %p"),time(h,m).strftime("%I:%M %p")) for h in range(0,24) for m in range(0,31,30) ]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=20, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=20, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ("day", "from_hour")
        unique_together = ("vendor", "day", "from_hour", "to_hour")

    def __str__(self):
        return self.get_day_display()