from datetime import date, time

from pawpal_system import Owner, Pet, Task

owner = Owner("John Doe")
dog = Pet("Woofington")
cat = Pet("Whiskers")
owner.add_pet(dog)
owner.add_pet(cat)

today = date.today()
walk_dog = Task("Walk the dog", time(17, 0), priority=3, frequency="daily", scheduled_date=today)
feed_cat = Task("Feed the cat", time(8, 30), priority=2, frequency="daily", scheduled_date=today)
give_dog_meds = Task("Give the dog medication", time(9, 0), priority=1, frequency="weekly", scheduled_date=today)
feed_dog = Task("Feed the dog", time(8, 0), priority=2, frequency="daily", scheduled_date=today)
cat_vet = Task("Take the cat to the vet", time(9, 0), priority=1, scheduled_date=today)

scheduler = owner.scheduler
owner.schedule_task(dog, walk_dog)
owner.schedule_task(cat, feed_cat)
owner.schedule_task(dog, give_dog_meds)
owner.schedule_task(dog, feed_dog)
owner.schedule_task(cat, cat_vet)

scheduler.complete_task(dog, feed_dog)

def show(title: str, **filters) -> None:
    print(title)
    for t in scheduler.sort_by_time(scheduler.filter_tasks(owner.get_all_tasks(), **filters)):
        status = "DONE" if t.completed else "TO-DO"
        print(f"  {t.scheduled_date} {t.time.strftime('%H:%M')} - {t.description} ({t.pet_name}, {status})")
    print()

show("All tasks (sorted by time):")
show("Pending only:", completed=False)
show("Completed only:", completed=True)
show("Woofington (dog):", pet_name="Woofington")
show("Whiskers (cat):", pet_name="Whiskers")

print("Schedule conflicts:")
conflicts = scheduler.find_conflicts(owner.get_all_tasks())
if conflicts:
    for warning in conflicts:
        print(f"{warning}")
else:
    print("None - you're all set!")
