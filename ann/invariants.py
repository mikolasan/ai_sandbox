# Reimport necessary libraries since environment was reset
import numpy as np
import matplotlib.pyplot as plt

# Random
#np.random.seed(42)  # For reproducibility
#signal_2d = np.random.randint(0, 11, size=(8, 8))


# Create two 8x8 matrices: one with a horizontal line at the top, and one with a line at the bottom
line_top = np.zeros((8, 8), dtype=int)
line_bottom = np.zeros((8, 8), dtype=int)

# Horizontal line at the top (first row filled with 1s)
line_top[0, :] = 1

# Horizontal line at the bottom (last row filled with 1s)
line_bottom[1, :] = 1

# Compute the 2D Fourier Transform for both matrices
dft_top = np.fft.fft2(line_top)
dft_bottom = np.fft.fft2(line_bottom)

# Shift the zero frequency component to the center
dft_top_shifted = np.fft.fftshift(dft_top)
dft_bottom_shifted = np.fft.fftshift(dft_bottom)

# Calculate the magnitude spectrum for both
magnitude_spectrum_top = np.abs(dft_top_shifted)
magnitude_spectrum_bottom = np.abs(dft_bottom_shifted)

# Plot both signals and their magnitude spectrums
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Original signals
axs[0, 0].imshow(line_top)
axs[0, 0].set_title('Line at Top (Original)')
axs[0, 0].set_xticks([])
axs[0, 0].set_yticks([])

axs[1, 0].imshow(line_bottom)
axs[1, 0].set_title('Line at Bottom (Original)')
axs[1, 0].set_xticks([])
axs[1, 0].set_yticks([])

# Magnitude spectrums
axs[0, 1].imshow(np.log(1 + magnitude_spectrum_top))
axs[0, 1].set_title('Magnitude Spectrum (Top Line)')
axs[0, 1].set_xticks([])
axs[0, 1].set_yticks([])

axs[1, 1].imshow(np.log(1 + magnitude_spectrum_bottom))
axs[1, 1].set_title('Magnitude Spectrum (Bottom Line)')
axs[1, 1].set_xticks([])
axs[1, 1].set_yticks([])

# plt.tight_layout()
plt.show()

print(magnitude_spectrum_top, magnitude_spectrum_bottom)