from django.contrib import admin
from accounts.models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.contrib import admin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = []
    list_filter = ['email', 'id']
    list_display = ['email']
    ordering = ('email',)
    exclude = [
        'is_staff',
        'username',
        'is_active'
    ]
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('active', 'staff', 'admin', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = [
        'date_joined',
    ]

    actions = [
        'activate_users',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        if (
            not is_superuser and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def activate_users(self, request, queryset):
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, 'Activated {} users.'.format(cnt))
    activate_users.short_description = 'Activate Users'


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'
    title = 'user'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

    def queryset(self, request, queryset):
        term = self.value()

        if term is None:
            return

        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(user__email__icontains=bit) |
                Q(user__last_name__icontains=bit)
            )

        return queryset.filter(any_name)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin, admin.SimpleListFilter):
    list_display = ['user']
    list_filter = [InputFilter]