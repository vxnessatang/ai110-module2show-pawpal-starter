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
PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}

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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        target_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        task_time = st.time_input("Time")
    with col4:
        priority_label = st.selectbox("Priority", ["high", "medium", "low"])

    if st.button("Add task"):
        target_pet = next(pet for pet in owner.pets if pet.name == target_pet_name)
        owner.schedule_task(
            target_pet,
            Task(task_title, task_time, PRIORITY_MAP[priority_label]),
        )
        st.success(f"Scheduled '{task_title}' for {target_pet_name}.")

tasks = owner.get_all_tasks()
if tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "time": task.time.strftime("%H:%M"),
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
            }
            for task in tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Calls Scheduler.make_plan() to order tasks by time, then priority.")

if st.button("Generate schedule"):
    plan = owner.scheduler.make_plan(owner.pets)
    if plan:
        st.write(f"Today's plan for {owner.name}:")
        for task in plan:
            st.markdown(f"- **{task.time.strftime('%H:%M')}** — {task.description}")
    else:
        st.warning("No tasks to schedule yet. Add some tasks first.")
