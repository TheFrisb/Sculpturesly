def get_unique_slug(model_class, base_slug, instance=None, counter=1):
    """
    Generate a unique slug, appending a counter if necessary.
    """
    slug = base_slug if counter == 1 else f"{base_slug}-{counter}"
    queryset = model_class.objects.filter(slug=slug)
    if instance:
        queryset = queryset.exclude(pk=instance.pk)
    if not queryset.exists():
        return slug
    return get_unique_slug(model_class, base_slug, instance, counter + 1)
