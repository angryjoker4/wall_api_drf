from django.contrib import admin
from django.contrib import messages

from .models import Category, Ad, AdReport


@admin.register(Category)
class AdsAdmin(admin.ModelAdmin):
    pass


class AdReportTabu(admin.TabularInline):
    model = AdReport
    fields = ('user', 'report_reason', 'datetime_reported')
    readonly_fields = fields
    ordering = ('-datetime_reported', )
    max_num = 0


@admin.register(Ad)
class AdsAdmin(admin.ModelAdmin):
    readonly_fields = ('author', 'datetime_modified', 'expiration_date', 'datetime_deleted')
    list_display = ('title', 'price', 'active', 'confirmation', 'datetime_modified', 'expiration_date', 'is_delete')
    ordering = ('-datetime_modified', )
    list_filter = ('active', 'is_delete', 'is_block')
    actions = ('soft_delete_selected', )
    inlines = (AdReportTabu, )

    def get_fields(self, request, obj=None):
        fields = ['author', 'title', 'text', 'price', 'image', 'status_product', 'category',
                  'location', 'phone', 'active', 'slug', 'confirmation', 'datetime_modified', 'expiration_date']

        if obj.is_block:
            fields.append('is_block')

        if obj.is_delete:
            fields.extend(['is_delete', 'delete_with', 'datetime_deleted'])

        return fields

    def delete_model(self, request, obj):
        if not obj.is_delete:
            obj.soft_delete('staff')
        else:
            messages.info(request, 'Ad has was deleted')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def soft_delete_selected(self, request, queryset):
        # Perform the soft deletion for selected objects
        for obj in queryset:
            obj.soft_delete(reason='staff')

    soft_delete_selected.short_description = 'Soft delete selected objects'
