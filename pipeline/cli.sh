#!/bin/bash

echo "Escriba el numero de experimento para ejecutar:"
echo "1 - Ejecutar pipeline con funcion de pesos"
echo "2 - Ejecutar pipeline reemplazando atributo RevLen por Entropy"
echo "3 - Ejecutar pipeline con evaluacion de bias"
echo "4 - Ejecutar pipeline con mitigacion de bias"

read experiment

echo "Escriba la precision decimal a utilizar (1.0, 0.1, 0.01, 0.001)"

read decimalPrecision


if [ "$decimalPrecision" = "1.0" ] || [ "$decimalPrecision" = "0.1" ] || [ "$decimalPrecision" = "0.01" ] || [ "$decimalPrecision" = "0.001" ] 
then
	if  [ "$experiment" = "1" ] || [ "$experiment" = "2" ] || [ "$experiment" = "3" ] || [ "$experiment" = "4" ]
	then
		time bash script.sh $experiment $decimalPrecision
	else
		echo "El numero de experimento es invalida. Elija entre los valores (1,2,3,4)"
	fi
else
	echo "La precision decimal es invalida. Elija entre los valores (1.0, 0.1, 0.01, 0.001)"
fi

