import os
import re
import argparse
import Calculations as cal

parser = argparse.ArgumentParser(description="Obtain the theoretical results for a PN junction (default values for Si")
parser.add_argument('-i', metavar='config_file', help='path to the config.txt', default=None)
parser.add_argument('-o', metavar='file_name', help='specify this option to rename the file')
parser.add_argument('-t', metavar='temperature (300.)', help='temperature for the simulation in [K]', type=float,
                    default=300.)
parser.add_argument('-mh', metavar='effective_mass_holes (0.01)', help='effective mass of the holes for the material',
                    type=float, default=0.81)
parser.add_argument('-me', metavar='effective_mass_electrons (1.18)',
                    help='effective mass of the electrons for the material',
                    type=float, default=1.18)
parser.add_argument('-ge', metavar='energy_gap (1.12)', help='energy gap of the material [eV]', type=float, default=1.12)
parser.add_argument('-rp', metavar='relative_permittivity (11.8)', help='relative permittivity of the material', type=float,
                    default=11.8)
parser.add_argument('-d', metavar='donors (5.0e16)', help='specify the donors [cm-3] with the format 4.2e15', type=float,
                    default=5.0e16)
parser.add_argument('-a', metavar='acceptors (5.0e16)', help='specify the acceptors [cm-3] with the format 6.7e16', type=float,
                    default=5.0e16)
parser.add_argument('-b', metavar='bias (0.0)', help='specify the bias [V]: forward 0.2, reverse -0.3', type=float,
                    default=0.0)
args = parser.parse_args()


def get_config(config_file):
    parameters = []
    with open(config_file, 'r') as cf:
        regex_parameters = re.compile(r'^(\S*)\=(.*)$')
        for line in cf:
            line = line.strip().replace(" ", "")
            if not line.startswith("#") and not line.startswith("\n"):
                match = regex_parameters.match(line)
                parameters.append((match.group(1), match.group(2)))
    result = {}
    for l in parameters:
        result[l[0]] = l[1]
    return result


if args.i is None:
    effective_mass_holes = args.mh
    effective_mass_electrons = args.me
    temperature = args.t
    gap_energy = args.ge
    relative_permittivity = args.rp
    donors = args.d
    acceptors = args.a
    bias = args.b

else:
    parameter = get_config(args.i)
    effective_mass_holes = float(parameter["effective_mass_holes"])
    effective_mass_electrons = float(parameter["effective_mass_electrons"])
    temperature = float(parameter["temperature"])
    gap_energy = float(parameter["gap_energy"])
    relative_permittivity = float(parameter["relative_permittivity"])
    donors = float(parameter["donors"])
    acceptors = float(parameter["acceptors"])
    bias = float(parameter["bias"])

n_i, N_V, N_C = cal.intrinsic_concentration(temperature, gap_energy)
p_p, n_n, p_n, n_p = cal.carriers(n_i, donors, acceptors)
V_bi = cal.built_in_potencial(donors, acceptors, n_i, temperature)
x_n = cal.depletion_n(relative_permittivity, V_bi, donors, acceptors)
x_p = cal.depletion_p(relative_permittivity, V_bi, donors, acceptors)
W = cal.depletion_zone(x_n, x_p)
E_max = cal.field_maximum(donors, x_n, relative_permittivity)
ValToIn, CondToIn, p_type, n_type = cal.bands(gap_energy, temperature, acceptors, n_i, donors, N_V,
                                              effective_mass_holes, effective_mass_electrons)
quasi_f, quasi_f_2, fermi = cal.displacement_bands(n_type, p_type, V_bi, bias)

if bias != 0.0:
    V_j = cal.bias(V_bi, bias)
    x_p_bias = cal.depletion_p_bias(relative_permittivity, V_j, donors, acceptors)
    x_n_bias = cal.depletion_n_bias(relative_permittivity, V_j, donors, acceptors)
    W_bias = cal.depletion_zone_bias(relative_permittivity, V_j, donors)
    E_max_bias = cal.field_maximum_bias(donors, x_n_bias, relative_permittivity)

'''

Printing the results to a file.txt

'''

file_name = args.o or "results"
check = file_name
i = 1
while os.path.isfile(check + ".txt"):
    i += 1
    check = "%s_%d" % (file_name, i)
if i > 1:
    file_name = check

f = open(file_name + ".txt", 'w')
f.writelines("\t\t\t\t\t\t+---------------+\n")
f.writelines("\t\t\t\t\t\t|  PN JUNCTION  |\n")
f.writelines("\t\t\t\t\t\t+---------------+\n")
f.writelines('\n\n')
f.writelines('+------------Initial Configuration------------+\n')
f.writelines("\t{:24} = {:{}{}.{}}[{}] \n".format('Temperature', temperature, '<', 10, '2f', 'K'))
f.writelines('\t{:24} = {:{}{}.{}}[{}] \n'.format('Energy gap', gap_energy, '<', 10, '2f', 'eV'))
f.writelines('\t{:24} = {:{}{}.{}}[{}] \n'.format('Donors', donors, '<', 10, '2e', 'cm-3'))
f.writelines('\t{:24} = {:{}{}.{}}[{}] \n'.format('Acceptors', acceptors, '<', 10, '2e', 'cm-3'))
f.writelines('\t{:24} = {:{}{}.{}}[{}] \n'.format('Bias', bias, '<', 10, '2f', 'V'))
f.writelines('\t{:24} = {:{}{}.{}} \n'.format('Effective mass holes', effective_mass_holes, '<', 10, '2f'))
f.writelines('\t{:24} = {:{}{}.{}} \n'.format('Effective mass electrons', effective_mass_electrons, '<', 10, '2f'))
f.writelines('\t{:24} = {:{}{}.{}} \n'.format('Relative permittivity', relative_permittivity, '<', 10, '2f'))
f.writelines('+---------------------------------------------+\n')
f.writelines('\n\n')
f.writelines('+-------------------Results-------------------+\n')
f.writelines("\t{:7} = {:{}{}.{}}[{}] \n".format('n_i', n_i, '<', 10, '2e', 'cm-3'))
f.writelines("\t{:7} = {:{}{}.{}}[{}] \n".format('p = p_p', p_p, '<', 10, '2e', 'cm-3'))
f.writelines("\t{:7} = {:{}{}.{}}[{}] \n".format('n = n_n', n_n, '<', 10, '2e', 'cm-3'))
f.writelines("\t{:7} = {:{}{}.{}}[{}] \n".format('p_n', p_n, '<', 10, '2e', 'cm-3'))
f.writelines("\t{:7} = {:{}{}.{}}[{}] \n".format('n_p', n_p, '<', 10, '2e', 'cm-3'))
f.writelines('                   --------                    \n')
f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('E_i - E_V', ValToIn, '<', 10, '3f', 'eV'))
f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('E_C - E_i', CondToIn, '<', 10, '3f', 'eV'))
f.writelines("\t{:15} = {:{}{}.{}}[{}] (P region) \n".format('E_F - E_i', p_type, '<', 10, '3f', 'eV'))
f.writelines("\t{:15} = {:{}{}.{}}[{}] (N region)\n".format('E_F - E_i', n_type, '<', 10, '3f', 'eV'))
f.writelines("\t{:15} = {:{}{}.{}}[{}] (Energy displacement)\n".format('(E_i)p - (E_i)n', quasi_f, '<', 10, '3f', 'V'))
f.writelines(
    "\t{:15} = {:{}{}.{}}[{}] (Validation of the energy displacement)\n".format('(E_i)p - (E_i)n', quasi_f_2, '<', 10,
                                                                                '3f', 'V'))
f.writelines('                   --------                    \n')
f.writelines("\t{:5} = {:{}{}.{}}[{}] \n".format('V_bi', V_bi, '<', 10, '3f', 'V'))
f.writelines("\t{:5} = {:{}{}.{}}[{}] \n".format('x_n', x_n, '<', 10, '2e', 'cm'))
f.writelines("\t{:5} = {:{}{}.{}}[{}] \n".format('x_p', x_p, '<', 10, '2e', 'cm'))
f.writelines("\t{:5} = {:{}{}.{}}[{}] \n".format('W', W, '<', 10, '2e', 'cm'))
f.writelines("\t{:5} = {:{}{}.{}}[{}] \n".format('E_max', E_max, '<', 10, '2e', 'V/cm'))
f.writelines('                   --------                    \n')
f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('V_A', bias, '<', 10, '3f', 'V'))
if bias != 0.0:
    f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('V_j', V_j, '<', 10, '3f', 'V'))
    f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('(x_n)\'', x_n_bias, '<', 10, '2e', 'cm'))
    f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('(x_p)\'', x_p_bias, '<', 10, '2e', 'cm'))
    f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('W\'', W_bias, '<', 10, '2e', 'cm'))
    f.writelines("\t{:15} = {:{}{}.{}}[{}] \n".format('E_max', E_max_bias, '<', 10, '2e', 'V/cm'))
    f.writelines(
        "\t{:15} = {:{}{}.{}}[{}] (Energy displacement)\n".format('(E_i)p - (E_i)n', fermi, '<', 10, '3f', 'V'))
f.writelines('+---------------------------------------------+\n')
f.close()
