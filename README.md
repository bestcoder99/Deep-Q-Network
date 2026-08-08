# Deep-Q-Network
# Agent World 🧠🌍

### What happens when 500 autonomous agents are dropped into a world with limited resources — and have to learn how to survive?

**Agent World** is a multi-agent reinforcement learning simulation where autonomous agents must make decisions about **work, food, energy, health, trade, and alliances** over a 1,200-day simulated environment.

There are no hard-coded instructions telling the learning agents when to work, when to rest, or when to buy food.

Instead, they experience the world, receive rewards and penalties from the consequences of their decisions, remember those experiences, and gradually learn a survival strategy using a **Deep Q-Network (DQN)**.

The project began as a simple agent-based survival simulation and evolved into an experiment in reinforcement learning, emergent economic behavior, and multi-agent interaction.

---

## The Idea

Imagine placing hundreds of agents into the same simulated world.

Every agent has a few basic resources:

* 💰 **Money**
* 🍎 **Food**
* ⚡ **Energy**
* ❤️ **Health**

Every simulated day, an agent has to decide what to do.

It can:

* **Work** to earn money
* **Rest** to recover
* **Buy food** to avoid starvation
* **Form alliances** with other agents

But every decision has consequences.

Working earns money but consumes food and energy.

Buying food improves survival but costs money.

Resting can preserve an agent but sacrifices the opportunity to earn.

Social interactions can create trusted relationships, trading opportunities, and alliances.

And poor decisions can eventually kill the agent.

The central question is simple:

> **Can an agent learn a survival strategy from experience instead of being explicitly programmed with one?**

---

# From Rules to Learning

Agent World contains rule-based strategies as well as an adaptive reinforcement-learning agent.

A manually designed strategy might contain logic such as:

```text
IF food is low:
    buy food

IF energy is low:
    rest

IF money is low:
    work
```

That works — but the intelligence belongs to the programmer.

The adaptive agent is different.

Instead of being told the correct action, it receives its current state:

```text
Money
Food
Energy
Health
```

and asks a neural network:

```text
How valuable would each possible action be from here?
```

The network produces Q-values:

```text
                Q-value

REST            8.31
WORK           14.72
BUY FOOD        4.19
ALLY            2.06
```

The agent can then choose the action with the highest estimated long-term value.

As the simulation continues, those estimates change.

The policy is **learned**, not written.

---

# Deep Q-Learning Architecture

The adaptive agents use a **Deep Q-Network (DQN)** to approximate the action-value function:

[
Q(s,a)
]

where:

* (s) = the agent's current state
* (a) = a possible action
* (Q(s,a)) = the expected long-term value of taking that action

The neural network maps:

```text
[ money, food, energy, health ]

              ↓

         Neural Network

              ↓

[ rest, work, buy_food, ally ]
```

Each output represents the predicted Q-value of an action.

This replaces the tabular Q-table used in traditional Q-learning.

Instead of memorizing the value of every discrete state-action pair, the network learns a function capable of **generalizing across states it has never seen before**.

---

# The Learning Loop

Every adaptive-agent interaction generates a transition:

```text
(state, action, reward, next_state, done)
```

For example:

```text
State
    Money: 20
    Food: 5
    Energy: 70
    Health: 8

Action
    WORK

Reward
    +25

Next State
    Money: 30
    Food: 4
    Energy: 60
    Health: 7.5

Done
    False
```

The experience is then stored and later used to train the network.

Conceptually:

```text
Current State
      │
      ▼
  Main DQN
      │
      ▼
   Q-values
      │
      ▼
ε-greedy action
      │
      ▼
 Environment
      │
      ├──── Reward
      │
      └──── Next State
               │
               ▼
         Replay Buffer
               │
        Random Mini-Batch
               │
        ┌──────┴──────┐
        ▼             ▼
    Main DQN      Target DQN
        │             │
 Predicted Q      Future Q
        │             │
        └──────┬──────┘
               ▼
             Loss
               │
               ▼
         Backpropagation
               │
               ▼
        Updated Main DQN
```

---

# Experience Replay

One of the major problems with reinforcement learning is that consecutive experiences are highly correlated.

An agent might experience:

```text
BUY FOOD
BUY FOOD
BUY FOOD
BUY FOOD
BUY FOOD
```

Training directly on each event in sequence can cause the network to overreact to whatever happened most recently.

Agent World therefore uses an **experience replay buffer**.

Each interaction is stored as:

```python
(state, action, reward, next_state, done)
```

Rather than learning only from the newest event, the DQN samples random mini-batches of past experiences.

For example:

```text
WORK
REST
BUY FOOD
WORK
ALLY
REST
...
```

A training step therefore represents many different situations simultaneously.

The network isn't asked:

> "How should I change because of this one experience?"

It is effectively asked:

> "What weight update best explains this diverse batch of experiences?"

This makes training substantially more stable.

---

# Mini-Batch Training

Experiences are sampled in batches of **64**.

For every batch, the network calculates:

```text
64 predicted Q-values
```

and:

```text
64 target Q-values
```

The loss between them is calculated and backpropagated through the neural network.

So instead of:

```text
Experience
    ↓
Update
```

training becomes:

```text
64 randomly sampled experiences
            ↓
     Predictions
            ↓
        Targets
            ↓
      Average Loss
            ↓
     Backpropagation
            ↓
      Weight Update
```

---

# Bellman Learning

The DQN learns using the Bellman target:

[
y = r + \gamma \max_{a'}Q(s',a')
]

where:

* (r) is the immediate reward
* (\gamma) controls the importance of future rewards
* (s') is the next state
* (Q(s',a')) estimates the value of future actions

This means an agent doesn't simply ask:

> **"Did this action help me right now?"**

It also asks:

> **"What kind of future did this action put me in?"**

That distinction is what allows reinforcement learning to discover multi-step strategies.

---

# Terminal States

Death is treated as a terminal transition.

When an agent dies, there is no future state from which it can collect additional reward.

The target therefore becomes:

[
y = r
]

instead of:

[
y = r + \gamma \max Q(s',a')
]

This prevents the network from assigning imaginary future value to a dead agent.

---

# Target Network

A subtle problem appears if the same neural network generates both:

1. the prediction being trained, and
2. the target it is trying to reach.

Every gradient update changes the network — which would also immediately change its own target.

It is like trying to hit a target that moves every time you take a shot.

Agent World therefore maintains two networks:

```text
Main DQN
    → learns continuously

Target DQN
    → remains temporarily frozen
```

The main network estimates:

[
Q(s,a)
]

while the target network estimates:

[
\max Q(s',a')
]

Periodically, the main network's learned weights are copied into the target network.

```text
Main DQN learns
      │
      │
      │  many updates
      ▼
copy weights
      │
      ▼
Target DQN
```

This gives the learning process a more stable target.

---

# Exploration vs Exploitation

If the agent always selected whichever action its initially random neural network preferred, it could become trapped in a terrible strategy.

Agent World therefore uses an **ε-greedy policy**.

Most of the time:

```text
Choose the action with the highest Q-value
```

But occasionally:

```text
Choose a random action
```

This creates the fundamental reinforcement-learning tradeoff:

### Exploitation

Use what the network currently believes is best.

### Exploration

Try something different and potentially discover a better strategy.

Without exploration, the agent cannot reliably discover alternatives to its existing behavior.

---

# One Brain, Hundreds of Lives

One of the more interesting aspects of Agent World is that adaptive agents contribute experiences to a **shared DQN**.

Think of each agent as a separate explorer of the environment:

```text
Agent 1 ─────┐
Agent 2 ─────┤
Agent 3 ─────┤
Agent 4 ─────┤
    ...      ├──► Replay Buffer ──► Shared DQN
Agent 500 ───┘
```

An individual agent may encounter only a small subset of possible situations.

But collectively, hundreds of agents can generate experiences involving different combinations of:

```text
wealth
hunger
energy
health
relationships
resource availability
```

The shared neural network learns from all of them.

An experience generated by one agent can therefore improve decisions made later for another agent.

---

# A 1,200-Day World

Each training episode can simulate up to:

```text
500 agents × 1,200 days
```

or potentially:

```text
600,000 agent-environment interactions
```

if every agent survives the full episode.

In practice, agents can die before Day 1,200, reducing the number of transitions generated.

Across multiple episodes, the environment resets while the DQN retains what it has learned.

Conceptually:

```text
Episode 1
500 new agents
      ↓
1,200 simulated days
      ↓
DQN learns
      ↓

Episode 2
500 new agents
      ↓
same DQN
      ↓
more experience
      ↓
DQN learns further

...

Episode N
```

This separates the **world** from the **learner**.

The population can disappear.

The learned policy survives.

---

# The Simulated Economy

Agent World is not only a survival environment.

Agents operate inside a primitive economy.

They can:

```text
WORK
 ↓
Money

Money
 ↓
Food

Food + Energy + Health
 ↓
Survival
```

Resources therefore have indirect value.

Money itself does not keep an agent alive.

Its usefulness comes from what the agent can eventually exchange it for.

This creates tradeoffs between accumulating wealth and maintaining the resources required for survival.

---

# Trading

Food is not always guaranteed to be available directly.

Agents can interact with other agents and exchange resources.

This introduces agent-to-agent dependencies that do not exist in traditional single-agent reinforcement-learning environments.

An action can now affect:

```text
the acting agent
+
another agent
+
future interactions
```

The environment consequently becomes partly shaped by the behavior of the population itself.

---

# Trust and Social Memory

Agents maintain information about previous interactions.

Repeated interaction can increase familiarity or trust between agents.

This creates the possibility of:

```text
strangers
   ↓
repeated interactions
   ↓
trusted agents
   ↓
trade
   ↓
alliances
```

Rather than treating every other agent as identical, the simulation can therefore contain persistent social relationships.

---

# Alliances

Agents can attempt to form alliances when certain social and resource conditions are satisfied.

Alliances add another layer to the survival problem:

> Is cooperation worth spending resources on?

An agent now has to balance immediate survival against potentially useful social relationships.

The action space is therefore not purely economic.

It includes a primitive form of **social decision-making**.

---

# Emergent Behavior

The interesting part of the simulation isn't any individual rule.

It's what happens when all the rules interact.

A seemingly sensible action can create unexpected downstream effects.

For example:

```text
Working more
    ↓
More money
    ↓
Greater ability to buy food

BUT

Working more
    ↓
Less energy
    ↓
Less food
    ↓
Lower health
    ↓
Potential death
```

Similarly:

```text
Saving money
```

may increase wealth while simultaneously making an agent less likely to spend resources necessary for survival.

The DQN has to discover these relationships through interaction.

This creates the possibility of emergent strategies that were never explicitly programmed.

---

# What Does "Success" Mean?

This is one of the hardest questions in reinforcement learning.

The DQN does not inherently understand concepts like:

```text
survival
wealth
health
cooperation
success
```

It understands only **reward**.

Therefore:

> **The reward function is effectively the objective of the artificial society.**

Rewarding wealth too aggressively may create rich but fragile agents.

Rewarding survival too aggressively may create extremely conservative agents.

Rewarding social interaction too aggressively may cause agents to waste resources forming relationships.

The simulation therefore doubles as an experiment in **reward engineering**.

Changing the reward function can change the behavior of the entire learned population.

---

# Measuring Learning

A falling neural-network loss alone does **not** prove that the agents are getting better.

Agent World can instead be evaluated using behavioral metrics such as:

### Survival

```text
Average survival time
Number of surviving agents after 1,200 days
Death rate
```

### Economy

```text
Average wealth
Maximum wealth
Minimum wealth
Wealth gap
Top wealth contribution
```

### Behavior

```text
WORK frequency
REST frequency
BUY FOOD frequency
ALLY frequency
```

### Social Dynamics

```text
Number of trades
Number of known-agent trades
Alliance formation
```

### Reinforcement Learning

```text
Episode reward
Training loss
Q-values
Exploration rate
```

The strongest test is eventually to freeze the trained network, disable exploration and learning, and compare its performance against an untrained or random policy.

---

# Current DQN Components

The reinforcement-learning implementation currently includes:

* Deep Q-Network
* Neural Q-function approximation
* Four-action output space
* ε-greedy exploration
* Experience replay
* Random mini-batch sampling
* Batch gradient descent
* Bellman targets
* Discounted future rewards
* Terminal-state handling
* Target network
* Periodic target synchronization
* Shared learning across multiple agents

---

# Tech Stack

**Language**

```text
Python
```

**Machine Learning**

```text
PyTorch
```

**Core concepts**

```text
Reinforcement Learning
Deep Q-Learning
Experience Replay
Target Networks
Multi-Agent Simulation
Agent-Based Modeling
Emergent Behavior
```

---

# Project Evolution

Agent World did not begin as a DQN.

The project evolved incrementally:

```text
Basic survival simulation
        ↓
Multiple agent personalities
        ↓
Economic interactions
        ↓
Trading
        ↓
Social memory
        ↓
Alliances
        ↓
Tabular Q-Learning
        ↓
Neural Q-function
        ↓
Deep Q-Network
        ↓
Experience Replay
        ↓
Target Network
        ↓
Multi-episode training
```

That evolution is important to the project.

Rather than treating reinforcement learning as a black-box library call, the goal was to understand why each component exists and what problem it solves.

A Q-table exposed the limitations of storing discrete state-action combinations.

A neural network introduced generalization.

Training on consecutive transitions introduced instability.

Experience replay addressed correlated data.

Using the same network to generate predictions and targets introduced another source of instability.

The target network addressed the moving-target problem.

Each component exists because the previous version exposed a limitation.

---

# Why Build This?

Most introductory machine-learning projects start with a static dataset:

```text
CSV
 ↓
model.fit()
 ↓
accuracy
```

Agent World takes a different approach.

There is no fixed dataset.

**The agents create the dataset by living.**

Every decision changes the environment.

Every consequence creates a new training example.

Every training example changes the neural network.

And the changed neural network alters future decisions.

```text
Agent behavior
      ↓
Environment changes
      ↓
Experiences generated
      ↓
Network learns
      ↓
Behavior changes
      ↓
Environment changes again
      ↓
...
```

The dataset, policy, and environment evolve together.

That feedback loop is what makes reinforcement learning fascinating.

---

# Questions This Project Can Explore

Agent World creates a sandbox for experiments such as:

* Does reinforcement learning outperform manually designed survival strategies?
* What survival policies emerge under resource scarcity?
* Does cooperation improve long-term survival?
* When does trading become preferable to direct resource acquisition?
* How does exploration affect mortality?
* What happens when the reward for wealth conflicts with the reward for survival?
* How does inequality evolve between autonomous agents?
* Can social relationships become strategically valuable?
* How does resource availability alter learned behavior?
* How robust is a learned policy to unfamiliar starting conditions?

The simulation is therefore less about producing one "perfect" agent and more about building an environment where these questions can actually be tested.

---

# Future Experiments

Possible extensions include:

### Double DQN

Reduce Q-value overestimation by separating action selection from target evaluation.

### Prioritized Experience Replay

Replay surprising or high-error experiences more frequently instead of sampling every transition uniformly.

### Dynamic Exploration

Decay ε as training progresses instead of maintaining a constant exploration probability.

### Model Persistence

Save trained weights and continue learning across independent program executions.

### Evaluation Mode

Freeze the trained network and evaluate it across many unseen worlds without gradient updates or exploration.

### Reward Ablation

Train identical networks under different reward structures and compare the societies that emerge.

### Resource Shocks

Introduce:

```text
famines
economic crashes
resource abundance
energy shortages
```

and test whether learned policies adapt.

### Population Experiments

Compare:

```text
100 agents
500 agents
1,000 agents
```

to investigate whether population size changes economic or social dynamics.

### Independent Brains

Instead of one shared DQN, give agents independent networks and investigate whether distinct learned personalities emerge.

### Multi-Agent Reinforcement Learning

Move from shared-policy DQN toward architectures explicitly designed for environments containing multiple simultaneously learning agents.

---

# The Bigger Idea

Agent World started with a very simple question:

> **Can I make a bot learn how to survive?**

But once multiple agents, scarce resources, money, trading, trust, alliances and reinforcement learning are placed inside the same environment, the question becomes more interesting:

> **What behavior emerges when artificial agents have resources to manage, other agents to interact with, and no explicit strategy beyond the incentives encoded in their world?**

There is no claim that this simulation models real human economies or societies.

It doesn't.

It is deliberately simplified.

But that simplicity is useful.

It creates a controllable sandbox where individual mechanisms can be changed and their consequences observed.

Change the rewards.

Change resource scarcity.

Change the available actions.

Change how agents interact.

Retrain.

Watch what happens.

That is the experiment.

---

## Status

🚧 **Active experiment**

The DQN architecture is implemented and the project is currently moving into systematic training, evaluation, reward-function tuning, and comparison against baseline strategies.

Results will be added as experiments are completed.

---

## Built From Scratch to Learn Reinforcement Learning

The primary purpose of Agent World is not to hide reinforcement learning behind abstractions.

It is to understand it.

From Q-values and Bellman targets to replay buffers, mini-batch gradient descent, neural-network weights, exploration, and target networks, the project was built incrementally to understand what each component actually contributes.

Because the interesting part isn't just getting an agent to learn.

It's understanding **why it learns at all.**

