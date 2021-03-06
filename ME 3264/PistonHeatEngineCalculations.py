pip install -q thermostate

pip install --upgrade -q uncertainties

import numpy as np
from thermostate import Q_,units,State
import matplotlib.pyplot as plt
import math
import warnings
warnings.filterwarnings('ignore')
from uncertainties import ufloat
from uncertainties.umath import log

#Piston

#Inner Diameter (ID) 
D_piston_error = Q_(0.1,"mm")
D_piston = ufloat(Q_(32.5,"dimensionless"),D_piston_error.magnitude)*units.mm
A_piston = (np.pi/4 * D_piston**2)
M_piston_error = Q_(0.6,"g")
M_piston = ufloat(Q_(35,"g").magnitude,M_piston_error.magnitude)*units.g
#Air Chamber (AC)
#Inner Diameter (ID) 
ID_AC_error = Depth_AC_error = Q_(0.25,"mm")
ID_AC = ufloat(Q_(44.8,"mm").magnitude,ID_AC_error.magnitude)*units.mm
Depth_AC = ufloat(Q_(112.5,"mm").magnitude,Depth_AC_error.magnitude)*units.mm
V_AC = Depth_AC * np.pi/4 * ID_AC**2
#Air Hose (AH)
ID_AH_error = ID_AC_error
Length_AH_error = Q_(0.1,"mm")
ID_AH = ufloat(Q_(3.3,"mm").magnitude,ID_AH_error.magnitude)*units.mm
Length_AH = ufloat(Q_(457,"mm").magnitude,Length_AH_error.magnitude)*units.mm
V_AH = Length_AH * np.pi/4 * ID_AH**2

def get_V(h): #Piston height (h) 
  return h * np.pi/4 * D_piston**2 + V_AC + V_AH

#Lab Data
h_error = 0.5
h_A = ufloat(25,h_error)*units.mm
h_B = ufloat(22,h_error)*units.mm
h_C = ufloat(65,h_error)*units.mm
h_D = ufloat(68,h_error)*units.mm
h_A_p = ufloat(26,h_error)*units.mm
m_A = m_D = m_A_p= Q_(0,"g")
m_B = m_C = Q_(100, "g")

def get_P(m): #Applied mass (m)
  return ((M_piston + m)*Q_(9.81, "m/s^2"))/A_piston + Q_(1,"atm")

p_A = get_P(m_A).to("kPa")
V_A = get_V(h_A).to("mm^3")
p_B = get_P(m_B).to("kPa")
V_B = get_V(h_B).to("mm^3")
p_C = get_P(m_C).to("kPa")
V_C = get_V(h_C).to("mm^3")
p_D = get_P(m_D).to("kPa")
V_D = get_V(h_D).to("mm^3")
p_A_p = get_P(m_A_p).to("kPa")
V_A_p = get_V(h_A_p).to("mm^3")
#Thermodynamic Work

#Isothermal (Requires Ideal Gas Assuption)
W_AB = p_A*V_A*log((V_B/V_A).magnitude) #Compression
W_CD = p_C*V_C*log((V_D/V_C).magnitude) #Expansion

#Isobaric 
W_BC = p_B*(V_C-V_B)
W_DA_p = p_D*(V_A_p-V_D)

W_net = W_AB+W_BC+W_CD+W_DA_p
print(p_C)
print("Thermodynamic Work =",W_net.to("J"))
#Mechanical Work

#Force over distance
W_BC_mech = (m_C*Q_(9.81,"m/s^2")) * (h_C-h_B)
print("Mechanical Work =",W_BC_mech.to("J"))
print(W_BC_mech.to("J") / W_net.to("J"))

#Plotting p-V Diagram

p = [p_A.magnitude.nominal_value,p_B.magnitude.nominal_value,p_C.magnitude.nominal_value,p_D.magnitude.nominal_value,p_A_p.magnitude.nominal_value]*units.kPa
V = [V_A.magnitude.nominal_value,V_B.magnitude.nominal_value,V_C.magnitude.nominal_value,V_D.magnitude.nominal_value,V_A_p.magnitude.nominal_value]*units.mm*units.mm*units.mm
plt.plot(V.to("cm^3"),p.to("kPa"),"k--")
plt.title("PV Diagram")
label = ["A","B","C","D","  A'"]
for i in range(len(p)):
  plt.text(V[i].to("cm^3").magnitude-0.75,p[i].magnitude+0.027, label[i])
  plt.plot(V[i].to("cm^3").magnitude,p[i].magnitude, "ko")
plt.plot(V[1:3].to("cm^3"),p[1:3].to("kPa"),"k-")
plt.plot(V[3:5].to("cm^3"),p[3:5].to("kPa"),"k-")
plt.xlabel("Volume (cm$^3$)")
plt.ylabel("Pressure (kPa)")
plt.ylim([101.6,103.1])
plt.show()