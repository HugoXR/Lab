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

t=T
erro_t = 1e-6


erro_chi = lambda T, C, erro_t, erro_C: np.sqrt((erro_T/(2*np.pi*C))**2 + (-erro_C*T/(2*np.pi*C**2))**2)
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

print(f"I = {I}+/-{erro_I} A")

V = R*I

erro_V = np.sqrt((erro_R*I)**2 + (erro_I*R)**2)

print(f"V = {V} +/- {erro_V} V")

