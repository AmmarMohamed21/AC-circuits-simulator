import os
os.environ["LANG"]="en_US.UTF-8"
from ahkab import circuit
from ahkab import new_ac
from ahkab import run
import cmath as m
def Rad(angle):
   return angle*3.14159265358979/180
mycircuit = circuit.Circuit(title="AC circuit")
print('\n')
filename = input("Enter the file name of the circuit: ")
w = float(input("Enter frequency: "))
cirfile = open(filename, "r")
for line in cirfile:
    values = line.split()
    if line == '\n':
        continue
    if values[0][0] == 'V':
        acvalue=m.rect(float(values[3]),Rad(float(values[4])))
        mycircuit.add_vsource(values[0], values[1], values[2], dc_value=0, ac_value=acvalue)#dc should not be zero?
    if values[0][0] == 'I':
        acvalue=m.rect(float(values[3]),Rad(float(values[4])))
        mycircuit.add_isource(values[0], values[1], values[2], dc_value=0, ac_value=acvalue)#dc should not be zero?
    if values[0][0] == 'C':
        mycircuit.add_capacitor(values[0], values[1], values[2], float(values[3]))
    if values[0][0] == 'L':
        mycircuit.add_inductor(values[0], values[1], values[2], float(values[3]))
    if values[0][0] == 'R':
        mycircuit.add_resistor(values[0], values[1], values[2], float(values[3]))
ac = new_ac(start=w,stop=w,points=2,x0=None)
res = run(mycircuit,ac)
#saving result in a file
f = open("result.txt", "w")
for result in res['ac'].keys():
    f.write(str(result) + "=")
    f.write(str(res['ac'][result][0]))
    f.write('\n')
#storing nodes voltages:
voltage=[0+0j]
for x in res['ac'].keys():
	if x[0]=='V':
		voltage.append(res['ac'][x][0])
#calculating power in each component:
cirfile = open(filename, "r")
impedance_z=complex(1,0)
power_S=0+0j
for line in cirfile:
    values = line.split()
    if line == '\n':
        continue
    node1=int(values[1])
    node2=int(values[2])
    if values[0][0] == 'V':
        for x in res['ac'].keys():
            if x[0]=='I' and (x[2]+x[3])=='V'+values[0][1].capitalize():
                I=complex.conjugate(res['ac'][x][0])
                V=m.rect(float(values[3]),Rad(float(values[4])))
                power_S=I*V*0.5
    if values[0][0] == 'I':
        V=voltage[node1]-voltage[node2]#needs verification
        I=complex.conjugate(m.rect(float(values[3]),Rad(float(values[4]))))
        power_S=I*V*0.5
    if values[0][0] == 'C':
        impedance_z=complex(0,-1/(w*float(values[3])))
    if values[0][0] == 'L':
        impedance_z=complex(0,w*float(values[3]))
    if values[0][0] == 'R':
        impedance_z=complex(float(values[3]),0)
    if values[0][0]=='L' or values[0][0]=='R' or values[0][0]=='C':
        voltageSquared=pow(abs(voltage[node1]-voltage[node2]),2)
        power_S=voltageSquared/(2*impedance_z)
    f.write("Power("+str(values[0])+")="+str(power_S)+"\n")
#closing the file
f.close()
print("Result is now produced in a txt file : result.txt")
print("Please enter any key to exit")
input()

