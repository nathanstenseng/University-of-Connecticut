import numpy as np
import matplotlib.pyplot as plt
import math
import csv
from scipy.optimize import curve_fit
from decimal import Decimal

def lin_approx(x,a_0,a_1):
  return a_1*x + a_0
UConn_1 = "#004369" #Navy
UConn_2 = "#A4C8E1" #Light Blue
UConn_3 = "#E4002B" #Red

# LVDT Testing
x_1 = np.asarray([1, 2, 3, 3.5, 4, 4.5, 5, 5.25, 5.5, 5.75, 6, 6.25, 6.5, 7]) #mm
V_1 = np.asarray([-3.472, -1.585, 0.286, 1.214, 2.1625, 3.1195, 4.0705, 4.5355, 5.018, 5.418, 5.94, 6.385, 6.823, 7.666]) #V
x_2 = np.asarray([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7])
V_2 = np.asarray([-3.485, -2.5305, -1.585, -0.653, 0.275, 1.214, 2.167, 3.112, 4.075, 5.018, 5.938, 6.8295, 7.669])
x_range = np.linspace(1,7,100)

coeff1, pcov_1 = curve_fit(lin_approx, x_1, V_1)
print("V = {:.3}x + {:.3}".format(coeff1[1],coeff1[0]))
stand_dev = np.sqrt(np.diag(pcov_1))
print(stand_dev)
plt.plot(x_range,lin_approx(x_range,*coeff1), "k-",label = "Line of best fit")
plt.plot(x_1,V_1,"o",label = "data")
plt.title("Test 1")
plt.ylabel("Recorded Voltage (V)")
plt.xlabel("Input Displacement (mm)")
plt.legend()
plt.grid(True)
plt.show()

coeff2, pcov_2 = curve_fit(lin_approx, x_2, V_2)
print("V = {:.3}x + {:.3}".format(coeff2[1],coeff2[0]))
plt.plot(x_range,lin_approx(x_range,*coeff2), "k-",label =  "Line of best fit")
plt.plot(x_2,V_2,"o",label = "data")
stand_dev = np.sqrt(np.diag(pcov_2))
print(stand_dev)
plt.title("LVDT Calibration")
plt.ylabel("Recorded Voltage (V)")
plt.xlabel("Input Displacement (mm)")
plt.legend()
plt.grid(True)
plt.show()

def get_V(d):
  return 1.87*d - 5.325
def get_d(V):
  return 0.535*V+2.846

# Peak to Peak
Vpp_1 = np.asarray([1,2,3,4,5,6,7,8,9,10]) #V
Vpp_2 = Vpp_1 #V
Vpp_3 = Vpp_2 #V
PeakPeak_1 = np.asarray([0.0057, 0.014, 0.022, 0.031, 0.036, 0.042, 0.0459, 0.046, 0.0462, 0.0462]) #V
PeakPeak_2 = np.asarray([0.0065, 0.014, 0.022, 0.031, 0.036, 0.042, 0.045, 0.0457, 0.0458, 0.0459]) #V
PeakPeak_3 = np.asarray([0.008, 0.015, 0.022, 0.029, 0.034, 0.038, 0.042, 0.044, 0.044, 0.0445]) #V

Vpp_1 = np.asarray([1,2,3,4,5,6,7]) #V
Vpp_2 = Vpp_1 #V
Vpp_3 = Vpp_2 #V
PeakPeak_1 = np.asarray([0.0057, 0.014, 0.022, 0.031, 0.036, 0.042, 0.0459]) #V
PeakPeak_2 = np.asarray([0.0065, 0.014, 0.022, 0.031, 0.036, 0.042, 0.045]) #V
PeakPeak_3 = np.asarray([0.008, 0.015, 0.022, 0.029, 0.034, 0.038, 0.042]) #V

d_1 = get_d(PeakPeak_1)
d_2 = get_d(PeakPeak_2)
d_3 = get_d(PeakPeak_3)

coeff1, pcov_1 = curve_fit(lin_approx, Vpp_1, d_1)
print("x = {:.3}V + {:.3}".format(coeff1[1],coeff1[0]))
stand_dev = np.sqrt(np.diag(pcov_1))
print(stand_dev)
plt.plot(Vpp_1, lin_approx(Vpp_1,*coeff1), "k-",label = "Linear Regression")
plt.plot(Vpp_1, d_1,"o",label = "Data")
plt.title("100 Hz Test")
plt.xlabel("Applied Voltage (V)")
plt.ylabel("Measured Displacement (mm)")
plt.legend()
plt.grid(True)
plt.show()

coeff1, pcov_1 = curve_fit(lin_approx, Vpp_2, d_2)
print("x = {:.3}V + {:.3}".format(coeff1[1],coeff1[0]))
stand_dev = np.sqrt(np.diag(pcov_1))
print(stand_dev)
plt.plot(Vpp_2, lin_approx(Vpp_2,*coeff1), "k-",label = "Linear Regression")
plt.plot(Vpp_2, d_2,"o",label = "Data")
plt.title("100 Hz Test")
plt.xlabel("Applied Voltage (V)")
plt.ylabel("Measured Displacement (mm)")
plt.legend()
plt.grid(True)
plt.show()

coeff1, pcov_1 = curve_fit(lin_approx, Vpp_3, d_3)
print("x = {:.3}V + {:.3}".format(coeff1[1],coeff1[0]))
stand_dev = np.sqrt(np.diag(pcov_1))
print(stand_dev)
plt.plot(Vpp_3, lin_approx(Vpp_3,*coeff1), "k-",label = "Linear Regression")
plt.plot(Vpp_3, d_3,"o",label = "Data")
plt.title("100 Hz Test")
plt.xlabel("Applied Voltage (V)")
plt.ylabel("Measured Displacement (mm)")
plt.legend()
plt.grid(True)
plt.show()