gcc -c -Wall -Werror -fpic universal_kepler.c
gcc -shared -o libuniversal_kepler.so universal_kepler.o
