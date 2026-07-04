"""PawPal+ system skeleton.

Class stubs generated from diagrams/uml_draft.mmd.
Attributes and method signatures only — method bodies are left as stubs.
"""

from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    hunger: int = 0
    health: int = 100

    def eat(self) -> None:
        """Feed the pet (reduce hunger)."""
        ...

    def walk(self) -> None:
        """Walk the pet (affects health)."""
        ...


@dataclass
class Task:
    description: str
    time: str
    priority: int
    completed: bool = False

    def check_off(self) -> None:
        """Mark this task as completed."""
        ...


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        ...

    def schedule_walk(self, pet: Pet, time: str) -> None:
        """Schedule a walk for the given pet at the given time."""
        ...

    def see_todays_tasks(self) -> list[Task]:
        """Return the tasks scheduled for today."""
        ...


@dataclass
class Scheduler:
    tasks_remaining: list[Task] = field(default_factory=list)

    def schedule_task(self, task: Task) -> None:
        """Add a task to the schedule, respecting time and priority constraints."""
        ...

    def make_plan(self) -> list[Task]:
        """Produce an ordered plan of tasks based on time and priority."""
        ...
