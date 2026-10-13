/* Recherche dichotomique dans un tableau trié */
#include <stdio.h>
#define TAILLE 8

int dichotomie(const int *t, int n, int x) {
    int g = 0, d = n - 1;
    while (g <= d) {
        int m = (g + d) / 2;
        if (t[m] == x) return m;
        if (t[m] < x) g = m + 1; else d = m - 1;
    }
    printf("absent : %d\n", x);
    return -1;
}
