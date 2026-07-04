import sys
from datetime import time
from pathlib import Path

# Make the project root importable so `pawpal_system` resolves from tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Task


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
