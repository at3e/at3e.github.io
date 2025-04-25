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
z = x⋅y
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
z ≥ x + y - 1 
```

while the XOR operation is linear, defining the binary AND construct requires additional constraints due to its non-linear nature. The variables x,y and z are binary, so no single variable can exceed the values of the others. To accurately and completely define the binary AND construct in this case, two additional constraints bound the solution space to contain the point (1,1) only.

```
z ≤ x
z ≤ y
```
The corresponding visualization is,

![Image](/assets/Gurobi/figure3.png){: width="30%" align="center"}

*Figure 3: The final solution space.*


The idea is extended for multiplication between a binary variable and an integer/continuous variable. Let `x` be a continuous/integer variable with a known upper bound `U`, and `y` be a binary variable. `z` is their product.
These are the constraints that work,
```
z <= U⋅y
z <= x
z >= x - U⋅(1 - y)
```
The last equation is an example of the if-else construct, explained next.

**If-else**

Gurobi’s Python API does not provide an inbuilt if-else construct. But the if-else constraint can be decomposed into linear constraints using auxiliary variables. Let us take up a simple case:  

\begin{equation} 
b =
\begin{cases} 
1, & \text{if } x < y \\
0, & \text{otherwise}
\end{cases}
\end{equation}

Here, we use what is called the big-M constraint.
Let 


To prove the same by proof by contradiction,

Let , and , it is easy to check that LHS is greater than zero, while RHS is not. Similarly, assuming  can disprove the same. 





