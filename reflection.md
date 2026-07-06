# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

Owner has a pet. Scheduler has a task.

- What classes did you include, and what responsibilities did you assign to each?

1. Pet (Attributes: name, hunger, health; Methods: eat, walk)
2. Owner (Attibutes: name, owns pet; Methods: add pet, schedule a walk, see today's tasks)
3. Task (Attributes: task description, time, priority, completed; Methods: check off task)
4. Scheduler (Attributes: none; Methods: schedule task, get all tasks, make plan)

**b. Design changes**

- Did your design change during implementation?

Yes

- If yes, describe at least one change and why you made it.

Time is now datetime.time to make comparing them more reliable than if they were strings. Owner now has a scheduler field so its methods can delegate to it. Pet now holds a list of tasks that can be added to. Task now has a pet name field so it's easy to tell which pet the task belongs to.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers time and priority.

- How did you decide which constraints mattered most?

Since the user wouldn't want tasks overlapping with each other, I thought time would be the constraint that mattered the most. Priority also seemed important because the user may schedule tasks that would be good to do but aren't as important as other tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff the scheduler makes is sacrificing preference for time and priority. The tradeoff is reasonable for this scenario because it is a basic scheduler, and the user can set the priority for the tasks based on their preferences when they add the task.

Another tradeoff is in the scheduler's conflict detection. find_conflicts() only flags tasks that share the exact same date and time rather than accounting for overlapping durations. Two tasks scheduled a minute apart won't be flagged because the tasks have no durations to overlap. This tradeoff is reasonable for a basic scheduler because the user can determine how much time tasks would realistically take when scheduling them and they would still receive a warning if they aaccidentally scheduled tasks for the same time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI to help me refine my initial design and corresponding UML diagram. It was also useful for debugging and refactoring my code.

- What kinds of prompts or questions were most helpful?

Prompts that provided detailed and specific context were the most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

One moment where I did not accept an AI suggestion as-is is when it suggested to turn my schedule_task() method into schedule_walk() instead. I did not accept this because that was not the direction I was going for in my design.

- How did you evaluate or verify what the AI suggested?

I visualized the new suggestions in a UML diagram and noticed this particular change. I reflected on what I wanted in the design and decided against it. Walking a pet can be a task but not all tasks will be walking.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
