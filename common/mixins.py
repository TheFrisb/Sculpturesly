from django.views.generic.base import ContextMixin


class TitleMixin(ContextMixin):
    """
    Adds a 'title' to the context.
    - Use 'self.title' for static titles
    - Or, override 'get_title()' for dynamic titles
    """

    def get_title(self):
        return getattr(self, "title", None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context
