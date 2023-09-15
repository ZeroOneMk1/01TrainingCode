#include <iostream>

using namespace std;

int main() {

    unsigned long num = 3797864567;

    cout << "This is the number itself: " << num << endl;

    unsigned long* mem = &num;

    cout << "This is the memory address of the number: " << mem << endl;

    unsigned long test = *mem;

    cout << "This is the de-referenced value of the reference mem, which is the original value of num: " << test << endl;

    cout << "So if I have a memory address, I need to DEREFERENCE using *, and if I want the memory address, I need to pass in the REFERENCE using &." << endl;

    *mem = 6;

    cout << "And if I edit the DEREFERENCED value of mem, I can change num wihtout directly calling it: " << num << endl;

    unsigned long memCast = (unsigned long) mem;

    cout << "I can also cast the value of the memory address to edit it: " << memCast << endl;

    float hack = * (float *) mem;

    cout << "I can also change the type of the bit representation of a value to f.e. a float: " << hack << endl;

    cout << "I can also change consts for some reason. A big reason to check for boundaries." << endl;

    const long varOne = 10;
    long varTwo = 20;

    long * varTwoPtr = &varTwo;

    // cout << sizeof(varOne) << endl << sizeof(varOnePtr) << endl;

    long memdiff = ((long) &varOne - (long) &varTwo)/8;

    cout << &varOne << endl << &varTwo << endl << memdiff << endl;

    cout << varTwoPtr[memdiff] << endl;

    varTwoPtr[memdiff] += 1;

    cout << varTwoPtr[memdiff] << endl;

    return 0;
}