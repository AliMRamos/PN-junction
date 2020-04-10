import os
import argparse
import Calculations as cal

parser = argparse.ArgumentParser(description="Obtain the theoretical results for a PN junction of Si")
parser.add_argument('-n', metavar='file_name', help='specify this option to rename the file.', default=None)
args = parser.parse_args()

'---------------------------DATOS---------------------------'
temperatura = 300.  # K
energia_gap = 1.12  # eV
cte_dielectrica = 1.044772 * (10. ** -12.)  # F/cm

donadores = 5.4 * (10. ** 16)  # cm-3
aceptores = 5.4 * (10. ** 17)  # cm-3
polarizacion = 0.3  # V

'-----------------------------------------------------------'

n_i, N_V, N_C = cal.concentracion_intrinseca(temperatura, energia_gap)
p_p, n_n, p_n, n_p = cal.portadores(n_i, donadores, aceptores)
V_bi = cal.potenical_contacto(donadores, aceptores, n_i, temperatura)
x_n = cal.vaciamiento_n(cte_dielectrica, V_bi, donadores, aceptores)
x_p = cal.vaciamiento_p(cte_dielectrica, V_bi, donadores, aceptores)
W = cal.ancho_vaciamiento(x_n, x_p)
E_max = cal.energia_maxima(donadores, x_n, cte_dielectrica)
ValToIn, CondToIn, p_type, n_type = cal.bandas(energia_gap, temperatura, aceptores, n_i, donadores, N_V)
quasi_f, quasi_f_2, fermi = cal.desplazamiento_bandas(n_type, p_type, V_bi, polarizacion)

# Aplicamos polarizacion
V_j = cal.bias(V_bi, polarizacion)
x_p_bias = cal.vaciamiento_p_bias(cte_dielectrica, V_j, donadores, aceptores)
x_n_bias = cal.vaciamiento_n_bias(cte_dielectrica, V_j, donadores, aceptores)
W_bias = cal.ancho_vaciamiento_bias(cte_dielectrica, V_j, donadores)
E_max_bias = cal.energia_maxima_bias(donadores, x_n_bias, cte_dielectrica)

'########################### RESULTADOS A UN TXT ###########################'

file_name = args.n or "datos"
check = file_name
i = 1
while os.path.isfile(check + ".txt"):
    i += 1
    check = "%s_%d" % (file_name, i)
if i > 1:
    file_name = check

f = open(file_name + ".txt", 'w')
f.writelines("----UNION PN de SI---")
f.writelines('\n\n')
f.writelines('n_i = %.2f [cm-3]' % n_i)
f.writelines('\n')
f.writelines('p = p_p = %f [cm-3]' % p_p)
f.writelines('\n')
f.writelines('n = n_n = %f [cm-3]' % n_n)
f.writelines('\n')
f.writelines('p_n = %f [cm-3]' % p_n)
f.writelines('\n')
f.writelines('n_p = %f [cm-3]' % n_p)
f.writelines('\n\n\n')
f.writelines('V_bi = %f' % V_bi)
f.writelines('\n\n')
f.writelines('x_n = %f [cm]' % x_n)
f.writelines('\n')
f.writelines('x_p = %f [cm]' % x_p)
f.writelines('\n')
f.writelines('W = %f [cm]' % W)
f.writelines('\n\n')
f.writelines('Campo maximo = %f' % E_max)
f.writelines('\n\n')
f.writelines('E_i - E_V = %f' % ValToIn)
f.writelines('\n')
f.writelines('E_C - E_i = %f' % CondToIn)
f.writelines('\n')
f.writelines('Zona P: E_F - E_i = %f' % p_type)
f.writelines('\n')
f.writelines('Zona N: E_F - E_i = %f' % n_type)
f.writelines('\n')
f.writelines('\n')
f.writelines('Deplazamiento: (E_i)_p -(E_i)_n = %f' % quasi_f)
f.writelines('\n')
f.writelines('Comprobacion del desplazamiento: %f' % quasi_f_2)
f.writelines('\n\n\n\n')
f.writelines('Polarizacion aplicada de %fV' % polarizacion)
f.writelines('\n\n')
f.writelines('V_j = %f' % V_j)
f.writelines('\n\n')
f.writelines('(x_n)\' = %f' % x_n_bias)
f.writelines('\n')
f.writelines('(x_p)\' = %f' % x_p_bias)
f.writelines('\n')
f.writelines('W\' = %f' % W_bias)
f.writelines('\n')
f.writelines('(E_max)\' = %f' % E_max_bias)
f.writelines('\n\n')
f.writelines('Desdoblamiento: %f' % fermi)
f.writelines('\n\n')
f.close()
