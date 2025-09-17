import numpy as np 
import matplotlib.pyplot as plt 

x = np.linspace(0, 10, 100)
y = np.sin(x)  
gaussian = np.exp(-0.5 * ((x - 5) / 1)**2)
plt.plot(x, y, label='sin(x)')
plt.plot(x, gaussian, label='Gaussian')
plt.legend()
plt.savefig('sinus_and_gaussian.png')
plt.show()
plt.close()
print("Script executed successfully")