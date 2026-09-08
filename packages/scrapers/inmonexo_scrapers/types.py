from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectDraft:
    project_name: str
    source_url: str
    project_url: str | None = None
    district: str | None = None
    address: str | None = None
    status_label: str | None = None
    price_text: str | None = None
