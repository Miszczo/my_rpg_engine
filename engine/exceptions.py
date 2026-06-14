"""Domain exception hierarchy for the RPG engine."""


class GameError(Exception):
    """Base exception for all game-domain errors."""


class InventoryFullError(GameError):
    """Raised when an item cannot be added because inventory capacity is reached."""


class InsufficientStatsError(GameError):
    """Raised when a character lacks resources (e.g. mana) for an action."""


class InvalidItemError(GameError):
    """Raised when an item is invalid for the requested operation."""
