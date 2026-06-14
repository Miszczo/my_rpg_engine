"""Quest system with objectives, status lifecycle, and rewards."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from engine.exceptions import GameError


class QuestStatus(Enum):
    """Lifecycle states for a quest."""

    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class QuestObjective:
    """Single progress target within a quest."""

    description: str
    target_count: int = 1
    current_count: int = 0

    def advance(self, amount: int = 1) -> None:
        """Increase progress toward the objective target.

        Args:
            amount: Progress increment. Non-positive values are ignored.
        """
        if amount <= 0:
            return
        self.current_count = min(self.target_count, self.current_count + amount)

    @property
    def is_complete(self) -> bool:
        """Return True when the objective target has been reached."""
        return self.current_count >= self.target_count


class Quest:
    """Quest with objectives, rewards, and a status lifecycle."""

    _next_id: int = 1

    def __init__(
        self,
        title: str,
        description: str = "",
        xp_reward: int = 50,
        gold_reward: int = 20,
        objectives: list[QuestObjective] | None = None,
    ) -> None:
        """Create a quest in the AVAILABLE state.

        Args:
            title: Short quest title.
            description: Longer quest description.
            xp_reward: Experience granted on completion.
            gold_reward: Gold granted on completion.
            objectives: Optional list of quest objectives.
        """
        self._id = Quest._next_id
        Quest._next_id += 1
        self.title = title
        self.description = description
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.objectives: list[QuestObjective] = (
            list(objectives) if objectives is not None else []
        )
        self.status = QuestStatus.AVAILABLE

    @property
    def id(self) -> int:
        """Unique identifier assigned at creation time."""
        return self._id

    @property
    def objectives_complete(self) -> bool:
        """Return True when every objective has been fulfilled."""
        return all(objective.is_complete for objective in self.objectives)

    def accept(self) -> None:
        """Move the quest from AVAILABLE to ACTIVE.

        Raises:
            GameError: If the quest is not in the AVAILABLE state.
        """
        if self.status is not QuestStatus.AVAILABLE:
            raise GameError(
                f"Quest {self.title!r} can only be accepted when available."
            )
        self.status = QuestStatus.ACTIVE

    def complete(self) -> tuple[int, int]:
        """Complete the quest and return rewards.

        Returns:
            Tuple of ``(xp_reward, gold_reward)``.

        Raises:
            GameError: If the quest is not active or objectives are incomplete.
        """
        if self.status is not QuestStatus.ACTIVE:
            raise GameError(
                f"Quest {self.title!r} can only be completed when active."
            )
        if not self.objectives_complete:
            raise GameError(
                f"Quest {self.title!r} objectives are not yet fulfilled."
            )
        self.status = QuestStatus.COMPLETED
        return (self.xp_reward, self.gold_reward)

    def fail(self) -> None:
        """Mark an active quest as failed.

        Raises:
            GameError: If the quest is not active.
        """
        if self.status is not QuestStatus.ACTIVE:
            raise GameError(
                f"Quest {self.title!r} can only be failed when active."
            )
        self.status = QuestStatus.FAILED

    def __repr__(self) -> str:
        return (
            f"Quest(id={self._id}, title={self.title!r}, "
            f"status={self.status.value})"
        )
