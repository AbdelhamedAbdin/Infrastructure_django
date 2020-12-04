from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


class SpeciesListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'title'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'query'

    default_value = None

    def lookups(self, request, model_admin):
        list_of_species = []
        queryset = Book.objects.all()
        for species in queryset:
            list_of_species.append(
                (str(species.id), species.title)
            )
        return sorted(list_of_species, key=lambda tp: tp[0])

    def queryset(self, request, queryset):
        if 'query' in request.GET:
            if self.value():
                return queryset.filter(id=self.value())
        else:
            return queryset

    def value(self):
        """
        Overriding this method will allow us to always have a default value.
        """
        value = super(SpeciesListFilter, self).value()
        if value is None:
            if self.default_value is None:
                first_species = Book.objects.order_by('title').first()
                value = None if first_species is None else first_species.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = (SpeciesListFilter, 'author__last_name')

    inlines = [BooksInstanceInline]
    # def display_genre(self):
    #     return ', '.join(genre.name for genre in self.genre.all()[:])
    #
    # display_genre.short_description = 'Genre'


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
