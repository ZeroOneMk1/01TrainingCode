#include <iostream>

using namespace std;

int* ptreturn(int number);
int* ptreturnNoNew(int number);

int main()
{
    int* ptr = ptreturn(4);

    cout << ptr << endl << *ptr << endl << "----" << endl;

    delete ptr;

    int* ptrtwo = ptreturnNoNew(8);

    cout << ptrtwo << endl << *ptrtwo << endl;

    return 0;
}

int* ptreturn(int number){
    int i = number;
    int* numcopy = new int;
    *numcopy = i;
    return numcopy;
}
int* ptreturnNoNew(int number){
    int numcopy = number;
    return &numcopy;
}
