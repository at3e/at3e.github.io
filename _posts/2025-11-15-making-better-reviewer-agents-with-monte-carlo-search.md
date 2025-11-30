---
layout: post
use_math: true
title: Creating better reviewer agents with Monte Carlo search algorithm
---


AI agents are everywhere, and this blog post aims to keep up with the trend. In the software industry, Large Language Models are increasingly being used as code reviewers, QA assistants, and autonomous agents inside multi-step workflows. Here, we look at a coder–reviewer use case workflow.
The pipeline retrieves context with RAG, the Planner breaks the task into executable steps, the Coder generates or updates code for each step, and the Reviewer evaluates outputs for correctness and quality. The Reviewer then delegates the next iteration to the Coder. Below is the flow diagram. In this post, we address the issue of LLM inconsistency at the code review stage.
![Image](/assets/agents/agents-image.001.png){: width="50%" align="center"}

First, I build a local version of this multi-agent code review engine. Please refer to the notebook that I made [here](https://colab.research.google.com/drive/1KvAOeGH-7LaPmkjPHA5d0Fc6tG9JR8kn#scrollTo=788294e1-161a-477e-8081-166b9071b36c) for a basic structure of a multi-agent coder and reviewer. Let's begin with what MCTS is.

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
        # average value
        return self.value_sum / self.visits if self.visits > 0 else 0.0

    def best_child(self, c_param=1.4):
        """Select child with highest UCB score."""
        scores = []
        for child in self.children:
            if child.visits == 0:
                score = float("inf")  # force exploration
            else:
                exploit = child.value()
                explore = c_param * math.sqrt(math.log(self.visits) / child.visits)
                score = exploit + explore
            scores.append(score)

        # argmax
        best_index = max(range(len(scores)), key=lambda i: scores[i])
        return self.children[best_index]
```

**The MCTS Class**

The MCTS class implements the search algorithm that comprises of four step cycle. 

**1.🔎 Selection**

This is where the agent decides where to go next in its current knowledge map (the game tree). It needs to know: should I stick with a move that’s been winning (Exploitation), or try something new that might be even better (Exploration)?MCTS uses the Upper Confidence Bound for Trees (UCT) formula to make this calculated gamble:

$$UCB = Q + c \cdot \sqrt{\frac{\ln(N)}{n}}$$

**2.🦚 Expansion: Adding New Knowledge**
Once the algorithm reaches a new, unanalyzed state (the selected child node), we need to add it to the search tree. The agent expands the tree by creating one or more new child nodes representing possible next moves from this state. This officially adds a new path to the agent's permanent memory structure for future search attempts.




