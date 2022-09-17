#include <cmath>
#include <iostream>
#include <chrono>
#include <unistd.h>
using namespace std;

#define PI 3.14159265358

int servoPins[2][3][3];
double servoDestinations[2][3][3];
double servoAngles[2][3][3];
/*
  The first index gives the side of the robot, where LEFT = 0 RIGHT = 1

  The second index gives the leg of the side, where BACK = 0 FRONT = 2

  The third index gives the servo on the leg, where CLOSER = LOWER
*/
static double tibia = 10.0;
static double femur = 10.0;
static double coaxia = 10.0;
static double BCSQ = femur * femur + tibia * tibia;
static double D2BC = 1/(femur * tibia)* 0.5;
static double BCSQD2BC = BCSQ * D2BC;
static int QUARTERWALKCYCLE = 250000; //THIS IS A GUESS. IT ASSUMES IT TAKES 1 SECOND TO TAKE ONE STEP.

static double horizOffset = 10.0;
static double vertOffset = 10.0;

static double desiredHeight = 5.0;
static double legLift = 1.0;

static double maxExtension = coaxia + sqrt((femur + tibia)*(femur + tibia) - desiredHeight * desiredHeight);

static double walkAngleDeg = 20; // In degrees!
static double walkAngle = walkAngleDeg / 180 * PI;
static double coAngle = (walkAngleDeg + 45)/180 * PI;
static double radToDeg = 1 / PI * 180;

static double gaitXCorner = maxExtension * cos(coAngle);
static double gaitY1 = maxExtension * sin(coAngle);
static double gaitY2 = gaitXCorner / sin(coAngle) * sin(walkAngle);

static double extendedCornerLeg[] = {gaitXCorner, gaitY1, -desiredHeight};
static double centerCornerLeg[] = {gaitXCorner, (gaitY1 + gaitY2)/2, -desiredHeight};
static double contractedCornerLeg[] = {gaitXCorner, gaitY2, -desiredHeight};

static double gaitXCenter = cos(walkAngle) * maxExtension;
static double gaitYCenter = sin(walkAngle) * maxExtension;

static double extendedCenterLeg[] = {gaitXCenter, gaitYCenter, -desiredHeight};
static double centerCenterLeg[] = {gaitXCenter, 0, -desiredHeight};
static double contractedCenterLeg[] = {gaitXCenter, -gaitYCenter, -desiredHeight};

enum State {walking, reversing, turning, idle, returning};

State state_;

// WARNING: I NEVER TESTED THE FLIPPING. THIS MAY MESS UP IN THE FUTURE. WATCH OUT FOR YOUR FINGERS!

int walkingTimeCounter = 0;
auto startedWalkingTime = chrono::high_resolution_clock::now();
auto startWalking();
void stopWalking();

void normalizeDesiredPos(int legIndex, double* desiredPos);

double calcFingerAngle(double desiredLength);

void calcAngles(double* normalizedDesiredToesPos, double* angles);

void rotateZ(double* vector, double theta, bool flip);

bool inEnvelope(double* normalizedDesiredPos);

int main(){
  // double angles[3];
  // double destoespos[] = {20.0, 20.0, 19.0};

  // normalizeDesiredPos(5, destoespos);

  // if (inEnvelope(destoespos)){
  //   calcAngles(destoespos, angles);

  //   cout << "Final Angles: [" << angles[0] << ", " << angles[1] << ", "<< angles[2] << "]" << endl;
  // }else{
  //   cout << "Outside of Envelope" << endl;
  // }

  startWalking();
  while(true){
    loop();
  }

  
  return 0;
}

void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < 18; i++){
    servoPins[(i - i%9)/9][(i-i%3)/3][i%3] = i;
  }

  state_ = idle;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  switch(state_){
    case(returning):

    case(idle):

    case(walking):
      walkingTimeCounter = chrono::duration_cast<chrono::microseconds>(chrono::high_resolution_clock::now() - startedWalkingTime).count();
      if((walkingTimeCounter - walkingTimeCounter%QUARTERWALKCYCLE)/QUARTERWALKCYCLE % 4 == 0){
        servoDestinations[0][0][0] = -centerCornerLeg[0];
        servoDestinations[0][0][1] = -centerCornerLeg[1];
        servoDestinations[0][0][2] = centerCornerLeg[2] + legLift;

        servoDestinations[0][1][0] = -centerCenterLeg[0];
        servoDestinations[0][1][1] = centerCenterLeg[1];
        servoDestinations[0][1][2] = centerCenterLeg[2];

        servoDestinations[0][2][0] = -centerCornerLeg[0];
        servoDestinations[0][2][1] = centerCornerLeg[1];
        servoDestinations[0][2][2] = centerCornerLeg[2] + legLift;

        servoDestinations[1][0][0] = centerCornerLeg[0];
        servoDestinations[1][0][1] = -centerCornerLeg[1];
        servoDestinations[1][0][2] = centerCornerLeg[2];

        servoDestinations[1][1][0] = centerCenterLeg[0];
        servoDestinations[1][1][1] = centerCenterLeg[1];
        servoDestinations[1][1][2] = centerCenterLeg[2] + legLift;

        servoDestinations[1][2][0] = centerCornerLeg[0];
        servoDestinations[1][2][1] = centerCornerLeg[1];
        servoDestinations[1][2][2] = centerCornerLeg[2];

      } else if((walkingTimeCounter - walkingTimeCounter%QUARTERWALKCYCLE)/QUARTERWALKCYCLE % 4 == 1){

        servoDestinations[0][0][0] = -contractedCornerLeg[0];
        servoDestinations[0][0][1] = -centerCornerLeg[1];
        servoDestinations[0][0][2] = contractedCornerLeg[2];

        servoDestinations[0][1][0] = -contractedCenterLeg[0];
        servoDestinations[0][1][1] = contractedCenterLeg[1];
        servoDestinations[0][1][2] = contractedCenterLeg[2];

        servoDestinations[0][2][0] = -extendedCornerLeg[0];
        servoDestinations[0][2][1] = extendedCornerLeg[1];
        servoDestinations[0][2][2] = extendedCornerLeg[2];

        servoDestinations[1][0][0] = extendedCornerLeg[0];
        servoDestinations[1][0][1] = -extendedCornerLeg[1];
        servoDestinations[1][0][2] = extendedCornerLeg[2];

        servoDestinations[1][1][0] = extendedCenterLeg[0];
        servoDestinations[1][1][1] = extendedCenterLeg[1];
        servoDestinations[1][1][2] = extendedCenterLeg[2];

        servoDestinations[1][2][0] = contractedCornerLeg[0];
        servoDestinations[1][2][1] = contractedCornerLeg[1];
        servoDestinations[1][2][2] = contractedCornerLeg[2];
      }else if((walkingTimeCounter - walkingTimeCounter%QUARTERWALKCYCLE)/QUARTERWALKCYCLE % 4 == 2){

        servoDestinations[0][0][0] = -centerCornerLeg[0];
        servoDestinations[0][0][1] = -centerCornerLeg[1];
        servoDestinations[0][0][2] = centerCornerLeg[2];

        servoDestinations[0][1][0] = -centerCenterLeg[0];
        servoDestinations[0][1][1] = centerCenterLeg[1];
        servoDestinations[0][1][2] = centerCenterLeg[2] + legLift;

        servoDestinations[0][2][0] = -centerCornerLeg[0];
        servoDestinations[0][2][1] = centerCornerLeg[1];
        servoDestinations[0][2][2] = centerCornerLeg[2];

        servoDestinations[1][0][0] = centerCornerLeg[0];
        servoDestinations[1][0][1] = -centerCornerLeg[1];
        servoDestinations[1][0][2] = centerCornerLeg[2] + legLift;

        servoDestinations[1][1][0] = centerCenterLeg[0];
        servoDestinations[1][1][1] = centerCenterLeg[1];
        servoDestinations[1][1][2] = centerCenterLeg[2];

        servoDestinations[1][2][0] = centerCornerLeg[0];
        servoDestinations[1][2][1] = centerCornerLeg[1];
        servoDestinations[1][2][2] = centerCornerLeg[2] + legLift;
      }else{
        servoDestinations[0][0][0] = -extendedCornerLeg[0];
        servoDestinations[0][0][1] = -extendedCornerLeg[1];
        servoDestinations[0][0][2] = extendedCornerLeg[2];

        servoDestinations[0][1][0] = -contractedCornerLeg[0];
        servoDestinations[0][1][1] = contractedCornerLeg[1];
        servoDestinations[0][1][2] = contractedCornerLeg[2];

        servoDestinations[0][2][0] = -extendedCornerLeg[0];
        servoDestinations[0][2][1] = extendedCornerLeg[1];
        servoDestinations[0][2][2] = extendedCornerLeg[2];

        servoDestinations[1][0][0] = contractedCornerLeg[0];
        servoDestinations[1][0][1] = -contractedCornerLeg[1];
        servoDestinations[1][0][2] = contractedCornerLeg[2];

        servoDestinations[1][1][0] = contractedCenterLeg[0];
        servoDestinations[1][1][1] = contractedCenterLeg[1];
        servoDestinations[1][1][2] = contractedCenterLeg[2];

        servoDestinations[1][2][0] = extendedCornerLeg[0];
        servoDestinations[1][2][1] = extendedCornerLeg[1];
        servoDestinations[1][2][2] = extendedCornerLeg[2];
      }


      for(int i = 0; i < 6; i++){
        normalizeDesiredPos(i, servoDestinations[(i - i%3)/3][i%3]);
        if (inEnvelope(servoDestinations[(i - i%3)/3][i%3])){
          calcAngles(servoDestinations[(i - i%3)/3][i%3], servoAngles[(i - i%3)/3][i%3]);

          cout << "Final Angles for Leg " << i << ": [" << servoAngles[(i - i%3)/3][i%3][0] << ", " << servoAngles[(i - i%3)/3][i%3][1] << ", "<< servoAngles[(i - i%3)/3][i%3][2] << "]" << endl;
        }else{
          cout << "Leg " << i << "OUTSIDE OF ENVELOPE:" << endl << "Final Angles for Leg " << i << ": [" << servoAngles[(i - i%3)/3][i%3][0] << ", " << servoAngles[(i - i%3)/3][i%3][1] << ", "<< servoAngles[(i - i%3)/3][i%3][2] << "]" << endl;
        }
      }

      sleep(10);

      //TODO: ADD THE PART THAT TELLS THE SERVOS WHERE TO GO PHYSICALLY WITHOUT FORGETTING CONVERSION FACTOR AND ANGLE CONVERSIONS.

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

auto startWalking(){
  walkingTimeCounter = 0;
  state_ = walking;
  startedWalkingTime = chrono::high_resolution_clock::now();
}

void stopWalking(){
  walkingTimeCounter = 0;
  state_ = idle;
}
