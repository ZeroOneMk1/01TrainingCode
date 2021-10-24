package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.OpMode;
import org.firstinspires.ftc.robotcore.external.Telemetry;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.util.Hardware;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.util.ElapsedTime;
import com.qualcomm.robotcore.util.Range;
import java.lang.Math;

@TeleOp(name = "Pushbot: Teleop Mechanum", group = "Pushbot")
//@Disabled
public class PushbotTeleopTank_Iterative extends OpMode {

    /* Declare OpMode members. */
    HardwareInit robot = new HardwareInit(); // use the class created to define a Pushbot's hardware
    private ElapsedTime runtime = new ElapsedTime();

    double slowness = .3;

    private double leftSpeed = 0;
    private double rightSpeed = 0;

    @Override
    public void init() {
        robot.init(hardwareMap);
        telemetry.addData("Say", "Hello Driver");
    }

    @Override
    public void init_loop() {
    }

    @Override
    public void start() {
    }

    @Override
    public void loop() {
        
        //Data Types!
        
        //Integers 0, -1, 399, 53729, 1325, 003452, -9999, 38  (int)
        
        //Double 3.32570, (double)
        
        //Boolean True, false (boolean)
        
        //Strings  ->  "Banana", "Pineapple", "serjokgnnbwpi"  (String)
        
        //characters -> 'q', 'f'  (char)
        
        //maximum speed set to .3 so that the robot isnt too fast
        slowness = .3;
        
        //maximum speed increases to .8 when  left stick is held
        if(gamepad1.left_stick_button){
            slowness = .8;
        }

        //Single stick drive variable allocation
        double drive = - gamepad1.left_stick_y;
        double side = gamepad1.left_stick_x;

    
        // Calculating motor power from input
        leftSpeed = drive * slowness + side * slowness;
        rightSpeed = drive * slowness - side * slowness;

        /** Stopping Joycon Drift */

        if(leftSpeed < .1 && leftSpeed > -.1){
            leftSpeed = 0;
        }
        if(rightSpeed < .1 && rightSpeed > -.1){
            rightSpeed = 0;
        }
        
        //Setting motor power values to variable values

        robot.leftDrive.setPower(leftSpeed);
        robot.rightDrive.setPower(rightSpeed);
        
        /* Telemetry is output onto the phone */
        
        telemetry.addData("Left", "%.2f", robot.leftDrive.getPower());
        telemetry.addData("Right", "%.2f", robot.rightDrive.getPower());
        telemetry.addData("Max Speed", "%.2f", slowness);
    }

    @Override
    public void stop() {
    }
}
