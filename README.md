# PN-junction
Calculates certain parameters for a PN junction, taking into account the (non)degeneration of the semiconductor and obtaining the results only for the nondegenerate states

## How to use

The script allow you to either read a [config.txt](https://github.com/AliMRamos/PN-junction/blob/master/config.txt) as this one or to pass in arguments. 

- Example for reading a file:
```
python main.py -i config.txt
```
- Example parsing arguments: 
```
python main.py -t 200 -mh 0.5 -me 0.3 -ge 1.46 -rp 6.43 -d 6.0e15 -a 6.0e15 -b 0.4
```

You can rename the output file for the results (results.txt) with:
```
python main.py -o rename
```
## **Parsed arguments**

Below are listed the arguments accepted by the progam. You can see the full information and default values by using th following command:\
`python main.py -h`


* -i:  path to a input file as in this example [config.txt](https://github.com/AliMRamos/PN-junction/blob/master/config.txt)
* -o:  specify this option to rename the output file
* -t:  temperature for the simulation
* -mh: effective mass of the holes for the material
* -me: effective mass of the electrons for the material
* -ge: energy gap of the material
* -rp: relative permittivity of the material
* -d:  specify the donors with the format 4.2e15
* -a:  specify the acceptors with the format 6.7e16
* -b:  specify the bias: forward 0.2, reverse -0.3

## Results

You can see some output files as examples [here](https://github.com/AliMRamos/PN-junction/tree/master/results). 
