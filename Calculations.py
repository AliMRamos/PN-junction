import math as m
import numpy as np
import scipy.constants as sc

cte_boltz_J = sc.physical_constants["Boltzmann constant"][0]  # J/K
cte_boltz_eV = sc.physical_constants["Boltzmann constant in eV/K"][0]  # eV/K
permittivity = sc.epsilon_0 / 100.  # F/cm
q = sc.e  # C


def intrinsic_concentration(temperature, gap_energy):
    N_C = 6. * (0.36 ** (3. / 2.)) * (temperature ** (3. / 2.)) * 4.8286 * (10. ** 15.)  # cm-3
    N_V = (0.81 ** (3. / 2.)) * (temperature ** (3. / 2.)) * 4.8286 * (10. ** 15.)  # cm-3
    n_i = m.sqrt(N_C * N_V) * m.e ** (-gap_energy / (2. * cte_boltz_eV * temperature))  # cm-3
    return n_i, N_V, N_C


def carriers(intrins_concentr, donors, acceptors):
    p_p = acceptors
    n_n = donors
    p_n = (intrins_concentr ** 2.) / donors
    n_p = (intrins_concentr ** 2.) / acceptors
    return p_p, n_n, p_n, n_p


def built_in_potencial(donors, acceptors, intrins_concentr, temperature):
    V_bi = (cte_boltz_J * temperature / q) * m.log(donors * acceptors / (intrins_concentr ** 2.))  # V
    return V_bi


def field_maximum(donors, x_n, relative_permittivity):
    E_max = -q * donors * x_n / (permittivity * relative_permittivity)  # V/cm
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


def bands(gap_energy, temperature, acceptors, concentr_instrins, donors, N_V, effective_mass_holes,
          effective_mass_electrons):
    E_V = 0.
    E_C = gap_energy + E_V
    E_i = E_V + (gap_energy / 2.) + (3. * cte_boltz_eV * temperature / 4.) * m.log(
        effective_mass_holes / effective_mass_electrons)
    E_F = E_V - (cte_boltz_eV * temperature * m.log(acceptors / N_V))
    if E_C - E_F > 3. * cte_boltz_eV * temperature and E_F - E_V > 3. * cte_boltz_eV * temperature:
        print('Nondegenerate Semiconductor')
    else:
        print('Degenerate Semiconductor, the approximations taken into a count can not be used')
        exit(1)
    # Fermi level
    p_type = cte_boltz_eV * temperature * m.log(concentr_instrins / acceptors)
    n_type = cte_boltz_eV * temperature * m.log(donors / concentr_instrins)
    return E_i - E_V, E_C - E_i, p_type, n_type


'''
Case for V_bi=0, none forward nor reverse bias has been taken into account
'''


def depletion_n(relative_permittivity, V_bi, donors, acceptors):
    x_n = m.sqrt(
        2. * permittivity * relative_permittivity * V_bi * acceptors / (q * donors * (acceptors + donors)))  # cm
    return x_n


def depletion_p(relative_permittivity, V_bi, donors, acceptors):
    x_p = m.sqrt(
        2. * (permittivity * relative_permittivity) * V_bi * donors / (q * acceptors * (acceptors + donors)))  # cm
    return x_p


def depletion_zone(x_n, x_p):
    W = x_p + x_n  # cm
    return W


'''
Applying forward and reverse bias:
    Forward bias: V_A > 0; V_A < V_bi
    Reverse bias: V_A < 0
'''


def bias(V_bi, bias):
    V_j = V_bi - bias
    return V_j


def depletion_n_bias(relative_permittivity, V_j, donors, acceptors):
    x_n_bias = m.sqrt(
        2. * (permittivity * relative_permittivity) * V_j * acceptors / (q * donors * (acceptors + donors)))
    return x_n_bias


def depletion_p_bias(relative_permittivity, V_j, donors, acceptors):
    x_p_bias = m.sqrt(2. * permittivity * relative_permittivity * V_j * donors / (q * acceptors * (acceptors + donors)))
    return x_p_bias


def depletion_zone_bias(relative_permittivity, V_j, donors):
    W_bias = m.sqrt(2. * (permittivity * relative_permittivity) * V_j / (q * donors))
    return W_bias


def field_maximum_bias(donors, x_n_bias, relative_permittivity):
    E_max_bias = -q * donors * x_n_bias / (permittivity * relative_permittivity)  # V/cm
    return E_max_bias


def displacement_bands(n_type, p_type, V_bi, bias):
    # Quasi Fermi levels
    quasi_f = n_type - p_type
    quasi_f_2 = V_bi
    fermi = bias
    return quasi_f, quasi_f_2, fermi


def current_flux(bias1, bias2, temperature, n_p, p_n):
    corriente = []
    D_n = cte_boltz_eV * temperature * 1488
    L_n = m.sqrt(D_n * 1 * (10 ** -10))
    D_p = cte_boltz_eV * temperature * 2169
    L_p = m.sqrt(D_p * 1 * (10 ** -10))
    voltage = np.linspace(bias1, bias2, num=20)
    voltage = list(voltage)
    for indx, bias in enumerate(voltage):
        J = q * (((D_n / L_n) * n_p) + ((D_p / L_p) * p_n)) * (
                (m.e ** (bias / (cte_boltz_eV * temperature))) - 1)
        corriente.append([voltage[indx], J])
    fil = open("corrientes.txt", "w")
    encabezado = ["------------------------------------------------------------ \n Current \n ------------------------------------------------------------ \nVoltage (V), Current (A/cm2) \n"]
    fil.writelines(encabezado)
    fil.writelines([str(i)+"\n" for i in corriente])
    fil.close()

