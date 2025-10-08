# src/core/templatetags/navigation.py
from django import template
from django.urls import Resolver404, resolve

register = template.Library()


def _is_active_by_view(request, view_name: str) -> bool:
    """Return True if the current resolved view name equals view_name."""
    try:
        current = resolve(request.path_info)
        return current.view_name == view_name
    except Resolver404:
        return False


@register.simple_tag(takes_context=True)
def active_url(
    context,
    *view_names,
    startswith: str | None = None,
    active_class: str = "text-indigo-600 font-semibold",
):
    """
    Usage in templates:
      class="{% active_url 'core:landing' %}"
      class="{% active_url 'core:about' startswith='/about/' %}"

    Returns active_class when the current view name matches any provided view_names,
    or when request.path starts with the given prefix.
    """
    request = context.get("request")
    if not request:
        return ""
    # view-name match
    for name in view_names:
        if _is_active_by_view(request, name):
            return active_class
    # path prefix match
    if startswith and request.path.startswith(startswith):
        return active_class
    return ""


@register.simple_tag(takes_context=True)
def aria_current(context, *view_names, startswith: str | None = None):
    """
    Usage in templates:
      {% aria_current 'core:landing' %}
      {% aria_current 'core:about' startswith='/about/' %}

    Returns aria-current="page" when active; else empty string.
    """
    request = context.get("request")
    if not request:
        return ""
    for name in view_names:
        if _is_active_by_view(request, name):
            return 'aria-current="page"'
    if startswith and request.path.startswith(startswith):
        return 'aria-current="page"'
    return ""
