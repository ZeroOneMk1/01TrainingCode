#include <cmath>
#include <iostream>
#include <chrono>
using namespace std;

#define PI 3.14159265358

int servoPins[2][3][3];
/*
  The first index gives the side of the robot, where LEFT = 0 RIGHT = 1

  The second index gives the leg of the side, where BACK = 0 FRONT = 2

  The third index gives the servo on the leg, where CLOSER = LOWER
*/
double tibia = 10.0;
double femur = 10.0;
double coaxia = 10.0;
double BCSQ = femur * femur + tibia * tibia;
double D2BC = 1/(femur * tibia)* 0.5;
double BCSQD2BC = BCSQ * D2BC;

double horizOffset = 10.0;
double vertOffset = 10.0;

double desiredHeight = 5.0;

double maxExtension = coaxia + sqrt((femur + tibia)*(femur + tibia) - desiredHeight * desiredHeight);

double walkAngleDeg = 20; // In degrees!
double walkAngle = walkAngleDeg / 180 * PI;
double coAngle = (walkAngleDeg + 45)/180 * PI;

double gaitXCorner = maxExtension * cos(coAngle);
double gaitY1 = maxExtension * sin(coAngle);
double gaitY2 = gaitXCorner / sin(coAngle) * sin(walkAngle);

double extendedCornerLeg[] = {gaitXCorner, gaitY1, -desiredHeight};
double contractedCornerLeg[] = {gaitXCorner, gaitY2, -desiredHeight};

double gaitXCenter = cos(walkAngle) * maxExtension;
double gaitYCenter = sin(walkAngle) * maxExtension;

double extendedCenterLeg[] = {gaitXCenter, gaitYCenter, -desiredHeight};
double contractedCenterLeg[] = {gaitXCenter, -gaitYCenter, -desiredHeight};

enum State {walking, reversing, turning, idle, returning};

State state_;

// WARNING: I NEVER TESTED THE FLIPPING. THIS MAY MESS UP IN THE FUTURE. WATCH OUT FOR YOUR FINGERS!


void normalizeDesiredPos(int legIndex, double* desiredPos);

double calcFingerAngle(double desiredLength);

void calcAngles(double* normalizedDesiredToesPos, double* angles);

void rotateZ(double* vector, double theta, bool flip);

bool inEnvelope(double* normalizedDesiredPos);

int main(){
  double angles[3];
  double destoespos[] = {20.0, 20.0, 19.0};

  normalizeDesiredPos(5, destoespos);

  if (inEnvelope(destoespos)){
    calcAngles(destoespos, angles);

    cout << "Final Angles: [" << angles[0] << ", " << angles[1] << ", "<< angles[2] << "]" << endl;
  }else{
    cout << "Outside of Envelope" << endl;
  }

  
  return 0;
}

void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < 18; i++){
    servoPins[(i - i%9)/9][(i-i%3)/3][i%3] = i;
  }

  state_ = returning;

}

void loop() {
  // put your main code here, to run repeatedly:
  switch(state_){
    case(returning):

    case(idle):

    case(walking):

    case(reversing):
    
    case(turning):
    
  }
}

void rotateZ(double* vector, double theta, bool flip){
  double tempvector[3];

  if(flip){
    tempvector[0] = -vector[0] * cos(theta) + vector[1] * sin(theta);
    tempvector[1] = vector[0] * sin(theta) + vector[1] * cos(theta);
    tempvector[2] = vector[2];
  }else{
    tempvector[0] = vector[0] * cos(theta) + vector[1] * sin(theta);
    tempvector[1] =-vector[0] * sin(theta) + vector[1] * cos(theta);
    tempvector[2] = vector[2];
  }

  vector[0] = tempvector[0];
  vector[1] = tempvector[1];
  vector[2] = tempvector[2];
}

bool inEnvelope(double* normalizedDesiredPos){
  double planarDistanceSQRD = normalizedDesiredPos[0] * normalizedDesiredPos[0] + normalizedDesiredPos[1] * normalizedDesiredPos[1];

  double angle = atan(normalizedDesiredPos[1]/normalizedDesiredPos[0]);
  double elbowPos[] = {normalizedDesiredPos[0] - coaxia * cos(angle), normalizedDesiredPos[1] - coaxia * sin(angle), normalizedDesiredPos[2]};
  double desiredArmPos[] = {sqrt(elbowPos[0] * elbowPos[0] + elbowPos[1] * elbowPos[1]), elbowPos[2]};

  double desLength = sqrt(desiredArmPos[0] * desiredArmPos[0] + desiredArmPos[1] * desiredArmPos[1]);

  if(normalizedDesiredPos[0] < 0){
    return false;
  }else if(planarDistanceSQRD < coaxia * coaxia){
    return false;
  }else if(desLength > femur + tibia){
    return false;
  }else if(normalizedDesiredPos[2] > 0){
    return false;
  }
  return true;
}

void normalizeDesiredPos(int legIndex, double* desiredPos){
  int legVec[] =  {(legIndex - legIndex % 3) / 3, legIndex % 3};

  int horizMult;
  int vertMult;


  if(legVec[0] == 0){
    horizMult = -1;
  }else{
    horizMult = 1;
  }
  if(legVec[1] == 0){
    vertMult = -1;
  }else if(legVec[1] == 1){
    vertMult = 0;
  }else{
    vertMult = 1;
  }

  double shoulderpos[] = {horizMult * horizOffset, vertMult * vertOffset};

  desiredPos[0] = desiredPos[0] - shoulderpos[0];
  desiredPos[1] = desiredPos[1] - shoulderpos[1];

  if(desiredPos[0] == 0){
    desiredPos[0] = 0.01;
  }
  if(desiredPos[1] == 0){
    desiredPos[1] = 0.01;
  }
  
  double theta;
  bool flip;

  if(legVec[0] == 1){
    flip = false;
  }else{
    flip = true;
  }
  
  if(legVec[1] == 1){
    theta = 0;
  }else if(legVec[1] == 0){
    theta = 7 * PI / 4;
  }else{
    theta = PI / 4;
  }

  rotateZ(desiredPos, theta, flip);
  
}


double calcFingerAngle(double desiredLength){
  return acos(BCSQD2BC - desiredLength * desiredLength * D2BC);
}

void calcAngles(double* normalizedDesiredToesPos, double* angles){
// Takes in a 3d position vector and an empty 3d vector and edits the empty vector to conntain the shoulder angle, elbow angle, and wrist angle
// 0 = X (LR), 1 = Y (FB), 2 = Z (UD)

// Angle 0 is between -90 and 90 degrees, angle 2 is between 0 and 180 degrees, and angle 3 is between 0 and 180 degrees

  angles[0] = atan(normalizedDesiredToesPos[1]/normalizedDesiredToesPos[0]);

  double elbowPos[] = {normalizedDesiredToesPos[0] - coaxia * cos(angles[0]), normalizedDesiredToesPos[1] - coaxia * sin(angles[0]), normalizedDesiredToesPos[2]};

  double desiredArmPos[] = {sqrt(elbowPos[0] * elbowPos[0] + elbowPos[1] * elbowPos[1]), elbowPos[2]};

  double desLength = sqrt(desiredArmPos[0] * desiredArmPos[0] + desiredArmPos[1] * desiredArmPos[1]);
  
  angles[2] = calcFingerAngle(desLength);

  angles[1] = PI / 2 - atan(desiredArmPos[1]/desiredArmPos[0]) - asin(tibia / desLength * sin(angles[2]));
}
