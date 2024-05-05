from django import template
from django.urls import resolve, Resolver404
from menu.models import MenuItem
from django.db.models import Prefetch

register = template.Library()


def get_item_dict(item: MenuItem, paths: list[str]) -> dict:
    children = []

    if paths and item.url == paths[0]:
        next_paths = paths[1:]
        children = [get_item_dict(child, next_paths) for child in item.children.all()]

    return {
        "id": item.id,
        "name": item.name,
        "url": item.url,
        "named_url": item.named_url,
        "absolute_url": item.get_absolute_url(),
        "children": children,
    }


def check_url(paths: list[str]) -> bool:
    if len(paths) == 0:
        return

    item = MenuItem.objects.filter(url=paths[0], parent=None).first()

    try:
        for path in paths[1:]:
            item = item.children.get(url=path)
            print(item, flush=True)
    except MenuItem.DoesNotExist:
        raise Resolver404


@register.inclusion_tag("menu.html", takes_context=True)
def draw_menu(context):
    path = context["request"].path
    path = resolve(path).kwargs.get("path")
    paths = list(filter(lambda x: x, path.split("/")))
    paths = [""] + paths

    print(path, paths, flush=True)

    check_url(paths)

    items = MenuItem.objects.filter(url="").prefetch_related("children").prefetch_related("children")
    menu_items = [get_item_dict(item, paths) for item in items]
    return {"menu_items": menu_items}
