
from typing import ClassVar, Protocol, TypeVar
from models.validation_result import ValidationResult

ResultType = TypeVar("ResultType", bound=ValidationResult)
class ResultRepositoryProtocol(Protocol[ResultType]):
    dsn: ClassVar[str | None]
    
    @classmethod
    def set_dsn(cls, dsn: str) -> None: ...

    @classmethod
    def add(cls, validation_result: ResultType) -> None: ...

    @classmethod
    def add_list(cls, results: list[ResultType], /) -> None: ...


    @classmethod
    def get_by_run_id(cls, run_id: int) -> list[ResultType]: ...

