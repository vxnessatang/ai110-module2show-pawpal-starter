from datetime import date

from pawpal_system import Owner, Pet, Task
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")

# Create the Owner once and keep it in the session "vault" so pets/tasks
# persist across reruns (Streamlit re-runs this script on every interaction).
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

owner: Owner = st.session_state.owner

# Priority label -> number (1 = top priority, matching the backend convention).
PRIORITY_MAP = {"High": 1, "Medium": 2, "Low": 3}

st.markdown("### Add a Pet")
col_p1, col_p2 = st.columns([3, 1])
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    st.write("")  # spacer to align the button with the input
    if st.button("Add pet"):
        owner.add_pet(Pet(pet_name))
        st.success(f"Added {pet_name}.")

if owner.pets:
    st.caption("Current pets: " + ", ".join(pet.name for pet in owner.pets))
else:
    st.info("No pets yet. Add one above before scheduling tasks.")

st.markdown("### Schedule a Task")
if owner.pets:
    col1, col2, col3 = st.columns(3)
    with col1:
        target_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        priority_label = st.selectbox("Priority", ["High", "Medium", "Low"])

    col4, col5, col6 = st.columns(3)
    with col4:
        task_date = st.date_input("Date", value=date.today())
    with col5:
        task_time = st.time_input("Time")
    with col6:
        frequency_label = st.selectbox("Repeats", ["One-off", "Daily", "Weekly"])

    if st.button("Add task"):
        target_pet = next(pet for pet in owner.pets if pet.name == target_pet_name)
        owner.schedule_task(
            target_pet,
            Task(
                task_title,
                task_time,
                PRIORITY_MAP[priority_label],
                frequency=None if frequency_label == "One-off" else frequency_label,
                scheduled_date=task_date,
            ),
        )
        st.success(f"Scheduled '{task_title}' for {target_pet_name}.")

scheduler = owner.scheduler
all_tasks = owner.get_all_tasks()

st.divider()
st.subheader("📋 Current Tasks")

if not all_tasks:
    st.info("No tasks yet. Add one above.")
else:
    # --- Conflict detection: surface clashes prominently before the list ---
    conflicts = scheduler.find_conflicts(all_tasks)
    if conflicts:
        st.warning(
            "**Scheduling conflict detected!** "
            "These tasks fall at the same date and time — you may not be able to do both:"
        )
        for warning in conflicts:
            # Strip the "WARNING - " prefix; Streamlit's icon already signals it.
            st.warning(warning.replace("WARNING - ", ""), icon="⚠️")
    else:
        st.success("No scheduling conflicts — you're all set! 🎉")

    # --- Filtering: let the owner narrow the list by pet and status ---
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pet_choice = st.selectbox(
            "Filter by pet", ["All pets"] + [pet.name for pet in owner.pets]
        )
    with col_f2:
        status_choice = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    pet_name = None if pet_choice == "All pets" else pet_choice
    completed = {"All": None, "Pending": False, "Completed": True}[status_choice]

    # Filter, then sort chronologically — both handled by the Scheduler.
    filtered = scheduler.filter_tasks(all_tasks, completed=completed, pet_name=pet_name)
    ordered = scheduler.sort_by_time(filtered)

    if ordered:
        st.table(
            [
                {
                    "Date": task.scheduled_date,
                    "Time": task.time.strftime("%H:%M"),
                    "Task": task.description,
                    "Pet": task.pet_name,
                    "Priority": task.priority,
                    "Repeats": task.frequency or "One-off",
                    "Status": "✅ Done" if task.completed else "⏳ To-do",
                }
                for task in ordered
            ]
        )
    else:
        st.caption("No tasks match the current filters.")

    # --- Recurring logic: complete a task; daily/weekly auto-reschedules ---
    st.markdown("#### Mark a task complete")
    pending = scheduler.sort_by_time(
        scheduler.filter_tasks(all_tasks, completed=False)
    )
    if pending:
        labels = {
            f"{t.scheduled_date} {t.time.strftime('%H:%M')} — {t.description} ({t.pet_name})": t
            for t in pending
        }
        choice = st.selectbox("Choose a pending task", list(labels))
        if st.button("Complete task"):
            task = labels[choice]
            pet = next(p for p in owner.pets if p.name == task.pet_name)
            new_task = scheduler.complete_task(pet, task)
            if new_task is not None:
                st.success(
                    f"Completed '{task.description}'. "
                    f"Next {task.frequency} occurrence scheduled for "
                    f"{new_task.scheduled_date}."
                )
            else:
                st.success(f"Completed '{task.description}'.")
            st.rerun()
    else:
        st.caption("Nothing pending — every task is done! 🎉")

st.divider()

st.subheader("Build Schedule")
st.caption("Calls Scheduler.make_plan() to order tasks by time, then priority.")

if st.button("Generate schedule"):
    plan = scheduler.make_plan(owner.pets)
    if plan:
        st.write(f"Today's plan for {owner.name}:")
        for task in plan:
            st.markdown(f"- **{task.time.strftime('%H:%M')}** - {task.description}")
    else:
        st.warning("No tasks to schedule yet. Add some tasks first.")
