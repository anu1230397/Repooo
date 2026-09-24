import pandas  as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



time= np.linspace (0,10,500)

amplitude =np.exp(-0.5 *time)*np.sin(2*np.pi*time)

fig, ax = plt.subplots(figsize=(8,4.5), dpi=100)
ax.plot(time, amplitude , color='blue', linewidth=2, label='Sensor A displacement')

ax.set_title('Damped Harmonic Response of Structure', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Time (seconds)', fontsize=12)
ax.set_ylabel('Displacement (mm)', fontsize=12)
# Enable engineering gridlines
ax.grid(True, linestyle='--', alpha=0.6)
# Configure the Legend
ax.legend(loc='upper right', frameon=True, shadow=True)

plt.show()
plt.savefig('damped_harmonic_response.png', dpi=300, bbox_inches='tight')

