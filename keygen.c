#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[]){
    srand(time(NULL));
    int keylen=strlen(argv[1]);
    char key [keylen+1];
    keygen(keylen,key);
    printf("%s", key);
    return 0;

}

void keygen(int keylen,char key[]){
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int charset_size = strlen(charset);
    for(unsigned int i=0;i<keylen;i++){
        int random_index = rand() % charset_size;  
        key[i] = charset[random_index];
    }
    key[keylen]='\0';

}
