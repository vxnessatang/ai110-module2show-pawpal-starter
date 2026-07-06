"""PawPal+ system implementation.

Core classes generated from diagrams/uml_draft.mmd.

Ownership model:
    Owner --> Pet --> Task     (an owner has pets; each pet holds its own tasks)
    Owner --> Scheduler        (the owner uses one scheduler)
    Scheduler organizes tasks *across* all of an owner's pets.
"""

from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta


@dataclass
class Task:
    """A single activity for a pet (e.g. a walk, a feeding)."""

    description: str
    time: time
    priority: int  # lower number = higher priority (1 = top priority)
    completed: bool = False
    pet_name: str | None = None  # set when the task is attached to a pet
    frequency: str | None = None  # "daily", "weekly", or None (one-off)
    scheduled_date: date | None = None  # the day this task is scheduled for

    def check_off(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Return a fresh, uncompleted copy for this task's next occurrence.

        Returns None for one-off tasks (frequency is None). For recurring
        tasks, timedelta advances the scheduled_date accurately — timedelta
        handles month/year rollovers, so "today + 1 day" is always the real
        next day.
        """
        if self.frequency is None:
            return None

        step = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(
            self.frequency
        )
        if step is None:
            raise ValueError(f"Unknown frequency: {self.frequency!r}")

        # Advance from the current scheduled_date if set, otherwise from today.
        base = self.scheduled_date if self.scheduled_date is not None else date.today()
        return replace(self, completed=False, scheduled_date=base + step)


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
        """Attach a task to this pet, stamping it with the pet's name."""
        task.pet_name = self.name
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

    def complete_task(self, pet: Pet, task: Task) -> "Task | None":
        """Mark a task complete; if recurring, schedule its next occurrence.

        Returns the newly scheduled task (for daily/weekly), or None for a
        one-off task. The new instance is added to the same pet.
        """
        task.check_off()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.schedule_task(pet, next_task)
        return next_task

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks ordered by their scheduled time (earliest first).

        Uses sorted() with a lambda `key` that pulls out each task's time.
        Because Task.time is a datetime.time object, comparing them directly
        already gives correct chronological order:

            sorted(tasks, key=lambda t: t.time)

        (If time were instead a string in "HH:MM" 24-hour format, the same
        lambda would still sort correctly, since zero-padded "HH:MM" strings
        compare in the right order alphabetically: "09:30" < "10:00".)
        """
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        tasks: list[Task],
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return the subset of tasks matching the given filters.

        completed: keep only completed (True) or pending (False) tasks;
                   None keeps both.
        pet_name:  keep only tasks belonging to the pet with this name.
                   Each Task carries its own pet_name, so no lookup is needed.
        """
        result = tasks

        if completed is not None:
            result = [t for t in result if t.completed == completed]

        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]

        return result

    def find_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return a warning message for each pair of tasks at the same slot.

        Lightweight strategy: group tasks by their (scheduled_date, time) slot,
        and any slot holding more than one task is a conflict. Completed tasks
        are ignored. Returns a list of human-readable warnings (empty if none)
        rather than raising — the caller decides what to do with them.
        """
        slots: dict[tuple, list[Task]] = {}
        for task in tasks:
            if task.completed:
                continue
            slots.setdefault((task.scheduled_date, task.time), []).append(task)

        warnings: list[str] = []
        for (day, slot_time), clashing in slots.items():
            if len(clashing) > 1:
                who = ", ".join(f"{t.description} ({t.pet_name})" for t in clashing)
                warnings.append(
                    f"WARNING - Conflict on {day} at {slot_time.strftime('%H:%M')}: {who}"
                )
        return warnings

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
