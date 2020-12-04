from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib import admin
from .models import Website, Page


@admin.register(Website)
class WebsiteAdmin(ModelAdmin):
    # actions = [scrape_website]
    list_display = ['url']
    search_fields = ['url']


class ScrapeStatusFilter(SimpleListFilter):
    title = 'Page Status' # a label for our filter
    parameter_name = 'pages' # you can put anything here

    def lookups(self, request, model_admin):
        list_of_page = []
        queryset = Page.objects.all()
        for page in queryset:
            list_of_page.append(
                (str(page.title), page.title)
            )
        return sorted(list_of_page, key=lambda tp: tp[0])

    def queryset(self, request, queryset):
        print(request.GET)
        if 'pages' in request.GET:
            if self.value():
                return queryset.filter(title=self.value())
        return queryset


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['website', 'title']
    list_filter = (ScrapeStatusFilter,)
