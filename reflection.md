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

Time is now datetime.time to make comparing them more reliable than if they were strings. Owner now has a scheduler field so its methods can delegate to it. Pet now also holds a list of tasks that can be added to.

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

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
