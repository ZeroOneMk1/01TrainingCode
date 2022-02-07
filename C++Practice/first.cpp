#include <iostream>
#include <array>

using namespace std;

long fact(long number)
{
    if(number <= 1)
    {
        return 1;
    }
    else
    {
        return number * fact(number - 1);
    }
}

void printall(string arr[20])
{
    
    for(int i = 0; i < 20; i++) {
        cout << arr[i] << endl;
    }
    
}

int main()
{
    cout << "Hello, world.\n";
    long num;
    cin >> num;
    if(num > 20)
    {
        cout << "The number is too big, sorry." << endl;
    }
    else
    {
        long l = fact(num);
        string str = to_string(l);
        cout << str << endl;
    }

    string thearr[20] = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"};

    // printall(thearr);

    string anotherarr[20];

    printall(anotherarr);

    return 0;
}