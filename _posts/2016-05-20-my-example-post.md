---
layout: post
---

Temporal demodulation is a widely employed technique for signal characterization. Here, I propose an envelope extraction method for periodic signals in presence of ambient noise when the signal and noise characteristics overlap. The design of a filter without prior knowledge of the noise characteristics can prove to be a challenging task. Given a clean template signal, cross coherence can be used to score the signal purity against time.

Let $r(t)$  of $T$ second duration and a test signal $s(t)$ of any duration. We consider a window length $w$ and hop-length $h$. The window length is approximately one time period of the reference signal. Let $t_{p_1}, t_{p_2}, t_{p_3}, ...  t_{p_N}$ be the timestamps corresponding to the S1 peaks of the reference signal. We select peaks with co-ordinates $\{ (t_{p_2}, p_2), ..., (t_{p_{N-1}}, p_{N-1}) \}$. The reference signal has uniform period and consistently maintains the S1/S2 amplitudes. A standard peak detection algorithm detects these peaks on the squared-energy envelope. The signals are windowed. The complex-coherency of stationary signals $r'(t)$ and $s'(t)$

{% include mathjs %}
\{ (t_{p_2}, p_2), ..., (t_{p_{N-1}}, p_{N-1}) \}
{% endinclude %}

{% comment %}
Might you have an include in your theme? Why not try it here!
{% include my-themes-great-include.html %}
{% endcomment %}

No laudem altera adolescens has, volumus lucilius eum no. Eam ei nulla audiam efficiantur. Suas affert per no, ei tale nibh sea. Sea ne magna harum, in denique scriptorem sea, cetero alienum tibique ei eos. Labores persequeris referrentur eos ei.
