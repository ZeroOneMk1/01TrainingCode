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

public class HardwareInit4Wheel
{
    /* Public OpMode members. */
    
    // Declare Motors and Servos
    public DcMotor  lbDrive   = null;
    public DcMotor  rbDrive  = null;
    public DcMotor  lfDrive   = null;
    public DcMotor  rfDrive  = null;
    
    
    // public Servo Finger = null;
    // public Servo Finger2 = null;
    

    /* local OpMode members. */
    HardwareMap hwMap           =  null;
    private ElapsedTime period  = new ElapsedTime();

    /* Constructor */
    public HardwareInit4Wheel(){

    }

    /* Initialize standard Hardware interfaces */
    public void init(HardwareMap ahwMap) {
        // Save reference to Hardware map
        hwMap = ahwMap;

        // Define and Initialize Motors
        lbDrive    = hwMap.get(DcMotor.class, "leftBackMotor");
        rbDrive   = hwMap.get(DcMotor.class, "rightBackMotor");
        lfDrive   = hwMap.get(DcMotor.class, "leftFrontMotor");
        rfDrive   = hwMap.get(DcMotor.class, "rightFrontMotor");

        // Set direction of Motors
        lbDrive.setDirection(DcMotor.Direction.REVERSE);
        rbDrive.setDirection(DcMotor.Direction.FORWARD);

        // Set the 0 power behavior of motors
        lbDrive.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rbDrive.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // Set all motors to zero power
        lbDrive.setPower(0);
        rbDrive.setPower(0);

        // Set all motors to run without encoders.
        // May want to use RUN_USING_ENCODERS if encoders are installed.
        lbDrive.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        rbDrive.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?

        lfDrive.setDirection(DcMotor.Direction.REVERSE);
        rfDrive.setDirection(DcMotor.Direction.FORWARD);

        // Set the 0 power behavior of motors
        lfDrive.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
        rfDrive.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);

        // Set all motors to zero power
        lfDrive.setPower(0);
        rfDrive.setPower(0);

        // Set all motors to run without encoders.
        // May want to use RUN_USING_ENCODERS if encoders are installed.
        lfDrive.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?
        rfDrive.setMode(DcMotor.RunMode.RUN_WITHOUT_ENCODER);//ENCODER?


       // Define and initialize ALL installed servos.
        // Finger  = hwMap.get(Servo.class, "Finger");
        // Finger2  = hwMap.get(Servo.class, "Finger2");
        // Finger.setPosition(0);
        // Finger2.setPosition(0);

    }
 }

