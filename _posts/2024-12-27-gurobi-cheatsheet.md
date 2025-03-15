---
layout: post
use_math: true
title: The Gurobi Cheatsheet for Integer Non-linear Programming Formulation 
---

Optimisation problems require translating real-life constraints and objectives into mathematical expressions that a solver, like Gurobi, can efficiently process. While Gurobi is a powerful optimisation engine, the key to harnessing its full potential is crafting well-structured models.
This article is a quick reference guide for beginners towards the essentials of ILP formulation. Also, it is a compilation of challenges I faced while formulating non-linear constraints on older Gurobi versions in the pre-ChatGPT era. This article attempts to understand how to decompose non-linear expressions into constituent linear expressions, which are expected to be utilized in tackling scheduling, resource allocation, or combinatorial optimisation problems.
We get started with the AND construct. This is for engineers who are stuck with an older Gurobi version which does not allow multiplication between variables. Additionally, it serves as a standard example of exacting a non-linear constraint from an approximate linear constraint.

We begin with the truth table of binary AND. 

<table class="center">
 {% for row in site.data.authors %}
    {% if forloop.first %}
    <tr>
      {% for pair in row %}
        <th>{{ pair[0] }}</th>
      {% endfor %}
    </tr>
    {% endif %}

    {% tablerow pair in row %}
      {{ pair[1] }}
    {% endtablerow %}
  {% endfor %}
</table>


Now, let's compare this with the binary XOR, which infact is a linear operation.

