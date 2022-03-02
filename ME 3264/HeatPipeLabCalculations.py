pip install -q thermostate

pip install --upgrade -q uncertainties

import numpy as np
from thermostate import Q_,units,State
import matplotlib.pyplot as plt
import math
import csv
import warnings
warnings.filterwarnings('ignore')
from uncertainties import ufloat
from uncertainties.umath import log

from google.colab import drive
drive.mount('/content/drive')

heat_4_dimensionless = []
heat_3_dimensionless = []
heat_5_dimensionless = []
heat_6_dimensionless = []
heat_2_dimensionless = []
heat_1_dimensionless = []
heat_7_dimensionless = []
#Make correct file name#########################################################

with open("/content/drive/MyDrive/Semester 6/ME 3264/Lab Reports/Lab #2/Data/Lab2DataPart2.txt", "r") as csvfile:
  plots = csv.reader(csvfile, delimiter = "\t")
  next(plots)
  for row in plots:
    heat_4_dimensionless.append(float(row[0]))
    heat_3_dimensionless.append(float(row[1]))
    heat_5_dimensionless.append(float(row[2]))
    heat_6_dimensionless.append(float(row[3]))
    heat_2_dimensionless.append(float(row[4]))
    heat_1_dimensionless.append(float(row[5]))
    heat_7_dimensionless.append(float(row[6]))



heat_4 = np.zeros_like(heat_4_dimensionless)*units.degC
heat_3 = np.zeros_like(heat_3_dimensionless)*units.degC
heat_5 = np.zeros_like(heat_5_dimensionless)*units.degC
heat_6 = np.zeros_like(heat_6_dimensionless)*units.degC
heat_2 = np.zeros_like(heat_2_dimensionless)*units.degC
heat_1 = np.zeros_like(heat_1_dimensionless)*units.degC
heat_7 = np.zeros_like(heat_7_dimensionless)*units.degC

for i in range(len(heat_4)):
  heat_4[i] = heat_4_dimensionless[i]*units.degC
  heat_3[i] = heat_3_dimensionless[i]*units.degC
  heat_5[i] = heat_2_dimensionless[i]*units.degC
  heat_6[i] = heat_1_dimensionless[i]*units.degC
  heat_2[i] = heat_6_dimensionless[i]*units.degC
  heat_1[i] = heat_5_dimensionless[i]*units.degC
  heat_7[i] = heat_7_dimensionless[i]*units.degC

time =  np.zeros_like(heat_4_dimensionless)*units.s

for i in range(len(time)):
  time[i] = Q_(i,"sec")/2

plt.rcParams["figure.figsize"] = (12,4)
plt.plot(time.to("min"),heat_4,"green")
plt.plot(time.to("min"),heat_3,"blue")
plt.plot(time.to("min"),heat_5,"yellow")
plt.plot(time.to("min"),heat_6,"orange")
plt.plot(time.to("min"),heat_2,"purple")
plt.plot(time.to("min"),heat_1,"violet")
plt.plot(time.to("min"),heat_7,"red")
plt.grid(True)
plt.show()

tempavg = np.zeros_like(heat_4_dimensionless)*units.K
evapavg = np.zeros_like(heat_4_dimensionless)*units.K
condavg = np.zeros_like(heat_4_dimensionless)*units.K

for i in range(len(heat_4)):
#  tempavg[i] = (heat_4[i].to("K")+heat_3[i].to("K")+heat_5[i].to("K"))/3
  evapavg[i] = (heat_7[i].to("K")+heat_6[i].to("K")+heat_5[i].to("K"))/3
  condavg[i] = (heat_1[i].to("K")+heat_2[i].to("K")+heat_3[i].to("K")+heat_4[i].to("K"))/4


#evap_diff = (evapavg-tempavg).to("delta_degC")
#cond_diff = (condavg-tempavg).to("delta_degC")
temp_drop = (evapavg-condavg).to("delta_degC")

plt.plot(time.to("min"),condavg.to("degC"),color = "#182A60",label = "Condenser Temperature")
plt.plot(time.to("min"),evapavg.to("degC"),color = "#E4002B",label = "Evaporator Temperature")
plt.legend()
plt.xlabel("Time (Minutes)")
plt.ylabel("Temperature ($^o$C)")
plt.title("Measured Heat Pipe Temperatures")
plt.grid(True)

#Filter test
from scipy.signal import lfilter

n = 75 # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1

temp_drop_filtered = lfilter(b,a,temp_drop)*units.delta_degC

plt.plot(time.to("min"),temp_drop.to("delta_degC"),color = "#A4C8E1",label = "Temperature Drop")
plt.plot(time.to("min"),temp_drop_filtered.to("delta_degC"),color = "#000E2F",label = "Temperature Drop (Filtered)")
plt.legend()
plt.xlabel("Time (Minutes)")
plt.ylabel("Temperature Drop ($^o$C)")
plt.title("Temperature Drop between Evaportator and Condenser versus Time")
plt.grid(True)

input_power = np.zeros_like(time)*units.watt

for i in range(len(time)):
  if 0*units.min<time[i]<9.25*units.min:
    input_power[i] = 3.08*units.watts
  elif 9.25*units.min<=time[i]<16.7*units.min:
    input_power[i] = 5.93*units.watts
  elif 16.7*units.min<=time[i]<24.7*units.min:
    input_power[i] = 9.02*units.watts
  elif 24.7*units.min<=time[i]:
    input_power[i] = 12.06*units.watts

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()

lns1 = ax1.plot(time.to("min"),temp_drop.to("delta_degC"),color = "#A4C8E1",label = "Temperature Drop")
lns2 = ax1.plot(time.to("min"),temp_drop_filtered.to("delta_degC"),color = "#000E2F",label = "Temperature Drop (Filtered)")
lns3 = ax2.plot(time.to("min"),input_power,"#E4002B",label = "Input Power")


ax1.set_xlabel("Time (Minutes)")
ax1.set_ylabel("Temperature Drop ($^o$C)",color = "#000E2F")
ax2.set_ylabel("Heat (W)",color = "#E4002B")
plt.title("Temperature Drop between Evaportator and Condenser versus Time")

lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=4)
ax1.grid(True)
plt.show()

l1 = []
avg1 = 0
len1 = 0
l2 = []
avg2 = 0
len2 = 0
l3 = []
avg3 = 0
len3 = 0
l4 = []
avg4 = 0
len4 = 0

def st_dev(avg, N, data):
  sum = 0
  for i in range(len(data)):
    sum += (data[i] - avg)**2
  return (sum/N)**(1/2)


for i in range(len(time)):
  if 0.5*units.min<time[i]<9.2*units.min:
    l1.append(temp_drop[i])
    avg1 += temp_drop[i]
    len1 += 1
  elif 9.3*units.min<=time[i]<16.2*units.min:
    l2.append(temp_drop[i])
    avg2 += temp_drop[i]
    len2 += 1
  elif 17.2*units.min<=time[i]<24.2*units.min:
    l3.append(temp_drop[i])
    avg3 += temp_drop[i]
    len3 += 1
  elif 25.2*units.min<=time[i-100]:
    l4.append(temp_drop[i])
    avg4 += temp_drop[i]
    len4 += 1

avg1 = avg1 / len1
std1 = st_dev(avg1, len1, l1)
avg2 = avg2 / len2
std2 = st_dev(avg2, len2, l2)
avg3 = avg3 / len3
std3 = st_dev(avg3, len3, l3)
avg4 = avg4 / len4
std4 = st_dev(avg4, len4, l4)

print(avg1.round(2), std1.round(3))
print(avg2.round(2), std2.round(3))
print(avg3.round(2), std3.round(3))
print(avg4.round(2), std4.round(3))

#Thermal Effectivity

q_3 = ((0.38*units.amperes).plus_minus(0.005)*(8.1*units.volts).plus_minus(0.05)).to("watts")
q_6 = ((0.52*units.amperes).plus_minus(0.005)*(11.4*units.volts).plus_minus(0.05)).to("watts")
q_9 = ((0.64*units.amperes).plus_minus(0.005)*(14.1*units.volts).plus_minus(0.05)).to("watts")
q_12 = ((0.74*units.amperes).plus_minus(0.005)*(16.3*units.volts).plus_minus(0.05)).to("watts")


#Temperature drop TD
TD_3 = avg1.plus_minus(std1)
TD_6 = avg2.plus_minus(std2)
TD_9 = avg3.plus_minus(std3)
TD_12 = avg4.plus_minus(std4)

def get_keff(l_eff,q,delta_T,A_c):
  return l_eff*q/(delta_T*A_c)

L_a = Q_(0,"mm")
L_e = Q_(45,"mm")
L_c = Q_(155,"mm")
L_eff = L_e/2+L_a+L_c/2
A_c = np.pi/4*Q_(8,"mm")**2

keff_3 = get_keff(L_eff,q_3,TD_3,A_c)
keff_6 = get_keff(L_eff,q_6,TD_6,A_c)
keff_9 = get_keff(L_eff,q_9,TD_9,A_c)
keff_12 = get_keff(L_eff,q_12,TD_12,A_c)

print(keff_3.to("kilowatts/meter/kelvin"))
print(keff_6.to("kilowatts/meter/kelvin"))
print(keff_9.to("kilowatts/meter/kelvin"))
print(keff_12.to("kilowatts/meter/kelvin"))
print(A_c)

#copper_pipe = get_keff(Q_(0.16,"m"),Q_(3,"watts"),46*units.degC-41*units.degC, np.pi/4*Q_(6,"mm")**2)
#print(copper_pipe.to("kilowatts/meter/kelvin"))

keff_list = np.zeros_like(time)*units.kilowatt/units.meter/units.kelvin
keff_list_filtered = np.zeros_like(time)*units.kilowatt/units.meter/units.kelvin

for i in range(len(time)):
  keff_list[i] = get_keff(L_eff,input_power[i],temp_drop[i],A_c)
  keff_list_filtered[i] = get_keff(L_eff,input_power[i],temp_drop_filtered[i],A_c)

n = 75 # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1

#keff_list_filtered = lfilter(b,a,keff_list)*units.kilowatt/units.meter/units.kelvin

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
lns1 = ax1.plot(time.to("min"),keff_list,color = "#A4C8E1",label = "Termal Conductivity")
lns2 = ax1.plot(time.to("min"),keff_list_filtered,color = "#000E2F",label = "Termal Conductivity (Filtered)")
lns3 = ax2.plot(time.to("min"),input_power,"#E4002B",label = "Input Power")

y_min = 0*units.kilowatt/units.meter/units.kelvin
y_max = 15*units.kilowatt/units.meter/units.kelvin
ax1.set_ylim(y_min,y_max)
ax1.set_xlabel("Time (Minutes)")
ax1.set_ylabel("Thermal Conductivity ($kW /(m\cdot K$)",color = "#000E2F")
ax2.set_ylabel("Heat (W)",color = "#E4002B")

lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=4)
ax1.grid(True)
plt.title("Effective Thermal Conductivites versus Time")
plt.show()