#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char other_buf[0x100];

int get_int() {
    char buf[0x10];
    fgets(buf, 10, stdin);
    return atoi(buf);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    int c;
    char buf[0x100];
    printf("Choose a name\n");
    printf("1. Chamber 2. Cypher 3. Killjoy\n");
    printf("Choice: ");
    c = get_int();

    if (c == 2) {
        puts("Nice job. Here is your gift.");
        /*fgets(buf, 0x100, stdin);*/
        int n = read(0, buf, 0x100);
        snprintf(other_buf, 0x100, buf);
        system("echo 'Cypher, the real sentinel'");
    }
}
