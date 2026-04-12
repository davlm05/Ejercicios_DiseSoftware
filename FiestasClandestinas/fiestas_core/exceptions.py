"""Domain-level exceptions raised by the service layer.

Service callers (API views, SSR views) translate these into HTTP responses
or template errors. Repositories and models never raise these — they raise
ORM errors that services catch and rewrap.
"""


class DomainError(Exception):
    """Base class for all domain-level errors."""


class NotFoundError(DomainError):
    """A referenced entity does not exist."""


class ValidationError(DomainError):
    """Input data failed a business rule."""


class CapacidadExcedidaError(DomainError):
    """A fiesta cannot accept more invitados — its capacity is full."""


class EstadoInvalidoError(DomainError):
    """An invitado cannot transition from its current state."""
