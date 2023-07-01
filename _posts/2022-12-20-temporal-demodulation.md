---
layout: post
use_math: true
title: On envelope extraction using cross coherence
---

Temporal demodulation is a widely employed technique for signal characterisation. Here, I propose an envelope extraction method for periodic signals in the presence of ambient noise and overlapping signal and noise characteristics. The design of a filter without prior knowledge of the noise characteristics can be challenging. Given a clean template signal, cross-coherence can be used to score the signal purity against time.

Let $ r(t) $ of $ T $ second duration and a test signal $s(t)$ of any duration. We consider a window length $ w $ and hop-length $ h $. In this example, we will consider the heart sound signal. 
![Image](/assets/st.svg){: style="float: left" width="50%"}
*The heart sound signal is an approximately periodic signal, with each period consisting of at least two distinct sounds, namely the S1 and S2, consisting of systolic and diastolic movements of the heart.*

The window length is approximately one time period of the reference signal. Let $ t_{p_1}, t_{p_2}, t_{p_3}, ...  t_{p_N} $ be the timestamps corresponding to the S1 peaks of the reference signal. We select peaks with co-ordinates $ (t_{p_2}, p_2), ..., (t_{p_{N-1}}, p_{N-1}) $. The reference signal has a uniform period and consistently maintains the S1/S2 amplitudes. A standard peak detection algorithm detects these peaks on the squared-energy envelope. The signals are windowed. The complex-coherency of stationary signals $ r'(t) $ and $ s'(t) $

\begin{equation}
C_{r's'} = \frac{\phi_{r's'}}{\sqrt{\phi_{r'r'}\phi_{s's'}}}
\end{equation}

where  $ \phi_{r's'} $ is the cross-spectrum of the signals, $ \phi_{r'r'} $ and $ \phi_{s's'} $ are the respective PSDs. The Welch algorithm estimates the cross-spectrum algorithm. 

![Image](/assets/Envelope_comparisions.svg){:style="display:block; margin-left:auto; margin-right:auto"}
*Comparison of the cross-coherence feature against traditional envelope features for a normal PCG recording.*

![Image](/assets/Envelope_comparisions_408.svg){:style="display:block; margin-left:auto; margin-right:auto"}
*Comparison of the cross-coherence feature against traditional envelope features for a PCG with inconsistent sound amplitudes.*


```
    Input: Window length w, sampling frequency f_s.
    Output: C of dimension.
    Local: Length of signal l_s, hop-length h, number of frames N_w, filter length l_f.

    N_w ⟵Round(l_s/ h)
    s ⟵ PadZeros(s, (w/2, w/2))
    l_f ⟵ Round(0.03*f_s)
    n_s ⟵ Round(f_s/20)
    [t_pn] ⟵ ComputeReferenceFrame(r, w, h, l_f)
    C ⟵ Zeros((Round(N_w+1), n_s/2+1))
    for t_pn ∈ {t_p1,  ..., t_pN} 
        C' ⟵ Zeros((N_w+1), n_s/2+1)
        for t ∈ {t_pn - n, ..., t_pn + n}
           C_t ⟵ []
           for N ∈ {0, (N_w+1))
           r' ⟵ r[t*h-(w/2): t*h+(w/2)]
           s' ⟵ s[N*h: N*h+w]
           f, C_rs ⟵ Coherence(r', s', N_fft, n_s)
           C_xy ⟵ GaussianFilter1d(C_xy, sigma)
           C'_t ⟵ C_rs
           C'_t ⟵ Threshold(C_t', p)
           C' ⟵ C' + C'_t
        C \leftarrow C + Normalize(C')
     Return C 
```
  
