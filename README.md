# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
All tasks (sorted by time):
  2026-07-05 08:00 - Feed the dog (Woofington, DONE)
  2026-07-06 08:00 - Feed the dog (Woofington, TO-DO)
  2026-07-05 08:30 - Feed the cat (Whiskers, TO-DO)
  2026-07-05 09:00 - Give the dog medication (Woofington, TO-DO)
  2026-07-05 09:00 - Take the cat to the vet (Whiskers, TO-DO)
  2026-07-05 17:00 - Walk the dog (Woofington, TO-DO)

Pending only:
  2026-07-06 08:00 - Feed the dog (Woofington, TO-DO)
  2026-07-05 08:30 - Feed the cat (Whiskers, TO-DO)
  2026-07-05 09:00 - Give the dog medication (Woofington, TO-DO)
  2026-07-05 09:00 - Take the cat to the vet (Whiskers, TO-DO)
  2026-07-05 17:00 - Walk the dog (Woofington, TO-DO)

Completed only:
  2026-07-05 08:00 - Feed the dog (Woofington, DONE)

Woofington (dog):
  2026-07-05 08:00 - Feed the dog (Woofington, DONE)
  2026-07-06 08:00 - Feed the dog (Woofington, TO-DO)
  2026-07-05 09:00 - Give the dog medication (Woofington, TO-DO)
  2026-07-05 17:00 - Walk the dog (Woofington, TO-DO)

Whiskers (cat):
  2026-07-05 08:30 - Feed the cat (Whiskers, TO-DO)
  2026-07-05 09:00 - Take the cat to the vet (Whiskers, TO-DO)

Schedule conflicts:
WARNING - Conflict on 2026-07-05 at 09:00: Give the dog medication (Woofington), Take the cat to the vet (Whiskers)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

PawPal+ adds four "smarter scheduling" features on top of the core classes. Each is implemented on the `Scheduler` (with recurrence logic living on `Task`):

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns tasks earliest-first using `sorted()` with a `key=lambda t: t.time`. Since `Task.time` is a `datetime.time`, values compare chronologically directly. |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status (`completed=True/False`) and/or by pet (`pet_name=...`). Both filters are optional and stack; passing none returns everything. |
| Conflict handling | `Scheduler.find_conflicts()` | Groups tasks by their exact `(scheduled_date, time)` slot; any slot with more than one pending task yields a warning string (naming each task and its pet). Returns warnings instead of raising, so the program never crashes. Detects both same-pet and cross-pet clashes. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | `complete_task()` marks a task done and, if it recurs, auto-schedules the next instance on the same pet. `next_occurrence()` clones the task with `timedelta(days=1)` (daily) or `timedelta(weeks=1)` (weekly) to advance `scheduled_date` accurately across month/year boundaries. |

### Sample output

```
Schedule conflicts:
WARNING - Conflict on 2026-07-05 at 09:00: Give the dog medication (Woofington), Take the cat to the vet (Whiskers)
```

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
