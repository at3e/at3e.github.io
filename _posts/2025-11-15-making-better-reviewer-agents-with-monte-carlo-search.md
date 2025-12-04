---
layout: post
use_math: true
title: Creating better reviewer agents with Monte Carlo search algorithm
---


AI agents are everywhere, and this blog post aims to keep up with the trend. In the software industry, Large Language Models (LLMs) are increasingly being used as code reviewers, QA assistants, and autonomous agents in multi-step workflows. At the heart of these agents lie LLMs with exceptional reasoning abilities. There are several techniques for enhancing LLM reasoning, including prompting-based methods (e.g., Chain-of-Thought), agent-based approaches (e.g., Reason + Act—the foundation of LangChain and LangGraph), and retrieval-based strategies (e.g. RAG combined with reasoning).

In this post, we focus on a coder–reviewer workflow and demonstrate how a search algorithm can serve as a tool for the reviewer LLM.

The multi-agent code review pipeline operates as follows: the code repository context is retrieved using RAG, the Planner agent breaks the task into executable steps, the Coder generates or updates code for each step, and the Reviewer evaluates the outputs for correctness and quality. The Reviewer then delegates the next iteration back to the Coder. Below is the flow diagram:
![Image](/assets/agents/agents-image.001.png){: width="50%" align="center"}

First, I build a local version of this multi-agent code review engine. Please refer to the notebook I created [here](https://colab.research.google.com/drive/1KvAOeGH-7LaPmkjPHA5d0Fc6tG9JR8kn#scrollTo=788294e1-161a-477e-8081-166b9071b36c) for a basic structure of a multi-agent coder and reviewer. Our goal is to build a tool for the reviewer agent that implements the Monte Carlo Tree Search (MCTS) algorithm. MCTS adds structure to the LLM’s decision-making search space.

Let’s begin with a brief introduction to MCTS.

**Monte Carlo Tree Search**

The MCTS is a search algorithm that incorporates randomised search to a tree structure and used in decision making.

Let's first build the MCTS class and construct a wrapper for the reviewer to ingest.

**The MCTS Node**

The node is the fundamental building block of the MCTS search tree. Each node captures the state and  metadata, its parent node, the action that led to it, its children, accumulated value, and more. The `is_expanded` checks whether all possible actions from this state have already been explored. The `value` method computes the state value (average rewrd). The `best_child` method selects the child node with the highest Upper Confidence Bound (UCB) score (more on UCB [here](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)).

```
import math
import random

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.action = move  # action taken from parent to reach this node
        self.children = []
        self.max_children = 5
        self.visits = 0
        self.value_sum = 0.0  # cumulative reward

    def is_expanded(self):
        return len(self.children) >= self.max_children

    def value(self):
        return self.value_sum / self.visits if self.visits > 0 else 0.0

    def best_child(self, c_param=1.4):
        scores = []
        for child in self.children:
            if child.visits == 0:
                score = float("inf")
            else:
                exploit = child.value()
                explore = c_param * math.sqrt(math.log(self.visits) / child.visits)
                score = exploit + explore
            scores.append(score)
        best_index = max(range(len(scores)), key=lambda i: scores[i])
        return self.children[best_index]
```

**The MCTS Class**

The MCTS class implements the search algorithm that comprises of four step cycle. 

**1.🔎 Selection**

This is where the agent decides where to go next in its current knowledge map (the game tree). It needs to know: should I stick with a move that’s been winning (Exploitation), or try something new that might be even better (Exploration)?MCTS uses the Upper Confidence Bound for Trees (UCT) formula to make this calculated gamble:

$$UCB = Q + c \cdot \sqrt{\frac{\ln(N)}{n}}$$

**2.🦚 Expansion**

Once the algorithm reaches a new, unanalyzed state (the selected child node), we need to add it to the search tree. The agent expands the tree by creating one or more new child nodes representing possible next moves from this state. This officially adds a new path to the agent's permanent memory structure for future search attempts.

**3. 🎲 Simulation**

Once a new node is added, instead of searching perfectly, the MCTS performs a Simulation or "Rollout".
Starting from the newly expanded node, the agent plays a quick, often random or heuristic-guided game to the very end (terminal state). This gives a rapid, initial estimate of the node's value.

**4. ⬆️ Backpropagation**

The final, crucial step is learning. The result of the Simulation (the reward, win/loss) is propagated back up the search tree, from the newly created node all the way back to the root node.As the result passes through each parent node, two things are updated:Visit Count: How many times this move/state has been analyzed.Value Sum: The total reward/score gathered from all simulations through this node.This update directly affects the $Q$ (Exploitation) score for future searches, ensuring that moves leading to great outcomes become higher priority in the next Selection phase.MCTS is a constant cycle: Select $\to$ Expand $\to$ Simulate $\to$ Backpropagate. It continually refines its map, becoming smarter and more confident with every iteration.

```
class MCTS:
    def __init__(self, root_state, iterations=1000):
        self.root = Node(root_state)
        self.iter = iterations

    def search(self):
        root = self.root
        for i in range(self.iter):
            node = self.select(root)
            if not node.state.is_terminal():
                node = self.expand(node)
            result = self.simulate(node.state)
            self.backpropagate(node, result)
        return root.best_child(c_param=0).action

    def select(self, node):
        while not node.state.is_terminal() and node.is_expanded():
            node = node.best_child(c_param=1.4)
        return node

    def expand(self, node):
        actions = node.state.get_legal_actions()
        for action in actions:
            if len(node.children) < node.max_children:
                new_state = node.state.apply_action(action)
                new_node = Node(new_state, parent=node, move=action)
                node.children.append(new_node)
                return new_node
        return node

    def simulate(self, state):
        current_state = state
        depth = 0
        max_depth = 10
        while not current_state.is_terminal() and depth < max_depth:
            actions = current_state.get_legal_actions()
            if not actions:
                break
            action = random.choice(actions)
            current_state = current_state.apply_action(action)
            depth += 1
        return current_state.get_reward()

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value_sum += reward
            node = node.parent

```


**Langchain Tools**

In LangChain, a tool is simply a Python function wrapped with metadata(prompts and docstrings) that makes it callable by an agent. Tools give agents the ability to perform actions—such as running code, querying a database, calling an API, searching documents, or executing a planner like MCTS—rather than relying solely on text generation. A key detail is that the agent decides which tool to call based on the tool’s docstring metioned in the tool's definition. When the agent receives a task, it reads these docstrings and selects the appropriate tool by matching the task description to the tool capabilities. 

At runtime, the agent follows a cycle like this:

- Interpret the user’s request.
- Look at the available tools and read their docstrings.
- Decide which tool (if any) is relevant.
- Call the tool with the required inputs.
- Use the tool’s output to proceed to the next reasoning step.

There are different ways to create Langchain tools. Here, I use the `@tool` decorator. Here's the basic template.

```
@tool("function_name")
def function_name(args) -> return_type:
    """Function docstring"""

    # Function definition 
    
    return output
```
