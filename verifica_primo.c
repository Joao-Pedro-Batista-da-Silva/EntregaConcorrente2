#include <stdio.h>
#include <stdlib.h> 
#include <pthread.h>
#include <math.h>
#include "timer.h"


long long int N;
long long int n=1;
pthread_mutex_t mutex;


typedef struct{
    long int id;
    long int num_avaliados;
} tArgs;

int ehPrimo(long long int n){
    int i;
    if (n <= 1) return 0;
    if (n == 2) return 1;
    if (n%2 == 0)return 0;
    for(i = 3;i < sqrt(n)+1;i+=2){
        if(n%i == 0) return 0;    
    }
    return 1;
}

void *executaTarefa(void *arg){
    tArgs *args = (tArgs *) arg;
    long long int n_da_vez;
    //printf("\nentrei na thread %ld===============\n", args->id);
    while(n<=N){
        pthread_mutex_lock(&mutex);
        n_da_vez = n;
        n++;
        pthread_mutex_unlock(&mutex);
        if(n_da_vez>N){
            break;
        }
        //printf("%lld\n",n_da_vez);
        if(ehPrimo(n_da_vez)){
            //printf("thread %d: eh primo %lld\n", args->id, n_da_vez);
            args->num_avaliados++;    
        }
        //else printf("\nthread %d: %lld nao eh primo\n", args->id, n_da_vez);
    }
    //printf("\nsai da thread %ld===============\n", args->id);
    pthread_exit(NULL);
    return 0;
}



int main(int argc, char* argv[]){
    int nthreads;
    pthread_t *tid;
    tArgs *args;
    long long int total_primos = 0;
    double inicializacao, inicio, fim, delta, total=0;
    GET_TIME(inicio);
    if(argc<3){
        printf("\nERRO Argumentos inválidos\nPor favor coloque algo no formato:%s <N-tamanho da sequancia de 1 a N> <numero de threads>",argv[0]);
        return 1;
    }
    nthreads = atoi(argv[2]);
    //printf("nthreads:%d\n",nthreads);
    N = atoll(argv[1]); 
    tid = (pthread_t*) malloc(sizeof(pthread_t)*nthreads);
    if(tid == NULL){
        printf("\nERRO em alocação de memoria\n");
        return 2;
    }
    args = (tArgs *) malloc(sizeof(tArgs)*nthreads);
    if(args == NULL){
        printf("\nERRO na criação de argumentos");
        return 4;
    }
    GET_TIME(fim);
    inicializacao = fim-inicio;
    delta = inicializacao;
    total = delta;
    pthread_mutex_init(&mutex, NULL);
    GET_TIME(inicio);
    for(long int i = 0; i<nthreads;i++){
        (args+i)->id = i;
        (args+i)->num_avaliados=0;
        
        if(pthread_create(&tid[i],NULL, executaTarefa, (void *)(args+i))){
            printf("\nERRO ao criar a thread\n");
            return 3;
        }
    }
    
    for(int i = 0; i<nthreads;i++){
        if(pthread_join(tid[i],NULL)){
            printf("\nERRO ao dar join nas threads\n");
            return 4;
        }
        //printf("thread %d: %ld de %lld\n", i, (args+i)->num_avaliados,N);
        total_primos += (args+i)->num_avaliados;
    }
    GET_TIME(fim);
    printf("totalPrimos,tamanhoN,nthreads,inicializacao,processamento,finalizacao,total\n");
    printf("%lld,", total_primos);
    printf("%lld,",N);
    printf("%d, ", nthreads);
    printf("%f, ", inicializacao);
    delta = fim-inicio;
    printf("%f, ",delta);
    total += delta;
    GET_TIME(inicio);
    free(tid);
    free(args);
    GET_TIME(fim);
    delta = fim - inicio;
    printf("%f, ",delta);
    total += delta;
    printf("%f\n" ,total);
    pthread_mutex_destroy(&mutex);

    return 0;
}