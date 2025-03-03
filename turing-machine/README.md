
# Turing Machine Calculator

Maquina de Turing capaz de realizar multiples calculos basicos de una calculadora para numeros binarios

## ¿Como funciona?
La máquina leerá la cinta y, según los símbolos que encuentre, realizará las operaciones entre los números binarios ingresados. **Es importante no incluir espacios en blanco**. La máquina procesará la cinta hasta encontrar el símbolo `=`, que indica el final de la expresión de lo contrario no funcionara. Para realizar múltiples operaciones en una misma cinta y garantizar el correcto orden de evaluación, se recomienda el uso de paréntesis para respetar la precedencia de las operaciones.



## operaciones

#### Ejemplos

| Operacion     | Entrada      | resultado  |
| ------------- | ------------ | ---------- |
| Suma | 100+11= | 111  |
| Resta | 100-11=| 1 |
| Multplicación | 11*10= | 110 |
| División | 110/10= | 11 |
| Raiz Cuadrada| 10000r= | 100 |
| Potencia | 10^11= | 1000 | 
| Modulo | 1100%11= | 0 |
| Multiples operaciones | ((101+11)*10/10)= | 1000 |

> [!NOTE]  
> Para facilidad de uso de la raiz cuadrada se usa `r` como simbolo.


## Ejecucion
Para probar el codigo es necesario descargar el archivo `main.py`. Para ejeturalo se debe abrir la terminal en caso de Linux y MacOS o un CMD en caso de windows en la ubicacion donde se descargo el archivo y ejecutar la sigiente linea:

```
~/ejemplo/de/ruta python main.py
```
Luego de esto aparecera un dialogo en la consola donde se podra ingresar la cinta con las operaciones.

Existen unos ejemplos dentro del codigo, es necesario comentar el `input` y descomentar el ejemplo deseado. El codigo deberia verse algo asi:

```python
# Ejemplos de uso:
#tape_input = "1100+101-11="  # (12 + 5 - 3) = 14 -> 1110
tape_input = "((1001+11)%11)="  # (9+3)%3 = 0 -> 0
#tape_input = "((101+11)*10/10)="  # ((5+3)*2/2) = 8 -> 1000

#tape_input = input("Ingrese la cinta: ")

tm = TuringMachine(tape_input)
tm.execute()
print("Resultado en la cinta:", tm.get_tape())
```
