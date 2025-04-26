#!/bin/bash

tamanho_n=(1 10 100 200 500 1000 2000 5000 10000 100000 1000000)
threads=(1 2 4)
repeticoes=(1 2 3 4 5)         
echo "tamanhoN,nthreads,inicializacao,processamento,finalizacao,total"
for k in ${tamanho_n[@]}
do
    for i in ${threads[@]}
    do
        for j in ${repeticoes[@]}
        do
        ./a.out $k $i
        done
        echo ""
    done
done
