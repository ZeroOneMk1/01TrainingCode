#include <cmath>
#include <iostream>
using namespace std;

int servoPins[2][3][3];
double tibia = 10.0;
double femur = 10.0;
double BCSQ = femur * femur + tibia * tibia;
double D2BC = 1/(2 * femur * tibia);
double BCSQD2BC = BCSQ * D2BC;

#define PI 3.14159265358

/*
  The first index gives the side of the robot, where LEFT = 0 RIGHT = 1

  The second index gives the leg of the side, where BACK = 0 FRONT = 2

  The third index gives the servo on the leg, where CLOSER = LOWER
*/
double calcFingerAngle(double desiredLength);

int main(){
    cout << calcFingerAngle(5.0) * 180.0 / PI << endl;
    return 0;
}

void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < 18; i++){
    servoPins[(i - i%9)/9][(i-i%3)/3][i%3] = i;
  }

}

void loop() {
  // put your main code here, to run repeatedly:

}

double calcFingerAngle(double desiredLength){
  return acos(BCSQD2BC - desiredLength * desiredLength * D2BC);
}