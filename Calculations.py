'''
Alicia M. Ramos, contacto munozramosalicia@gmail.com
Calculos teoricos para una union PN de Si
Valores tomados de http://www.ioffe.ru/SVA/NSM/Semicond/Si/index.html
'''
import math as m
import numpy as np
import scipy.constants as sc

cte_boltz_J = sc.physical_constants["Boltzmann constant"][0]  # J/K
cte_boltz_eV = sc.physical_constants["Boltzmann constant in eV/K"][0]  # eV/K
q = sc.e  # C
m_h = 0.81  # *m_0
m_e = 1.18  # *m_0


def concentracion_intrinseca(temperatura, energia_gap):
    N_C = 6. * (0.36 ** (3. / 2.)) * (temperatura ** (3. / 2.)) * 4.8286 * (10. ** 15.)  # cm-3
    N_V = (0.81 ** (3. / 2.)) * (temperatura ** (3. / 2.)) * 4.8286 * (10. ** 15.)  # cm-3
    n_i = m.sqrt(N_C * N_V) * m.e ** (-energia_gap / (2. * cte_boltz_eV * temperatura))  # cm-3
    return n_i, N_V, N_C


def portadores(concentr_intrins, donadores, aceptores):
    p_p = aceptores
    n_n = donadores
    p_n = (concentr_intrins ** 2.) / donadores
    n_p = (concentr_intrins ** 2.) / aceptores
    return p_p, n_n, p_n, n_p


def potenical_contacto(donadores, aceptores, concentr_intrins, temperatura):
    V_bi = (cte_boltz_J * temperatura / q) * m.log(donadores * aceptores / (concentr_intrins ** 2.))  # V
    return V_bi


def energia_maxima(donadores, x_n, cte_dielectrica):
    E_max = -q * donadores * x_n / cte_dielectrica  # V/cm
    return E_max


'''
Gap between the different bands. E_V as reference; =0

In Equilibrium:
    N type: n = N_D
    P type: p = N_A
    n * p = n_i**2

Out of equilibrium:
    We need to take in account the different parts of the junction to analise the Fermi level
'''


def bandas(energia_gap, temperatura, aceptores, concentr_instrins, donadores, N_V):
    E_V = 0.
    E_C = energia_gap + E_V
    E_i = E_V + (energia_gap / 2.) + (3. * cte_boltz_eV * temperatura / 4.) * m.log(m_h / m_e)
    E_F = E_V - (cte_boltz_eV * temperatura * m.log(aceptores / N_V))
    if E_C - E_F > 3. * cte_boltz_eV * temperatura and E_F - E_V > 3. * cte_boltz_eV * temperatura:
        print('Es no degenerado')
    else:
        print('Es degenerado, no se puede aproximar')
        exit(1)
    # Fermi level
    p_type = cte_boltz_eV * temperatura * m.log(concentr_instrins / aceptores)
    n_type = cte_boltz_eV * temperatura * m.log(donadores / concentr_instrins)
    return E_i - E_V, E_C - E_i, p_type, n_type


'''
Case for V_bi=0, none forward nor reverse bias has been taken into account
'''


def vaciamiento_n(cte_dielectrica, V_bi, donadores, aceptores):
    x_n = m.sqrt(2. * cte_dielectrica * V_bi * aceptores / (q * donadores * (aceptores + donadores)))  # cm
    return x_n


def vaciamiento_p(cte_dielectrica, V_bi, donadores, aceptores):
    x_p = m.sqrt(2. * cte_dielectrica * V_bi * donadores / (q * aceptores * (aceptores + donadores)))  # cm
    return x_p


def ancho_vaciamiento(x_n, x_p):
    W = x_p + x_n  # cm
    return W


'''
Applying forward and reverse bias:
    Forward bias: V_A > 0; V_A < V_bi
    Reverse bias: V_A < 0
'''


def bias(V_bi, polarizacion):
    V_j = V_bi - polarizacion
    return V_j


def vaciamiento_n_bias(cte_dielectrica, V_j, donadores, aceptores):
    x_n_bias = m.sqrt(2. * cte_dielectrica * V_j * aceptores / (q * donadores * (aceptores + donadores)))
    return x_n_bias


def vaciamiento_p_bias(cte_dielectrica, V_j, donadores, aceptores):
    x_p_bias = m.sqrt(2. * cte_dielectrica * V_j * donadores / (q * aceptores * (aceptores + donadores)))
    return x_p_bias


def ancho_vaciamiento_bias(cte_dielectrica, V_j, donadores):
    W_bias = m.sqrt(2. * cte_dielectrica * V_j / (q * donadores))
    return W_bias


def energia_maxima_bias(donadores, x_n_bias, cte_dielectrica):
    E_max_bias = -q * donadores * x_n_bias / cte_dielectrica  # V/cm
    return E_max_bias


def desplazamiento_bandas(n_type, p_type, V_bi, polarizacion):
    # Quasi Fermi levels
    quasi_f = n_type - p_type
    quasi_f_2 = V_bi
    fermi = polarizacion
    return quasi_f, quasi_f_2, fermi


def densidad_corriente(polarizacion1, polarizacion2, temperatura, n_p, p_n):
    corriente = []
    D_n = cte_boltz_eV * temperatura * 1488
    L_n = m.sqrt(D_n * 1 * (10 ** -10))
    D_p = cte_boltz_eV * temperatura * 2169
    L_p = m.sqrt(D_p * 1 * (10 ** -10))
    voltage = np.linspace(polarizacion1, polarizacion2, num=20)
    voltage = list(voltage)
    for indx, polarizacion in enumerate(voltage):
        J = q * (((D_n / L_n) * n_p) + ((D_p / L_p) * p_n)) * (
                    (m.e ** (polarizacion / (cte_boltz_eV * temperatura))) - 1)
        corriente.append([voltage[indx], J])
    return corriente


