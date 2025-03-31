---
layout: post
use_math: true
title: The Gurobi Cheatsheet for Integer Non-linear Programming Formulation 
---

Optimisation problems require translating real-life constraints and objectives into mathematical expressions that a solver, like Gurobi, can efficiently process. While Gurobi is a powerful optimisation engine, the key to harnessing its full potential is crafting well-structured models.
This article is a quick reference guide for beginners towards the essentials of ILP formulation. Also, it is a compilation of challenges I faced while formulating non-linear constraints on older Gurobi versions in the pre-ChatGPT era. This article attempts to understand how to decompose non-linear expressions into constituent linear expressions, which are expected to be utilized in tackling scheduling, resource allocation, or combinatorial optimisation problems.
We get started with the AND construct. This is for engineers who are stuck with an older Gurobi version which does not allow multiplication between variables. Additionally, it serves as a standard example of exacting a non-linear constraint from an approximate linear constraint.

**Binary AND**


We begin with the truth table of binary AND, and the plot of the same.

```
z = x.y
```

| x | y | z |
|--|--|--|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |  

![Image](/assets/Gurobi/figure1.png){: width="30%" align="center"}

*Figure 1: Points corresponding to (0,0), (0,1), and (1,0) are represented by red dots, indicating a value of 0 in the AND truth table. The point (1,1), is marks the output 1.*

Now, let's compare this with the binary XOR, which infact is a linear operation.

| x | y | z |
|--|--|--|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |  

With respect to the binary XOR, binary AND represents the shaded region.

![Image](/assets/Gurobi/figure2.png){: width="30%" align="center"}

*Figure 2: Line representing binary XOR equation passes through points (0,1), and (1,0). The shaded region represents feasibility for binary AND.*

The shaded region in Figure 2 is represented as,

```
\begin{equation}
z \geq x + y
\end{equation}
```

while the XOR operation is linear, defining the binary AND construct requires additional constraints due to its non-linear nature. Specifically, the fact that variables are binary implies that no single variable can exceed the values of the others involved in the operation. To accurately and completely define the AND construct in this case, we must introduce two supplementary constraints to bound the solution space effectively.

By visualizing these relationships and constraints through the image and understanding their mathematical underpinnings, we can appreciate the broader methodology of translating non-linear operations into piece-wise linear constraints. This approach is foundational in optimization problems where linear representations simplify computations and improve compatibility with certain solvers.
