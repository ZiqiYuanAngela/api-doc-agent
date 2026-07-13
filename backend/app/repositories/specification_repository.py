from typing import Any


class SpecificationNotFoundError(KeyError):
    pass


class SpecificationRepository:
    def __init__(self) -> None:
        self._specifications: dict[str, dict[str, Any]] = {}

    def save(
        self,
        specification_id: str,
        specification: dict[str, Any],
    ) -> None:
        self._specifications[specification_id] = specification

    def get(self, specification_id: str) -> dict[str, Any]:
        specification = self._specifications.get(specification_id)

        if specification is None:
            raise SpecificationNotFoundError(
                f"Specification not found: {specification_id}"
            )

        return specification

    def exists(self, specification_id: str) -> bool:
        return specification_id in self._specifications


specification_repository = SpecificationRepository()