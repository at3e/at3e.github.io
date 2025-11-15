---
layout: post
use_math: true
title: Creating better reviewer agents with Monte Carlo search algorithm
---


AI agents are everywhere. This blog post is to keep up with the trend. In the software industry, Large Language Models are increasingly being used as code reviewers, QA assistants, and autonomous agents inside multi-step workflows. Here, we look  at a coder-reviewer usecase workflow, 
The pipeline retrieves context with RAG, the Planner breaks the task into executable steps, the Coder generates or updates code for each step, and the Reviewer evaluates outputs for correctness and quality. The reviewer then delagtes the next iteration to the coder. Below is the flow diagram.  In this post, we try to answer the problem of the llm inconsistency problem at the code review stage. 
![Image](/assets/agents/agents-image.001.png){: width="30%" align="center"}
