import numpy as np
def leer_adc_12bits(voltaje_entrada, v_ref=3.3):
"""
Simula la digitalización de un ADC de 12 bits (rango discreto 0 a 4095).
"""
# Validación de rango de seguridad física
if voltaje_entrada < 0.0 or voltaje_entrada > v_ref:
raise ValueError(f"Error de sobretensión: {voltaje_entrada}V fuera de rango (0 - {v_ref}V)")
# 12 bits = 2^12 - 1 = 4095 niveles discretos
niveles = 2**12 - 1
valor_digital = int(round((voltaje_entrada / v_ref) * niveles))
return valor_digital
if __name__ == "__main__":
print(f"Lectura a 1.65V: {leer_adc_12bits(1.65)} digital")