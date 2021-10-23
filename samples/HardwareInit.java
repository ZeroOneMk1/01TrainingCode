/* Copyright (c) 2017 FIRST. All rights reserved.
 *
 * COPY THIS CODE INTO YOUOR PRE-EXISTING HARDWAREINIT FILE
 */

package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.hardware.HardwareMap;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.util.ElapsedTime;

/**
 * This is NOT an opmode.
 *
 * This class can be used to define all the specific hardware for a single robot.
 * In this case that robot is a Pushbot.
 * See PushbotTeleopTank_Iterative and others classes starting with "Pushbot" for usage examples.
 *
 * This hardware class assumes the following device names have been configured on the robot:
 * Note:  All names are lower case and some have single spaces between words.
 *
 * Motor channel:  Left  drive motor:        "left_drive"
 * Motor channel:  Right drive motor:        "right_drive"
 * Motor channel:  Manipulator drive motor:  "left_arm"
 * Servo channel:  Servo to open left claw:  "left_hand"
 * Servo channel:  Servo to open right claw: "right_hand"
 */
public class HardwareInit
{
    /* Public OpMode members. */
    
    // Declare Motors and Servos
    public DcMotor  leftMotor   = null;
    public DcMotor  rightMotor  = null;
    
    
    // public Servo Finger = null;
    // public Servo Finger2 = null;



    /* local OpMode members. */
    HardwareMap hwMap           =  null;
    private ElapsedTime period  = new ElapsedTime();

    /* Constructor */
    public HardwareInit(){

    }

    /* Initialize standard Hardware interfaces */
    public void init(HardwareMap ahwMap) {
        // Save reference to Hardware map
        hwMap = ahwMap;

        // Define and Initialize Motors
        leftMotor    = hwMap.get(DcMotor.class, "left");
        rightMotor   = hwMap.get(DcMotor.class, "right");

        // Set direction of Motors
        leftMotor.setDirection(DcMotor.Direction.REVERSE);
        rightMotor.setDirection(DcMotor.Direction.FORWARD);

        // Set the 0 power behavior of motors
        leftMotor.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rightMotor.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // Set all motors to zero power
        leftMotor.setPower(0);
        rightMotor.setPower(0);

        // Set all motors to run without encoders.
        // May want to use RUN_USING_ENCODERS if encoders are installed.
        leftMotor.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        rightMotor.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?


       // Define and initialize ALL installed servos.
        // Finger  = hwMap.get(Servo.class, "Finger");
        // Finger2  = hwMap.get(Servo.class, "Finger2");
        // Finger.setPosition(0);
        // Finger2.setPosition(0);

    }
 }

