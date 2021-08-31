from django.contrib import admin
from .models.product import Products
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
import csv
from django.http import HttpResponse
import sys
if sys.version_info[0] >= 3:
    unicode = str

def export_as_csv_action(description="Export selected objects as CSV file", fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])

        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset

        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)

        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])

        return response

    export_as_csv.short_description = description
    return export_as_csv


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']	
    actions=[export_as_csv_action("Dowload CSV",fields=["name","price","category"])]
		

class AdminOrders(admin.ModelAdmin):
    display=["product","customer","quantity","price","date","status"]
    actions=[export_as_csv_action("Download CSV",fields=["product","customer","quantity","price","date","status"])]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    actions=[export_as_csv_action("Download CSV",fields=["name"])]

class AdminCustomer(admin.ModelAdmin):
    display = ["first_name","last_name","phone","email"]
    actions=[export_as_csv_action("Download CSV",["first_name","last_name","phone","email"])]
# Register your models here.
admin.site.register(Products,AdminProduct)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Order,AdminOrders)



