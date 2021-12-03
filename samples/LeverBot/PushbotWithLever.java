package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.OpMode;
import org.firstinspires.ftc.robotcore.external.Telemetry;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.util.Hardware;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.util.ElapsedTime;
import com.qualcomm.robotcore.util.Range;
import java.lang.Math;

@TeleOp(name = "Leverbot: Teleop", group = "LeverBot")
//@Disabled
public class PushbotWithLever extends OpMode {

    /* Declare OpMode members. */
    HardwareInit_3Motors robot = new HardwareInit_3Motors(); // use the class created to define a Pushbot's hardware
    private ElapsedTime runtime = new ElapsedTime();

    static final double     COUNTS_PER_MOTOR_REV    = 1440 ;    // eg: TETRIX Motor Encoder
    static final double     DRIVE_GEAR_REDUCTION    = 2.0 ;     // This is < 1.0 if geared UP
    static final double     WHEEL_DIAMETER_INCHES   = 4.0 ;     // For figuring circumference
    static final double     COUNTS_PER_INCH         = (COUNTS_PER_MOTOR_REV * DRIVE_GEAR_REDUCTION) /
                                                      (WHEEL_DIAMETER_INCHES * 3.1415);
    static final double     ROBOT_CIRCUMFERENCE     = 4.0;
    static final double     DRIVE_SPEED             = 0.6;
    static final double     TURN_SPEED              = 0.5;
    static final double     GEAR_RATIO              = 3.0;

    double slowness = .3;
    double leverslow = .3;

    private double leftSpeed = 0;
    private double rightSpeed = 0;
    private double leverSpeed = 0;

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
        
        //maximum speed increases to .8 when  left stick is held
        if(gamepad1.left_stick_button){
            slowness = .8;
        }else{
            slowness = .3;
        }
        
        if(gamepad1.right_stick_button){
            leverslow = .3;
        }else{
            leverslow = .1;
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
        
        if(gamepad1.b){
            encoder_lift_lever(1, -5, 2);
        }else if (gamepad1.a){
            encoder_lift_lever(1, 5, 2);
        }
        
        leverSpeed = gamepad1.right_stick_y * leverslow;
        
        


        //Setting motor power values to variable values

        robot.leftDrive.setPower(leftSpeed);
        robot.rightDrive.setPower(rightSpeed);
        robot.lever.setPower(leverSpeed);
        
        /* Telemetry is output onto the phone */
        
        telemetry.addData("Left", "%.2f", robot.leftDrive.getPower());
        telemetry.addData("Right", "%.2f", robot.rightDrive.getPower());
        telemetry.addData("Max Speed", "%.2f", slowness);
    }

    @Override
    public void stop() {
    }

    public void encoder_lift_lever(double speed, double degrees, double timeoutS){
        if(!robot.lever.isBusy()){
            int newLiftTarget;

            double rotationsIntended = degrees / 360;

            double rotationsMotor = rotationsIntended /* GEAR_RATIO*/;

            double target = rotationsMotor * COUNTS_PER_MOTOR_REV;

            // Ensure that the opmode is still active

            // Determine new target position, and pass to motor controller
            newLiftTarget = robot.lever.getCurrentPosition() + (int)(target);
            robot.lever.setTargetPosition(newLiftTarget);

            // Turn On RUN_TO_POSITION
            robot.lever.setMode(DcMotor.RunMode.RUN_TO_POSITION);

            // reset the timeout time and start motion.
            runtime.reset();
            robot.lever.setPower(Math.abs(speed));

            // keep looping while we are still active, and there is time left, and both motors are running.
            // Note: We use (isBusy() && isBusy()) in the loop test, which means that when EITHER motor hits
            // its target position, the motion will stop.  This is "safer" in the event that the robot will
            // always end the motion as soon as possible.
            // However, if you require that BOTH motors have finished their moves before the robot continues
            // onto the next step, use (isBusy() || isBusy()) in the loop test.
            while ((runtime.seconds() < timeoutS) &&
                    (robot.lever.isBusy())) {

                // Display it for the driver.
                telemetry.addData("Path1",  "Running to %7d", newLiftTarget);
                telemetry.addData("Path2",  "Running at %7d",
                                            robot.lever.getCurrentPosition());
                telemetry.update();
            }

            // Stop all motion;
            robot.lever.setPower(0);

            // Turn off RUN_TO_POSITION
            robot.lever.setMode(DcMotor.RunMode.RUN_USING_ENCODER);
        }

    }
}
