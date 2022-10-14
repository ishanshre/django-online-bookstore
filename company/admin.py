from django.contrib import admin
from .models import (
    Company,
    CompanyPhoneNumber,
    Achievement,
    FAQ,
    Carrer,
    CV,
)
# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyPhoneNumber)
admin.site.register(Achievement)
admin.site.register(FAQ)
admin.site.register(Carrer)
admin.site.register(CV)