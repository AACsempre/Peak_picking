#Input data to peak_picking.py

filepath = 'test_data.csv'
h_cor = 3       # Do not consider first h_vor rows (Header)
Freq = 100      # Sample Frequency [Hz]
freq_r_L = 0.2  # Frequency range Low value [Hz]
freq_r_H = 10   # Frequency range High value [Hz]
dist = 4        # Min distance between npeaks - samples between neighbouring peaks (dist * Freq / n = interval_Hz)
limit_frq = 10  # Maximum amount of frequencies to present