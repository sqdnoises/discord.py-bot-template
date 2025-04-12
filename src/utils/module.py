import pkgutil
from typing import Any

__all__ = (
    "import_submodule",
    "list_modules",
)


def import_submodule(module_path: str) -> Any:
    """
    Import a submodule using __import__.

    Args:
        module_path (str): The path to the submodule (e.g., "A.B.C").

    Returns:
        Any: The imported submodule.
    """
    module = __import__(module_path)
    parts = module_path.split(".")
    for part in parts[1:]:
        module = getattr(module, part)
    return module


def list_modules(package: str | Any) -> list[str]:
    if type(package) == str:
        package = __import__(package)

    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(
        package.__path__, prefix=package.__name__ + "."  # type: ignore
    ):
        modules.append(modname)

    return modules
