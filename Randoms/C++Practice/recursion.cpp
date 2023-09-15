#include <iostream>

using namespace std;

unsigned long fact(unsigned long number);

int main(){
    unsigned long int num;

    cin >> num;
    if (num > 20)
    {
        cout << "The number is too big, sorry." << endl;
    }
    else
    {
        unsigned long l = fact(num);
        cout << l << endl;
    }
}

unsigned long fact(unsigned long number)
{
    if (number <= 1)
    {
        return 1;
    }
    else
    {
        return number * fact(number - 1);
    }
}