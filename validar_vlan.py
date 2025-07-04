vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN pertenece al rango NORMAL.")
elif 1006 <= vlan <= 4094:
    print("La VLAN pertenece al rango EXTENDIDO.")
else:
    print("Número de VLAN fuera de rango válido (1-4094).")
