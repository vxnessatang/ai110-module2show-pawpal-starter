from datetime import time

from pawpal_system import Owner, Pet, Task

owner = Owner("John Doe")

dog = Pet("Woofington")
cat = Pet("Whiskers")
owner.add_pet(dog)
owner.add_pet(cat)

feed_dog = Task("Feed the dog", time(8, 0), priority=2)
feed_cat = Task("Feed the cat", time(8, 30), priority=2)
give_dog_meds = Task("Give the dog medication", time(9, 0), priority=1)

owner.schedule_task(dog, feed_dog)
owner.schedule_task(cat, feed_cat)
owner.schedule_task(dog, give_dog_meds)

print("Today's Schedule:")
for task in sorted(owner.get_all_tasks(), key=lambda t: t.time):
    print(f"  {task.time.strftime('%H:%M')} - {task.description}")
