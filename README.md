# Peak_picking
Peak picking technique for basic frequency domain<br>
<br>
Given a set of accelerograms, this script makes signal processing for the frequency domain using the Fast Fourier Transform (FFT).<br>
Then, an algorithm is used to pick the frequency peaks, provided they are not too close to each other. Peaks are selected according to their magnitude, in descending steps.<br>

The FFT transformation and peak search makes use of the python scipy library.<br>

The input data file consists of a csv file. Each column corresponds to an accelerogram. The first rows might correspond to a header, whcih can be ignored.<br>
The input variables are contained in the inputs.py file.<br>
    - filepath: 'test_data.csv'<br>
    - h_cor: Do not consider first h_vor rows (Header)<br>
    - Freq: Sample Frequency [Hz]<br>
    - freq_r_L: Frequency range Low value [Hz]<br>
    - freq_r_H: Frequency range High value [Hz]<br>
    - dist: Minimun distance between peaks - samples between neighbouring peaks<br>
    - limit_frq: Maximum amount of frequencies to present<br>

The output file is a table saved in a csv file. Each  column contains the main peaks obtained from the Peak picking technique.<br> 
