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
 * Motor channel:  Left  drive motor:        "left"
 * Motor channel:  Right drive motor:        "right"
 */

public class HardwareInit_5Motors
{
    /* Public OpMode members. */
    
    // Declare Motors and Servos
    public DcMotor  leftBack   = null;
    public DcMotor  rightBack  = null;
    public DcMotor  leftFront  = null;
    public DcMotor  rightFront = null;
    public DcMotor  lever      = null;
    
    
    // public Servo Finger = null;
    // public Servo Finger2 = null;
    

    /* local OpMode members. */
    HardwareMap hwMap           =  null;
    private ElapsedTime period  = new ElapsedTime();

    /* Constructor */
    public HardwareInit_5Motors(){

    }

    /* Initialize standard Hardware interfaces */
    public void init(HardwareMap ahwMap) {
        // Save reference to Hardware map
        hwMap = ahwMap;

        // Define and Initialize Motors
        leftBack    = hwMap.get(DcMotor.class, "left");
        rightBack   = hwMap.get(DcMotor.class, "right");
        lever   = hwMap.get(DcMotor.class, "lever");

        // Set direction of Motors
        leftBack.setDirection(DcMotor.Direction.REVERSE);
        rightBack.setDirection(DcMotor.Direction.FORWARD);
        lever.setDirection(DcMotor.Direction.FORWARD);

        // Set the 0 power behavior of motors
        leftBack.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rightBack.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        lever.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // Set all motors to zero power
        leftBack.setPower(0);
        rightBack.setPower(0);
        lever.setPower(0);

        // Set all motors to run without encoders.
        // May want to use RUN_USING_ENCODERS if encoders are installed.
        leftBack.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        rightBack.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        lever.setMode(DcMotor.RunMode.RUN_USING_ENCODER);//ENCODER?

        leftFront    = hwMap.get(DcMotor.class, "leftF");
        rightFront   = hwMap.get(DcMotor.class, "rightF");

        // Set direction of Motors
        leftFront.setDirection(DcMotor.Direction.REVERSE);
        rightFront.setDirection(DcMotor.Direction.FORWARD);

        // Set the 0 power behavior of motors
        leftFront.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rightFront.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // Set all motors to zero power
        leftFront.setPower(0);
        rightFront.setPower(0);

        // Set all motors to run without encoders.
        // May want to use RUN_USING_ENCODERS if encoders are installed.
        leftFront.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        rightFront.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?


       // Define and initialize ALL installed servos.
        // Finger  = hwMap.get(Servo.class, "Finger");
        // Finger2  = hwMap.get(Servo.class, "Finger2");
        // Finger.setPosition(0);
        // Finger2.setPosition(0);

    }
 }

