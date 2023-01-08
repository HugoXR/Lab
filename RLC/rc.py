import numpy as np


R = 100
C = 0.47e-6
V = 3.37
T = 100e-6
erro_R = 5
erro_C = 0.01e-6
erro_V = 0.01
erro_T = 1e-6

Chi = lambda T,C: T/(2*np.pi*C)

phi = lambda Chi,R,T,C: np.arctan(Chi(T,C)/R)

i = lambda V,R,Chi,phi,T,t: (V/np.sqrt(R**2 + Chi(T,C)**2))*np.sin(phi(Chi,R,T,C)+t*2*np.pi/T)

t=np.array([T*n for n in np.arange(0,2,0.001)])
#t = T/5
erro_t = 1e-6


erro_chi = lambda T, C, erro_T, erro_C: np.sqrt((erro_T/(2*np.pi*C))**2 + (-erro_C*T/(2*np.pi*C**2))**2)
erro_phi = lambda erro_chi,T,C,erro_t,erro_C,Chi,R,erro_R: np.sqrt((R*erro_chi(T,C,erro_t,erro_C))**2 + (-erro_R*Chi(T,C))**2)/(R**2 + Chi(T,C)**2)



dV = lambda i,V,R,Chi,phi,T,t: i(V,R,Chi,phi,T,t)/V
dR = lambda i,V,R,Chi,phi,T,t: -i(V,R,Chi,phi,T,t)*R/(R**2 + Chi(T,C)**2)
dChi = lambda i,V,R,Chi,phi,T,t: -i(V,R,Chi,phi,T,t)*Chi(T,C)/(R**2 + Chi(T,C)**2)
dphi = lambda V,R,Chi,phi,T,t: (V/np.sqrt(R**2 + Chi(T,C)**2))*np.cos(phi(Chi,R,T,C)+t*2*np.pi/T)
dt = lambda dphi,V,R,Chi,phi,T,t: (dphi(V,R,Chi,phi,T,t)*2*np.pi)/T
dT = lambda dphi,V,R,Chi,phi,T,t: -V*t*2*np.pi*dphi(V,R,Chi,phi,T,t)/T**2

#dV = dV(i,V,R,Chi,phi,T,t)
#dR = dR(i,V,R,Chi,phi,T,t)
#dChi = dChi(i,V,R,Chi,phi,T,t)
#dt = dt(dphi,V,R,Chi,phi,T,t)
#dT = dT(dphi,V,R,Chi,phi,T,t)
#dphi = dphi(V,R,Chi,phi,T,t)

erro_i = lambda dV,dR,dChi,dphi,dT,dt,erro_V,erro_R,erro_chi,erro_phi,erro_T,erro_t,i,V,R,Chi,phi,T,t: np.sqrt((dV(i,V,R,Chi,phi,T,t)*erro_V)**2 + (dR(i,V,R,Chi,phi,T,t)*erro_R)**2 + (dChi(i,V,R,Chi,phi,T,t)*erro_chi(T,C,erro_t,erro_C))**2 + (dphi(V,R,Chi,phi,T,t)*erro_phi(erro_chi,T,C,erro_t,erro_C,Chi,R,erro_R))**2 + (dT(dphi,V,R,Chi,phi,T,t)*erro_T)**2 + (dt(dphi,V,R,Chi,phi,T,t)*erro_t)**2)



I = i(V,R,Chi,phi,T,t) 
erro_I = erro_i(dV,dR,dChi,dphi,dT,dt,erro_V,erro_R,erro_chi,erro_phi,erro_T,erro_t,i,V,R,Chi,phi,T,t)

i_max = lambda T,C,V,Chi,R: V/np.sqrt(R**2+Chi(T,C)**2)

I_max = i_max(T,C,V,Chi,R)
V_max_C = Chi(T,C)*I_max
V_max_R = R*I_max
dV_max = lambda R,Chi,T,C: 1/np.sqrt(R**2+Chi(T,C)**2)
dChi_max = lambda V,R,Chi,T,C: -V*Chi(T,C)/(np.sqrt(R**2 + Chi(T,C)**2))**3
dR_max = lambda V,R,Chi,T,C: -R*V/(np.sqrt(R**2 + Chi(T,C)**2))**3

erro_i_max = lambda dV_max,dChi_max,dR_max,T,C,R,erro_chi,erro_V,erro_R: np.sqrt((dV_max(R,Chi,T,C)*erro_V)**2 + (dChi_max(V,R,Chi,T,C)*erro_chi(T,C,erro_T,erro_C))**2 + (dR_max(V,R,Chi,T,C)*erro_R)**2)

erro_v_max_C = lambda I_max,Chi,erro_i_max,erro_chi,T,C,erro_T,erro_C: np.sqrt((I_max*erro_chi(T,C,erro_T,erro_C))**2 + (Chi(T,C)*erro_i_max(dV_max,dChi_max,dR_max,T,C,R,erro_chi,erro_V,erro_R))**2)

erro_v_max_R = lambda R,I_max,erro_i_max,dV_max,dChi_max,dR_max,T,C,erro_chi,erro_V,erro_R: np.sqrt((I_max*erro_R)**2 + (R*erro_i_max(dV_max,dChi_max,dR_max,T,C,R,erro_chi,erro_V,erro_R))**2)

erro_I_max = erro_i_max(dV_max,dChi_max,dR_max,T,C,R,erro_chi,erro_V,erro_R)
erro_V_max_C = erro_v_max_C(I_max,Chi,erro_i_max,erro_chi,T,C,erro_T,erro_C)
erro_V_max_R = erro_v_max_R(R,I_max,erro_i_max,dV_max,dChi_max,dR_max,T,C,erro_chi,erro_V,erro_R)


print(f"Capacitor")
print(f"{I_max} +/- {erro_I_max} A")
print(f"{V_max_C} +/- {erro_V_max_C} V")

print(f"Resistor")
print(f"{I_max} +/- {erro_I_max} A")
print(f"{V_max_R} +/- {erro_V_max_R} V")


#for n,value in enumerate(I):
#    print(f"{n*0.001}T {value} +/- {erro_I[n]} A")

#print(f"I = {I}+/-{erro_I} A")

#V = Chi(T,C)*I

#print(f"{Chi(T,C)}")

#erro_V = np.sqrt((erro_R*I)**2 + (erro_I*R)**2)

#for n,value in enumerate(V):
#    print(f"{n*0.001}T {value} +/- {erro_V[n]} V")


#print(f"V = {V} +/- {erro_V} V")
#print(np.max(I))
#print(np.max(V))
