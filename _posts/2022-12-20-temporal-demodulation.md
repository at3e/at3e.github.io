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

![Image](/assets/Envelope_comparisions.svg){:style="display:block; margin-left:auto; margin-right:auto"}
*Comparison of the cross-coherence feature against traditional envelope features for a normal PCG recording.*

![Image](/assets/Envelope_comparisions_408.svg){:style="display:block; margin-left:auto; margin-right:auto"}
*Comparison of the cross-coherence feature against traditional envelope features for a PCG with inconsistent sound amplitudes.*

where  $ \phi_{r's'} $ is the cross-spectrum of the signals, $ \phi_{r'r'} $ and $ \phi_{s's'} $ are the respective PSDs. The Welch algorithm estimates the cross-spectrum algorithm. 

```
    **Input**: Window length w, sampling frequency f_s.
    Output: C of dimension.
    Local: Length of signal l_s, hop-length h, number of frames N_w, filter length l_f
           N_w → (l_s/ h)
    \STATE $s \leftarrow \textsc{PadZeros}(s, (w/2, w/2)) $ \\
    \STATE $l_f \leftarrow \textsc{round}(0.03*f_s) $ \\
    \STATE $n_s \leftarrow \textsc{round}(f_s/20) $ \\
    \STATE $ [t_{p_n}] \leftarrow \textsc{ComputeReferenceFrame}(r, w, h, l_f) $ \\
    \STATE $ C \leftarrow \textsc{zeros}((\textsc{round}(N_w+1), n_s/2+1)) $ \\
    \STATE $ \textbf{for} \hspace{0.5em} t_{p_n} \in \{ t_{p_2}, t_{p_{N-1}} \} $ \\
    \STATE \quad $C' \leftarrow \textsc{zeros}((\textsc{round}(N_w+1), n_s/2+1))$ \\
    \STATE \quad $ \textbf{for} \hspace{0.5em} t \in [t_{p_n}-n, t_{p_n}+n] $ \\
    \STATE \qquad $ C_t \leftarrow \{ \} $ \\
    \STATE \qquad $ \textbf{for} \hspace{0.5em} N \in [0, \textsc{round}(N_w+1)) $ \\
    \STATE \quad \qquad $ r' = r[t*h-(w/2): t*h+(w/2)]  $ \\
    \STATE \quad \qquad $ s' = s[N*h: N*h+w] $ \\
    \STATE \quad \qquad $ f, C_{rs} = \textsc{Coherence}(r', s', N_{\text{fft}}, n_s) $ \\
    \STATE \quad \qquad $ C_{xy} = \textsc{GaussianFilter1d}(C_{xy}, \sigma) $ \\
    \STATE \quad \qquad $ C'_t \leftarrow C_{rs} $ \\
    \STATE \quad \qquad $ C'_t \leftarrow \textsc{Threshold}(C_t', p) $ \\
    \STATE \quad \qquad $ C' \leftarrow C' + C'_t $ \\
    \STATE \qquad $ C \leftarrow C + \textsc{Normalize}(C')$ \\
    \STATE \textbf{Return} C 
```
  
