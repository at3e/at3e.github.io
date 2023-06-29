---
layout: post
use_math: true
title: On signal characterization using cross coherence
---

Temporal demodulation is a widely employed technique for signal characterization. Here, I propose an envelope extraction method for periodic signals in the presence of ambient noise when the signal and noise characteristics overlap. The design of a filter without prior knowledge of the noise characteristics can be challenging. Given a clean template signal, cross-coherence can be used to score the signal purity against time.

Let $ r(t) $ of $ T $ second duration and a test signal $s(t)$ of any duration. We consider a window length $w$ and hop-length $ h $. The window length is approximately one time period of the reference signal. Let $ t_{p_1}, t_{p_2}, t_{p_3}, ...  t_{p_N} $ be the timestamps corresponding to the S1 peaks of the reference signal. We select peaks with co-ordinates $ (t_{p_2}, p_2), ..., (t_{p_{N-1}}, p_{N-1}) $. The reference signal has a uniform period and consistently maintains the S1/S2 amplitudes. A standard peak detection algorithm detects these peaks on the squared-energy envelope. The signals are windowed. The complex-coherency of stationary signals $ r'(t) $ and $ s'(t) $

\begin{equation}
C_{r's'} = \frac{\phi_{r's'}}{\sqrt{\phi_{r'r'}\phi_{s's'}}}
\end{equation}

![Image](/assets/Envelope_comparisions.eps){: style="float: left"}
![Image](/assets/Envelope_comparisions_408.eps){: style="float: right"}

where  $ \phi_{r's'} $ is the cross-spectrum of the signals, $ \phi_{r'r'} $ and $ \phi_{s's'} $ are the respective PSDs. The Welch algorithm estimates the cross-spectrum algorithm. 
