#!/bin/bash

tamanho_n=(1000 1000000)
threads=(1 2 4)
repeticoes=(1 2 3 4 5)         
for k in ${tamanho_n[@]}
do
    for i in ${threads[@]}
    do
        for j in ${repeticoes[@]}
        do
        ./a.out $k $i
        done
    done
done
