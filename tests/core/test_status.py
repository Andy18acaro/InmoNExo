import pytest

from inmonexo_core.enums import ProjectStatus
from inmonexo_core.status import map_project_status


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("PRE VENTA", ProjectStatus.PRE_SALE),
        ("Pre venta", ProjectStatus.PRE_SALE),
        ("LANZAMIENTO", ProjectStatus.PRE_SALE),
        ("Nuevo lanzamiento", ProjectStatus.PRE_SALE),
        ("EN CONSTRUCCIÓN", ProjectStatus.UNDER_CONSTRUCTION),
        ("En construcción", ProjectStatus.UNDER_CONSTRUCTION),
        ("ENTREGA INMEDIATA", ProjectStatus.READY_TO_MOVE),
        ("Entrega inmediata", ProjectStatus.READY_TO_MOVE),
        ("Pronta entrega", ProjectStatus.READY_TO_MOVE),
        ("ENTREGADO", ProjectStatus.DELIVERED),
        ("", ProjectStatus.UNKNOWN),
        ("En planos", ProjectStatus.PRE_SALE),
        ("En lanzamiento", ProjectStatus.PRE_SALE),
    ],
)
def test_map_project_status(label: str, expected: ProjectStatus) -> None:
    assert map_project_status(label) == expected
