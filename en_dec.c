//en_dec.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* en_dec(char* msg, char* key, int length);

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Uso: %s <messaggio> <chiave>\n", argv[0]);
        return 1;
    }

    int length = strlen(argv[1]);

    char *crypt = en_dec(argv[1], argv[2], length);

    printf("%s\n", crypt);

    free(crypt); // LIBERA memoria
    return 0;
}

char* en_dec(char* msg, char* key, int length) {
    char *cryptedmsg = malloc(length + 1); 


    for (int i = 0; i < length; i++) {
        cryptedmsg[i] = msg[i] ^ key[i];
    }
    cryptedmsg[length] = '\0'; 

    return cryptedmsg;
}
