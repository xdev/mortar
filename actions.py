def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
    make_active.short_description = "Mark selected items as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
    make_inactive.short_description = "Mark selected items as inactive"
