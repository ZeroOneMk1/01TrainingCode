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

public class HardwareInit
{
    /* Public OpMode members. */
    
    // Declare Motors and Servos
    public DcMotor  leftDrive   = null;
    public DcMotor  rightDrive  = null;
    
    
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
        leftDrive    = hwMap.get(DcMotor.class, "left");
        rightDrive   = hwMap.get(DcMotor.class, "right");

        // Set direction of Motors
        leftDrive.setDirection(DcMotor.Direction.REVERSE);
        rightDrive.setDirection(DcMotor.Direction.FORWARD);

        // Set the 0 power behavior of motors
        leftDrive.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rightDrive.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // Set all motors to zero power
        leftDrive.setPower(0);
        rightDrive.setPower(0);

        // Set all motors to run without encoders.
        // May want to use RUN_USING_ENCODERS if encoders are installed.
        leftDrive.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        rightDrive.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?


       // Define and initialize ALL installed servos.
        // Finger  = hwMap.get(Servo.class, "Finger");
        // Finger2  = hwMap.get(Servo.class, "Finger2");
        // Finger.setPosition(0);
        // Finger2.setPosition(0);

    }
 }

