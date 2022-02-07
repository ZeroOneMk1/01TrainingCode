package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.OpMode;
import org.firstinspires.ftc.robotcore.external.android.AndroidTextToSpeech;
import org.firstinspires.ftc.robotcore.external.Telemetry;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.util.Hardware;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.util.ElapsedTime;
import com.qualcomm.robotcore.util.Range;
import java.lang.Math;

@TeleOp(name = "Leverbot: Teleop 4 Wheel", group = "LeverBot")
//@Disabled
public class PushbotWithLever4Wheel extends OpMode {

    /* Declare OpMode members. */
    HardwareInit_5Motors robot = new HardwareInit_5Motors(); // use the class created to define a Pushbot's hardware
    private ElapsedTime runtime = new ElapsedTime();
    private AndroidTextToSpeech androidTextToSpeech;

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
        androidTextToSpeech = new AndroidTextToSpeech();
        androidTextToSpeech.initialize();
    }

    @Override
    public void init_loop() {
    }

    @Override
    public void start() {
        androidTextToSpeech.speak("Get ready for an ass-whooping!");
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
        
        // if(gamepad1.b){
        //     encoder_lift_lever(1, -0.9, 1);
        // }else if (gamepad1.a){
        //     encoder_lift_lever(1, 0.9, 1);
        // }

        if(gamepad1.x){
            androidTextToSpeech.speak("oo woo!"); //says uwu
        }else if(gamepad1.y){
            androidTextToSpeech.speak("oh woe!"); //says owo
        }else if(gamepad1.right_bumper){
            androidTextToSpeech.speak("poggers!");
        }else if(gamepad1.left_bumper){
            androidTextToSpeech.speak("get forked!");
        }else if(gamepad1.a){
            androidTextToSpeech.speak("Awooga!");
        }else if(gamepad1.b){
            androidTextToSpeech.speak("Help me stepbro, I'm stuck!");
        }
        
        leverSpeed = gamepad1.right_stick_y * leverslow;

        //Setting motor power values to variable values

        robot.leftBack.setPower(leftSpeed);
        robot.rightBack.setPower(rightSpeed);
        robot.leftFront.setPower(leftSpeed);
        robot.rightFront.setPower(rightSpeed);
        robot.lever.setPower(leverSpeed);
        
        /* Telemetry is output onto the phone */
        
        telemetry.addData("leftBack", "%.2f", robot.leftBack.getPower());
        telemetry.addData("rightBack", "%.2f", robot.rightBack.getPower());
        telemetry.addData("leftFront", "%.2f", robot.leftFront.getPower());
        telemetry.addData("rightFront", "%.2f", robot.rightFront.getPower());
        telemetry.addData("lever", "%.2f", robot.lever.getPower());
        telemetry.addData("Max Speed", "%.1f", slowness);
        
    }

    @Override
    public void stop() {
        androidTextToSpeech.speak("GG EASY!");
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
