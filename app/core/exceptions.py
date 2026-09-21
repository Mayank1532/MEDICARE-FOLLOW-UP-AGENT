class AppError(Exception):
    """Base exception for expected application errors."""

    def __init__(self, message: str, code: str = "APPLICATION_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class PatientNotFoundError(AppError):
    """Raised when a requested patient does not exist."""

    def __init__(self, patient_id: str) -> None:
        super().__init__(
            message=f"Patient '{patient_id}' was not found.",
            code="PATIENT_NOT_FOUND",
        )


class WorkflowExecutionError(AppError):
    """Raised when a follow-up workflow cannot be completed."""

    def __init__(
        self,
        workflow: str,
        message: str = "The workflow could not be completed.",
    ) -> None:
        super().__init__(
            message=message,
            code="WORKFLOW_EXECUTION_ERROR",
        )
        self.workflow = workflow
