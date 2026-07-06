import sys
from datetime import date, time, timedelta
from pathlib import Path

# Make the project root importable so `pawpal_system` resolves from tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Scheduler, Task


def test_task_completion():
    """check_off() should change the task's status to completed."""
    task = Task("Feed the dog", time(8, 0), priority=1)
    assert task.completed is False

    task.check_off()

    assert task.completed is True


def test_task_addition_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count."""
    dog = Pet("Rex")
    assert len(dog.tasks) == 0

    dog.add_task(Task("Walk the dog", time(9, 0), priority=2))

    assert len(dog.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks earliest-first, regardless of input order."""
    scheduler = Scheduler()
    # Deliberately added out of chronological order.
    evening = Task("Walk the dog", time(17, 0), priority=3)
    morning = Task("Feed the dog", time(8, 0), priority=2)
    midday = Task("Give meds", time(12, 30), priority=1)

    ordered = scheduler.sort_by_time([evening, morning, midday])

    assert ordered == [morning, midday, evening]


def test_sort_by_time_does_not_mutate_input():
    """sort_by_time() should return a new list, leaving the original order intact."""
    scheduler = Scheduler()
    original = [
        Task("Walk", time(17, 0), priority=1),
        Task("Feed", time(8, 0), priority=1),
    ]

    scheduler.sort_by_time(original)

    # The caller's list is untouched (Walk still first).
    assert original[0].description == "Walk"


def test_completing_daily_task_creates_next_days_task():
    """Completing a daily task should add a new task for the following day."""
    scheduler = Scheduler()
    dog = Pet("Rex")
    today = date(2026, 7, 5)
    feed = Task(
        "Feed the dog", time(8, 0), priority=2, frequency="daily", scheduled_date=today
    )
    dog.add_task(feed)

    new_task = scheduler.complete_task(dog, feed)

    # Original is marked done; a fresh copy exists for tomorrow.
    assert feed.completed is True
    assert new_task is not None
    assert new_task.completed is False
    assert new_task.scheduled_date == today + timedelta(days=1)
    assert len(dog.tasks) == 2


def test_completing_one_off_task_creates_no_new_task():
    """A non-recurring task should be marked done without spawning a copy."""
    scheduler = Scheduler()
    dog = Pet("Rex")
    task = Task("Vet visit", time(9, 0), priority=1)  # frequency defaults to None
    dog.add_task(task)

    result = scheduler.complete_task(dog, task)

    assert result is None
    assert task.completed is True
    assert len(dog.tasks) == 1


def test_find_conflicts_flags_duplicate_times():
    """Two tasks in the same date+time slot should produce one warning."""
    scheduler = Scheduler()
    today = date(2026, 7, 5)
    dog_meds = Task("Dog meds", time(9, 0), priority=1, scheduled_date=today, pet_name="Rex")
    cat_vet = Task("Cat vet", time(9, 0), priority=1, scheduled_date=today, pet_name="Whiskers")

    warnings = scheduler.find_conflicts([dog_meds, cat_vet])

    assert len(warnings) == 1
    # Both clashing tasks are named in the warning.
    assert "Dog meds" in warnings[0]
    assert "Cat vet" in warnings[0]


def test_find_conflicts_returns_empty_when_no_clash():
    """Different times (or an empty list) should produce no warnings, no crash."""
    scheduler = Scheduler()
    today = date(2026, 7, 5)
    a = Task("A", time(8, 0), priority=1, scheduled_date=today)
    b = Task("B", time(9, 0), priority=1, scheduled_date=today)

    assert scheduler.find_conflicts([a, b]) == []
    assert scheduler.find_conflicts([]) == []
