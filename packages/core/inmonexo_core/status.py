from inmonexo_core.enums import ProjectStatus

_STATUS_MAP: dict[str, ProjectStatus] = {
    "pre venta": ProjectStatus.PRE_SALE,
    "pre-venta": ProjectStatus.PRE_SALE,
    "preventa": ProjectStatus.PRE_SALE,
    "nuevo lanzamiento": ProjectStatus.PRE_SALE,
    "lanzamiento": ProjectStatus.PRE_SALE,
    "en planos": ProjectStatus.PRE_SALE,
    "en lanzamiento": ProjectStatus.PRE_SALE,
    "en construccion": ProjectStatus.UNDER_CONSTRUCTION,
    "en construcción": ProjectStatus.UNDER_CONSTRUCTION,
    "entrega inmediata": ProjectStatus.READY_TO_MOVE,
    "pronta entrega": ProjectStatus.READY_TO_MOVE,
    "listo para vivir": ProjectStatus.READY_TO_MOVE,
    "entregado": ProjectStatus.DELIVERED,
    "proyecto entregado": ProjectStatus.DELIVERED,
}


def map_project_status(label: str | None) -> ProjectStatus:
    if not label or not label.strip():
        return ProjectStatus.UNKNOWN

    key = " ".join(label.strip().lower().split())
    return _STATUS_MAP.get(key, ProjectStatus.UNKNOWN)
