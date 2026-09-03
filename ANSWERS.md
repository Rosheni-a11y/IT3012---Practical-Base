# Practical 01

## Task 1.1: The Environment State (`__init__`)

### 1. (Remember) List the four components of the PEAS framework discussed in Lecture 01.

- **Performance Measure (P)** – Defines how the success of the agent is evaluated.
- **Environment (E)** – The external world in which the agent operates.
- **Actuators (A)** – The mechanisms used by the agent to perform actions.
- **Sensors (S)** – The mechanisms used by the agent to perceive or gather information from the environment.

### 2. (Understand) Look at the `VisualGridHuntGame.__init__` method. Which specific variables in this code represent the physical "Environment (E)" state?

- The physical environment state is represented by `self.width`, `self.height`, `self.agent_pos`, `self.walls`, `self.food_positions`, and `self.opponents`.
- These variables describe the grid size and the positions of the agent, walls, food, and opponents in the environment.

### 3. (Analyze) Based on the variables initialized (specifically `self.opponents`), classify this baseline environment as "Single-Agent" or "Multi-Agent". Briefly justify your choice.

- The baseline environment is a **Multi-Agent environment** because `self.opponents` represents other agents that exist and act within the same environment as the main agent.

---

## Task 1.2: The Perception Subsystem (`get_percept`)

### 4. (Remember) Define what a "percept sequence" is according to Lecture 01.

- A percept sequence is the complete history of all percepts that an agent has received from the environment from the beginning up to the current time.

### 5. (Understand) Which component of the PEAS framework does the `get_percept()` method represent in our code?

- The `get_percept()` method represents the **Sensors (S)** component of the PEAS framework because it provides the agent with information about the current state of the environment.

### 6. (Evaluate) Based on the exact dictionary returned by `get_percept()`, is this environment "Fully Observable" or "Partially Observable"? Explain why based on what the agent can and cannot see.

- The environment is **Partially Observable** because `get_percept()` does not provide the agent with the complete environment state.
- For example, the agent knows the number of remaining food items but cannot see their exact positions, and it also does not receive the complete wall locations.

---

## Task 1.3: Action Execution (`execute_action`)

### 7. (Understand) When `execute_action()` deducts points for hitting a wall, which PEAS component is being actively updated?

- The **Performance Measure (P)** component is being updated because hitting a wall decreases `self.score` by 5 points, which affects how the agent's performance is evaluated.

### 8. (Evaluate) Why is it structurally important that this metric evaluates changes in the external environment state (hitting a wall) rather than the agent's internal processing effort?

- The performance measure should evaluate the agent based on the actual outcomes of its actions in the environment rather than its internal processing effort.
- This ensures that the agent is rewarded for achieving the desired results and penalized for undesirable outcomes such as hitting a wall.

---

## Part 2: Guided Modification & Deep Theory Mapping

### Step 2.1: Extending the Environment Initialization (`__init__`)

### 9. (Understand) If you successfully add `self.toxic_traps` to the environment but intentionally hide this data from the agent's sensors, how does this specifically alter the environment's "Observability" classification?

- The environment remains **Partially Observable** because the toxic trap locations are part of the environment state but are hidden from the agent's sensors.
- Therefore, the agent does not have complete information about the environment.

### Step 2.2: Updating the Perception Subsystem (`get_percept`)

### 10. (Analyze) By adding `smells_toxin`, you expand the agent's percept sequence. Explain how this specific sensor helps the agent act with "Rationality" (maximizing expected utility).

- The `smells_toxin` sensor helps the agent know when it is on a toxic trap.
- By getting this information, the agent can make better decisions and try to avoid the -15 score penalty.
- This helps the agent maximize its performance.

### Step 2.3: Modifying Action Execution & Visual Rendering (`execute_action` & `draw_grid`)

### 11. (Remember) You programmed a severe score penalty for stepping on a trap to avoid metric exploitation. What was the classic "Vacuum World Exploit" example discussed in Lecture 01 that illustrated the danger of faulty metrics?

- In the Vacuum World example, if the agent is rewarded every time it cleans dirt, it may make the area dirty again and clean it repeatedly just to get more rewards.
- This shows that a badly designed performance measure can make the agent behave in an unwanted way.

---
