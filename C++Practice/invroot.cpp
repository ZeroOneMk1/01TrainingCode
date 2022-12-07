#include <iostream>
#include <math.h>
#include <chrono>

using namespace std;

float Q_sqrt(float number);

int main(){
    int sumn = 0;
    int sumq = 0;
    float sumdiffs = 0.f;

    for(float testnum = 0.001f; testnum <= 5.0f; testnum += 0.001f){

        chrono::high_resolution_clock::time_point startn = chrono::high_resolution_clock::now();

        float inv = 1 / sqrt(testnum);

        chrono::high_resolution_clock::time_point stopn = chrono::high_resolution_clock::now();

        float qinv = Q_sqrt(testnum);

        chrono::high_resolution_clock::time_point stopq = chrono::high_resolution_clock::now();

        chrono::high_resolution_clock::duration durationn = chrono::duration_cast<chrono::nanoseconds>(stopn - startn);
        chrono::high_resolution_clock::duration durationq = chrono::duration_cast<chrono::nanoseconds>(stopq - stopn);

        sumdiffs += abs(qinv/inv - 1);

        sumn += durationn.count();
        sumq += durationq.count();
        
    }

    int avgn = sumn / 5000;
    int avgq = sumq / 5000;
    float avgdiff = sumdiffs / 5000.0;

    // cout << "I can use this to recreate the quake algorithm and finally understand it. I'll use the number " << testnum << endl;

    cout << "After 5000 trials, the normal inverse took on average " << avgn << " nanoseconds, and the quake took " << avgq << " nanoseconds" << endl << "The difference was on average " << avgdiff * 100.f << "%" << endl;
}

float Q_sqrt(float number){
    long i;
    float x2, y;
    const float threehalfs = 1.5F;

    x2 = number * 0.5F;
    y = number;
    i = * (long *) &y;
    i = 0x5f3759df - ( i >> 1 );
    y = * (float *) &i;
    y = y * ( threehalfs - ( x2 * y * y ) );
    y = y * ( threehalfs - (x2 * y * y));

    return abs(y);
}