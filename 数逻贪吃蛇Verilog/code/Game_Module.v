`timescale 1ns / 1ps

module GameModule (
	input clk,//模块主要使用的时钟
	input rst,
	input mov_clk,//根据输入改变移动方向的时钟
	input [1:0]state,//游戏状态
	input [3:0] Button_Control,//控制蛇移动方向
	input [9:0] X_Pos,//VGA当前扫描像素点的X坐标0~640
	input [9:0] Y_Pos,//VGA当前扫描像素点的Y坐标0~480
	output reg [6:0] length,
	output reg [2:0]pixel,//VGA扫描像素点的状态
	output reg die,//游戏失败
	output reg win//游戏胜利
	);
	
	wire [1:0] Direction;//蛇前进方向
	wire Grow;//蛇是否增长一个单位
	wire [5:0] Food_X;//食物坐标
	wire [5:0] Food_Y;
	wire [5:0] Head_X,Head_Y;//蛇头坐标
	localparam UP = 2'b00,//上下左右
				  DOWN = 2'b11,
				  LEFT = 2'b01,
				  RIGHT = 2'b10,
				  PlayState = 2'b01,//游戏状态
				  NONE = 3'b000,//扫描像素点的类型，无
				  HEAD = 3'b010,//蛇头
				  BODY = 3'b001,//蛇身
			  	  WALL = 3'b001,//墙壁
				  FOOD = 3'b100;//食物
	

	
	
 	reg [5:0] Unit_X[15:0];//每个单元是蛇的一节身体的X坐标
	reg [5:0] Unit_Y[15:0];//身体的Y坐标
	reg [15:0] Unit_Exist;//判断上面各个单元是否真的存储蛇身体信息
	reg refresh;//食物刷新信号
	assign Head_X = Unit_X[0];//蛇头存储在第一个单元中
	assign Head_Y = Unit_Y[0];
	
	initial begin//初始化 蛇长度为2
		Unit_X[0] <= 6'd20;
		Unit_Y[0] <= 6'd15;
		Unit_X[1] <= 6'd20;
		Unit_Y[1] <= 6'd14;
		die <= 0;
		win <= 0;
		refresh <= 0;
		Unit_Exist <= 16'b0000000000000011;
		length <= 2;
	end
	
		CreatEgg M0(.clk(clk),//随机产生食物,判断蛇是否吃到食物,输出蛇是否增长的信号
					.rst(rst),
					.refresh(refresh),
					.Head_X(Head_X),
					.Head_Y(Head_Y),
					.Food_X(Food_X),
					.Food_Y(Food_Y),
					.Grow(Grow)
					);	
					
	Moving_control M1(.clk(mov_clk),
					      .rst(rst),
					      .Control(Button_Control),
					      .direction(Direction)
					      );
					
		//当蛇吃到食物时，蛇长度增长
	always @( posedge clk or posedge rst ) begin
		if( rst ) begin//复位
			Unit_Exist <= 16'b0000000000000011;
			length <= 2;
		end
		else begin
		if(state==PlayState)//游戏状态 
				if( Grow==1 ) begin
					length <= length + 1;//长度增一
					Unit_Exist[length] <= 1;//寄存器有效单元增一
				end
				else begin
				end
		else begin//其它状态  初始化长度信息
				Unit_Exist <= 16'b0000000000000011;
				length <= 2;
			end
		end
	end

	always @( posedge clk or posedge rst)begin
		if(rst) begin//复位
			Unit_X[0] <= 6'd20;
			Unit_Y[0] <= 6'd15;
			Unit_X[1] <= 6'd20;
			Unit_Y[1] <= 6'd14;
			die <= 0;
			win <= 0;
		end
		else begin//首先判断蛇是否达成游戏结束的条件，未达成时，进行蛇的移动
			if( state== PlayState ) begin
				if(length==16)//判断是否达到最大长度
					win<=1;
				else if( ( Direction == UP && Unit_Y[0] == 1 )  
						| ( Direction == DOWN && Unit_Y[0] == 28 )
						| ( Direction == LEFT && Unit_X[0] == 1 )
						| ( Direction == RIGHT && Unit_X[0] == 38 ) )
						die <= 1;//判断是否撞墙
				else if( ( Unit_Y[0] == Unit_Y[1] && Unit_X[0] == Unit_X[1] && Unit_Exist[1] == 1 )
							| ( Unit_Y[0] == Unit_Y[2] && Unit_X[0] == Unit_X[2] && Unit_Exist[2] == 1 )
							| ( Unit_Y[0] == Unit_Y[3] && Unit_X[0] == Unit_X[3] && Unit_Exist[3] == 1 )
							| ( Unit_Y[0] == Unit_Y[4] && Unit_X[0] == Unit_X[4] && Unit_Exist[4] == 1 )
							| ( Unit_Y[0] == Unit_Y[5] && Unit_X[0] == Unit_X[5] && Unit_Exist[5] == 1 )
							| ( Unit_Y[0] == Unit_Y[6] && Unit_X[0] == Unit_X[6] && Unit_Exist[6] == 1 )
							| ( Unit_Y[0] == Unit_Y[7] && Unit_X[0] == Unit_X[7] && Unit_Exist[7] == 1 )
							| ( Unit_Y[0] == Unit_Y[8] && Unit_X[0] == Unit_X[8] && Unit_Exist[8] == 1 )
							| ( Unit_Y[0] == Unit_Y[9] && Unit_X[0] == Unit_X[9] && Unit_Exist[9] == 1 )
							| ( Unit_Y[0] == Unit_Y[10] && Unit_X[0] == Unit_X[10] && Unit_Exist[10] == 1 )
							| ( Unit_Y[0] == Unit_Y[11] && Unit_X[0] == Unit_X[11] && Unit_Exist[11] == 1 )
							| ( Unit_Y[0] == Unit_Y[12] && Unit_X[0] == Unit_X[12] && Unit_Exist[12] == 1 )
							| ( Unit_Y[0] == Unit_Y[13] && Unit_X[0] == Unit_X[13] && Unit_Exist[13] == 1 )
							| ( Unit_Y[0] == Unit_Y[14] && Unit_X[0] == Unit_X[14] && Unit_Exist[14] == 1 )
							| ( Unit_Y[0] == Unit_Y[15] && Unit_X[0] == Unit_X[15] && Unit_Exist[15] == 1 ) )
							die <= 1;//判断是否吃到身体
				else begin//上述判断均为假说明游戏继续,下面先判断食物是否刷新在蛇身体上
						if( ( Food_Y == Unit_Y[1] && Food_X == Unit_X[1] && Unit_Exist[1] == 1 )
							| ( Food_Y == Unit_Y[2] && Food_X == Unit_X[2] && Unit_Exist[2] == 1 )
							| ( Food_Y == Unit_Y[3] && Food_X == Unit_X[3] && Unit_Exist[3] == 1 )
							| ( Food_Y == Unit_Y[4] && Food_X == Unit_X[4] && Unit_Exist[4] == 1 )
							| ( Food_Y == Unit_Y[5] && Food_X == Unit_X[5] && Unit_Exist[5] == 1 )
							| ( Food_Y == Unit_Y[6] && Food_X == Unit_X[6] && Unit_Exist[6] == 1 )
							| ( Food_Y == Unit_Y[7] && Food_X == Unit_X[7] && Unit_Exist[7] == 1 )
							| ( Food_Y == Unit_Y[8] && Food_X == Unit_X[8] && Unit_Exist[8] == 1 )
							| ( Food_Y == Unit_Y[9] && Food_X == Unit_X[9] && Unit_Exist[9] == 1 )
							| ( Food_Y == Unit_Y[10] && Food_X == Unit_X[10] && Unit_Exist[10] == 1 )
							| ( Food_Y == Unit_Y[11] && Food_X == Unit_X[11] && Unit_Exist[11] == 1 )
							| ( Food_Y == Unit_Y[12] && Food_X == Unit_X[12] && Unit_Exist[12] == 1 )
							| ( Food_Y == Unit_Y[13] && Food_X == Unit_X[13] && Unit_Exist[13] == 1 )
							| ( Food_Y == Unit_Y[14] && Food_X == Unit_X[14] && Unit_Exist[14] == 1 )
							| ( Food_Y == Unit_Y[15] && Food_X == Unit_X[15] && Unit_Exist[15] == 1 ) )
							refresh <= 1;//判断是否吃到身体
							else refresh <= 0;
			   //在寄存器单元间进行移位赋值,然后将新蛇头信息存储在第一个单元来实现移动
						Unit_X[1] <= Unit_X[0];
						Unit_Y[1] <= Unit_Y[0];
						Unit_X[2] <= Unit_X[1];
						Unit_Y[2] <= Unit_Y[1];
						Unit_X[3] <= Unit_X[2];
						Unit_Y[3] <= Unit_Y[2];
						Unit_X[4] <= Unit_X[3];
						Unit_Y[4] <= Unit_Y[3];
						Unit_X[5] <= Unit_X[4];
						Unit_Y[5] <= Unit_Y[4];
						Unit_X[6] <= Unit_X[5];
						Unit_Y[6] <= Unit_Y[5];
						Unit_X[7] <= Unit_X[6];
						Unit_Y[7] <= Unit_Y[6];
						Unit_X[8] <= Unit_X[7];
						Unit_Y[8] <= Unit_Y[7];
						Unit_X[9] <= Unit_X[8];
						Unit_Y[9] <= Unit_Y[8];
						Unit_X[10] <= Unit_X[9];
						Unit_Y[10] <= Unit_Y[9];
						Unit_X[11] <= Unit_X[10];
						Unit_Y[11] <= Unit_Y[10];
						Unit_X[12] <= Unit_X[11];
						Unit_Y[12] <= Unit_Y[11];
						Unit_X[13] <= Unit_X[12];
						Unit_Y[13] <= Unit_Y[12];
						Unit_X[14] <= Unit_X[13];
						Unit_Y[14] <= Unit_Y[13];
						Unit_X[15] <= Unit_X[14];
						Unit_Y[15] <= Unit_Y[14];
								
						case( Direction ) //根据运动方向产生新的蛇头
							UP:Unit_Y[0] <= Unit_Y[0] - 1;
							DOWN:Unit_Y[0] <= Unit_Y[0] + 1;
							LEFT:Unit_X[0] <= Unit_X[0] - 1;
							RIGHT: Unit_X[0] <= Unit_X[0] + 1;
						endcase
					end
				end
				else begin//非游戏状态，进行蛇身信息以及游戏状态信号的初始化
				Unit_X[0] <= 6'd20;
				Unit_Y[0] <= 6'd15;
				Unit_X[1] <= 6'd20;
				Unit_Y[1] <= 6'd14;
				die <= 0;
				win <= 0;
				refresh <= 0;
				end
			end
		end

	//返回VGA当前扫描坐标点的像素类型
	always @( X_Pos or Y_Pos ) begin
		if( X_Pos >= 0 && X_Pos < 640 && Y_Pos >= 0 && Y_Pos < 480 ) begin
			if(  X_Pos[9:4] == 0 || Y_Pos[9:4] == 0 || X_Pos[9:4] == 39 || Y_Pos[9:4] == 29 )
				pixel <= WALL;//当前像素为墙壁
			else if( X_Pos[9:4] == Unit_X[0] && Y_Pos[9:4] == Unit_Y[0] && Unit_Exist[0] == 1 )
				pixel <= HEAD;//蛇头
			else if(X_Pos[9:4] == Food_X && Y_Pos[9:4] == Food_Y)
				pixel <= FOOD;//食物
			else if( ( X_Pos[9:4] == Unit_X[1] && Y_Pos[9:4] == Unit_Y[1] && Unit_Exist[1] == 1 )
					 || ( X_Pos[9:4] == Unit_X[2] && Y_Pos[9:4] == Unit_Y[2] && Unit_Exist[2] == 1 )
					 || ( X_Pos[9:4] == Unit_X[3] && Y_Pos[9:4] == Unit_Y[3] && Unit_Exist[3] == 1 )
					 || ( X_Pos[9:4] == Unit_X[4] && Y_Pos[9:4] == Unit_Y[4] && Unit_Exist[4] == 1 )
					 || ( X_Pos[9:4] == Unit_X[5] && Y_Pos[9:4] == Unit_Y[5] && Unit_Exist[5] == 1 )
					 || ( X_Pos[9:4] == Unit_X[6] && Y_Pos[9:4] == Unit_Y[6] && Unit_Exist[6] == 1 )
					 || ( X_Pos[9:4] == Unit_X[7] && Y_Pos[9:4] == Unit_Y[7] && Unit_Exist[7] == 1 )
					 || ( X_Pos[9:4] == Unit_X[8] && Y_Pos[9:4] == Unit_Y[8] && Unit_Exist[8] == 1 )
					 || ( X_Pos[9:4] == Unit_X[9] && Y_Pos[9:4] == Unit_Y[9] && Unit_Exist[9] == 1 )
					 || ( X_Pos[9:4] == Unit_X[10] && Y_Pos[9:4] == Unit_Y[10] && Unit_Exist[10] == 1 )
					 || ( X_Pos[9:4] == Unit_X[11] && Y_Pos[9:4] == Unit_Y[11] && Unit_Exist[11] == 1 )
					 || ( X_Pos[9:4] == Unit_X[12] && Y_Pos[9:4] == Unit_Y[12] && Unit_Exist[12] == 1 )
					 || ( X_Pos[9:4] == Unit_X[13] && Y_Pos[9:4] == Unit_Y[13] && Unit_Exist[13] == 1 )
					 || ( X_Pos[9:4] == Unit_X[14] && Y_Pos[9:4] == Unit_Y[14] && Unit_Exist[14] == 1 )
					 || ( X_Pos[9:4] == Unit_X[15] && Y_Pos[9:4] == Unit_Y[15] && Unit_Exist[15] == 1 ))
				pixel <= BODY;//蛇身
			else
				pixel <= NONE;//空白
		end
	end	 

endmodule


