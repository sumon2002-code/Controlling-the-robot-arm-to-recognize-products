
#include <Servo.h>

Servo servo_z_axis;
Servo servo_x_axis;
Servo servo_y_axis;
Servo servo_clamp;

int x_axis_degree = 70; //chân xoay tăng là xoay trái hạ là xoay phải
int y_axis_degree = 130; //chân nâng trái tăng là nâng, hạ là xuống
int z_axis_degree = 55; //giảm là nâng lên, tăng là hạ
int clamp_degree = 130; // tăng là kẹp, giảm là thả


void setup() {
  Serial.begin(9600);
 
  servo_z_axis.attach(10);  
  servo_x_axis.attach(11);
  servo_y_axis.attach(9);
   servo_clamp.attach(6);
}

void loop() {
  controlWithJoystick();
  controlWithPython();
}

void controlWithJoystick() {
  int left_joystick_x_value = analogRead(A0);
  int left_joystick_y_value = analogRead(A1);
  int right_joystick_x_value = analogRead(A2);
  int right_joystick_y_value = analogRead(A3);

  if (left_joystick_x_value < 340) y_axis_degree -= 7;
  else if (left_joystick_x_value > 680) y_axis_degree += 7;

  if (left_joystick_y_value < 340) clamp_degree -= 5;
  else if (left_joystick_y_value > 680) clamp_degree += 5;

  if (right_joystick_x_value < 340) x_axis_degree -= 7;
  else if (right_joystick_x_value > 680) x_axis_degree += 7;

  if (right_joystick_y_value < 340) z_axis_degree -= 5;
  else if (right_joystick_y_value > 680) z_axis_degree += 5;

  z_axis_degree = min(100, max(20, z_axis_degree));
  x_axis_degree = min(180, max(0, x_axis_degree));
  y_axis_degree = min(160, max(70, y_axis_degree)); 
  clamp_degree = min(160, max(40, clamp_degree));

  servo_clamp.write(clamp_degree);
  delay(10);
  servo_x_axis.write(x_axis_degree);
  delay(10);
  servo_y_axis.write(y_axis_degree);
  delay(10);
  servo_z_axis.write(z_axis_degree);
  delay(10);
}

void controlWithPython() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    if (data.equals("vat1_command")) {
      moveToVat1Position();
    } else if (data.equals("vat2_command")) {
      moveToVat2Position();
    } else if (data.equals("vat3_command")) {
      moveToVat3Position();
    }
  }
}

void moveToVat1Position() {
  servo_y_axis.write(150);
  delay(2000);
  servo_x_axis.write(30);
  delay(3000);
  servo_z_axis.write(75);
  delay(2000);
   servo_clamp.write(80);
  delay(1000);
  servo_y_axis.write(130);
  delay(2000);
  servo_clamp.write(130);
  delay(2000);
  servo_y_axis.write(150);
  delay(2000);
  servo_x_axis.write(110);
  delay(3000);
  servo_y_axis.write(110);
  delay(2000);
  servo_clamp.write(80);
  delay(2000);
}

void moveToVat2Position() {
  servo_y_axis.write(150);
  delay(2000);
  servo_x_axis.write(30);
  delay(2000);
  servo_z_axis.write(75);
  delay(2000);
   servo_clamp.write(80);
  delay(1000);
  servo_y_axis.write(130);
  delay(2000);
  servo_clamp.write(130);
  delay(2000);
  servo_y_axis.write(150);
  delay(2000);
  servo_x_axis.write(130);
  delay(2000);
  servo_y_axis.write(110);
  delay(2000);
  servo_clamp.write(80);
  delay(2000);
  
  
}

void moveToVat3Position() {
  
  servo_y_axis.write(150);
  delay(2000);
  servo_x_axis.write(30);
  delay(2000);
  servo_z_axis.write(75);
  delay(2000);
   servo_clamp.write(80);
  delay(1000);
  servo_y_axis.write(130);
  delay(2000);
  servo_clamp.write(130);
  delay(2000);
  servo_y_axis.write(150);
  delay(2000);
  servo_x_axis.write(150);
  delay(2000);
  servo_y_axis.write(110);
  delay(2000);
  servo_clamp.write(80);
  delay(2000);
}
