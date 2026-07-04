"""PawPal+ system implementation.

Core classes generated from diagrams/uml_draft.mmd.

Ownership model:
    Owner --> Pet --> Task     (an owner has pets; each pet holds its own tasks)
    Owner --> Scheduler        (the owner uses one scheduler)
    Scheduler organizes tasks *across* all of an owner's pets.
"""

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    """A single activity for a pet (e.g. a walk, a feeding)."""

    description: str
    time: time
    priority: int  # lower number = higher priority (1 = top priority)
    completed: bool = False

    def check_off(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Stores a pet's details and the tasks scheduled for it."""

    name: str
    hunger: int = 0
    health: int = 100
    tasks: list[Task] = field(default_factory=list)

    def eat(self) -> None:
        """Feed the pet, reducing hunger (clamped at 0)."""
        self.hunger = max(0, self.hunger - 20)

    def walk(self) -> None:
        """Walk the pet: improves health but builds up hunger."""
        self.health = min(100, self.health + 10)
        self.hunger = min(100, self.hunger + 10)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    scheduler: "Scheduler" = field(default_factory=lambda: Scheduler())
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        if pet not in self.pets:
            self.pets.append(pet)

    def schedule_task(self, pet: Pet, task: Task) -> None:
        """Schedule a task for one of this owner's pets, via the scheduler."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not one of {self.name}'s pets.")
        self.scheduler.schedule_task(pet, task)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    """The 'brain': retrieves, organizes, and manages tasks across pets."""

    def schedule_task(self, pet: Pet, task: Task) -> None:
        """Add a task to a pet's task list."""
        pet.add_task(task)

    def make_plan(self, pets: list[Pet]) -> list[Task]:
        """Build an ordered plan of outstanding tasks, sorted by time then priority."""
        # Completed tasks are excluded. On a time conflict, the higher-priority
        # (lower-numbered) task is kept and the other is dropped.
        pending = [task for pet in pets for task in pet.tasks if not task.completed]

        # Sort by time, then by priority (1 = top priority) as a tiebreaker.
        pending.sort(key=lambda t: (t.time, t.priority))

        plan: list[Task] = []
        for task in pending:
            # Conflict rule: skip a task that shares a time slot with one
            # already chosen (the earlier one wins because it is higher
            # priority thanks to the sort above).
            if plan and plan[-1].time == task.time:
                continue
            plan.append(task)
        return plan
