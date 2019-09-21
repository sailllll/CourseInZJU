#include <IRremote.h>
#include <Servo.h>

const int LeftMotor = 8;//左电机控制方向的引脚
const int LeftMotorPWM = 9;//左电机控制转速的引脚
const int RightMotor = 10;
const int RightMotorPWM = 11;
const int RightTrackSensor = 3;//右循迹传感器
const int LeftTrackSensor = 4;
const int RightAvoidSensor = 5;//右避障传感器
const int LeftAvoidSensor = 6;
int RTSS, LTSS;//右（左）循迹传感器状态（RightTrackSensorState）
int RASS, LASS;//右（左）避障传感器状态（RightAvoidSensorState）

#define TRACK_MODE 1 //依次为巡线、避障、遥控模式
#define AVOID_MODE 2
#define REMOTE_MODE 3
#define PORTKEY A2
uint8_t keyMode;
const int LED1 = 7;
const int LED2 = 12;
int RECV_PIN = A4;//端口
IRrecv irrecv(RECV_PIN);
decode_results results;

long int last = millis();
long int advanceR = 0x00FF629D;//前进，对应CH
long int retreatR = 0x00FFA857;//后退，对应+
long int leftR = 0x00FF22DD;//左转，对应|<<
long int rightR = 0x00FFC23D;// 右转,对应>||
long int brakeR = 0x00FF02FD;//停车,对应>>|


void LEDInit()//用于指示当前模式的信号灯
{
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
}
void sensorInit()//电机和传感器的初始化
{
  pinMode(LeftMotor, OUTPUT);
  pinMode(RightMotor, OUTPUT);
  pinMode(LeftMotorPWM, OUTPUT);
  pinMode(RightMotorPWM, OUTPUT);
  pinMode(RightTrackSensor, INPUT);
  pinMode(LeftTrackSensor, INPUT);
  pinMode(RightAvoidSensor, INPUT);
  pinMode(LeftAvoidSensor, INPUT);
}

void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn();//打开接收器
  sensorInit();
  modeInit();
  LEDInit();
}

void loop() {
  modeScan();
  modeSwitch();

}
//-----------------------小车基本动作---------------------------------
void advance()//小车前进
{
  digitalWrite(RightMotor, LOW);//规定电机低电平为正转
  analogWrite(RightMotorPWM, 255);//调速为最大
  digitalWrite(LeftMotor, LOW);
  analogWrite(LeftMotorPWM, 255);
}

void brake()//刹车
{
  digitalWrite(RightMotor, LOW);
  analogWrite(RightMotorPWM, 0);//调速为0，停车
  digitalWrite(LeftMotor, LOW);
  analogWrite(LeftMotorPWM, 0);
}

void left()//左转
{
  digitalWrite(RightMotor, LOW);
  analogWrite(RightMotor, 255);//只动右轮使小车左转
  digitalWrite(LeftMotor, LOW);
  analogWrite(LeftMotor, 0);
}

void right()//右转
{
  digitalWrite(RightMotor, LOW);
  analogWrite(RightMotor, 0);//只动左轮使小车右转
  digitalWrite(LeftMotor, LOW);
  analogWrite(LeftMotor, 255);
}

void retreat()//后退
{
  digitalWrite(RightMotor, HIGH);//电机置高电平，反转后退
  analogWrite(RightMotorPWM, 255);
  digitalWrite(LeftMotor, HIGH);
  analogWrite(LeftMotorPWM, 255);
}

//---------------各模式实现------------
void autoTrack()//自动循迹模式，无红外线返回时传感器返回高电平（黑线吸收红外线）
{
  RTSS = digitalRead(RightTrackSensor);//读取左右传感器电位状态
  LTSS = digitalRead(LeftTrackSensor);
  if(RTSS == LOW && LTSS ==LOW)//左右均为低电平，小车在线路上
    advance();
  else if(RTSS == LOW && LTSS == HIGH)//左传感器检测到黑线，说明小车向右偏离线路
    left();
  else if(RTSS == HIGH && LTSS == LOW)//右传感器检测到黑线，说明小车向左偏离线路
    right();
  else//都是黑色，黑线过宽，无法继续循迹
    brake();
}

void autoAvoid()//自动避障模式,传感器检测到障碍物时返回低电平
{
  RASS = digitalRead(RightAvoidSensor);//读取左右传感器电位状态
  LASS = digitalRead(LeftAvoidSensor);
  if( RASS == HIGH && LASS == HIGH)//前方无障碍，前进
    advance();
  else if(RASS == HIGH && LASS == LOW)//左边检测到障碍，右转
    right();
  else if(RASS == LOW && LASS == HIGH)//右边检测到障碍，左转
    left();
  else//前方都有障碍，停车并后退
  {
    brake();
    delay(500);
    retreat();
    delay(500);
    if(random(0,2))//左右转随机选择
        left();
    else
        right();
    delay(500);
  }
}

void dump(decode_results *results)
{
  if(results->decode_type == UNKNOWN)//信号无法解码时停车
    brake();
}

void remoteControl()
{
  if( irrecv.decode(&results))//调用irrecv类解码，decode()判断是否收到编码
  //如果收到编码，返回非零值并将该编码存储于decode_results结构中
  {
    if(millis()- last > 200)//确认收到的信号
    {
      dump(&results);//解码接收到的红外信号
    }
    //根据解码的信号执行相应操作
    if(results.value == advanceR) advance();//前进
    else  if(results.value == brakeR) brake();//刹车
    else  if(results.value == leftR) left();//左转
    else  if(results.value == rightR) right();//右转
    else  if(results.value == retreatR) retreat();//后退
    
    last = millis();
    irrecv.resume();//当前信号已解码后，resume()接收下一个信号
  }
}

//----------------初始化以及模式转换---------------
void modeSwitch()//三种模式的转换
{
  switch(keyMode)
  {
    case TRACK_MODE://巡线模式，LED1亮，LED2暗
      autoTrack();
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
      break;
    case AVOID_MODE://避障模式，LED1暗，LED2亮
      autoAvoid();
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, HIGH);
      break;
    case REMOTE_MODE://遥控模式,LED1和LED2均亮
      remoteControl();
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, HIGH);
      break;
    default:
      break;
  }
}

void modeInit()
{
  pinMode(PORTKEY, INPUT_PULLUP);//初始化按钮，默认巡线模式
  keyMode = TRACK_MODE;
}

void modeScan()
{
  static uint8_t sign = 0;
  if( (sign == 0) && (digitalRead(PORTKEY) == HIGH))//利用sign确保单次按键只进入一次语句块
  {
    sign = 1;
    switch(keyMode)//错位赋值完成模式切换
    {
      case TRACK_MODE:
        keyMode = AVOID_MODE;
        break;
      case AVOID_MODE:
        keyMode = REMOTE_MODE;
        break;
      case REMOTE_MODE:
        keyMode = TRACK_MODE;
        break;
      default:
        break;
    }
  }
  if(digitalRead(PORTKEY) == LOW)//按键松开时，sign归零，等待下次按键
    sign = 0;
}

