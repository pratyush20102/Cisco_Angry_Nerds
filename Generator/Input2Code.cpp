#include <bits/stdc++.h>
using namespace std ;

long long binpow(long long a, long long b, long long m = 2e18) {
    a %= m;
    long long res = 1;
    while (b > 0) {
        if (b & 1)
            res = res * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return res;
}

int main(){
    int maxi = binpow(2, 16) - 1, rule_max = 500;
    for(int statements = 1; statements <= 10000; statements++){
        int u = rand()%maxi, v = rand()%maxi;
        int rule_rand = rand()%rule_max + 1;
        cout << "Cts role-based permissions from " << u << " to " << v << " rule_" << rule_rand << endl; 
    }
    return 0 ;
}
