---
layout: post
use_math: true
title: Creating better reviewer agents with Monte Carlo search algorithm
---


AI agents are everywhere, and this blog post aims to keep up with the trend. In the software industry, Large Language Models are increasingly being used as code reviewers, QA assistants, and autonomous agents inside multi-step workflows. Here, we look at a coder–reviewer use case workflow.
The pipeline retrieves context with RAG, the Planner breaks the task into executable steps, the Coder generates or updates code for each step, and the Reviewer evaluates outputs for correctness and quality. The Reviewer then delegates the next iteration to the Coder. Below is the flow diagram. In this post, we address the issue of LLM inconsistency at the code review stage.
![Image](/assets/agents/agents-image.001.png){: width="30%" align="center"}

First, I build a local version of this multi-agent code review engine. Please refer to the notebook that I made [here](https://colab.research.google.com/drive/1KvAOeGH-7LaPmkjPHA5d0Fc6tG9JR8kn#scrollTo=788294e1-161a-477e-8081-166b9071b36c) for a basic structure of a multi-agent coder and reviewer. Let's begin with what MCTS is.

**Monte Carlo Tree Search**
The MCTS is a search algorithm that incorporates randomised search to a tree structure and used in decision making.
