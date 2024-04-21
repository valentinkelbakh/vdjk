# isort:skip_file
# flake8: noqa
from .apply import apply_router
from .base import base_router
from .holidays import holidays_router
from .menu import menu_router
from .projects import projects_router
from .recipes import recipes_router

routers = [
    apply_router,
    base_router,
    holidays_router,
    menu_router,
    projects_router,
    recipes_router,
]
