`timescale 1ns / 1ps

module VGA_Color(
		input clk,
		input rst,
		input disValid,
		input [1:0]state,
		input [2:0]pixel,//即将显示的像素类别
		input [11:0] EggPos,//蛋的位置(以像素块为单位)
		input [9:0] X_Pos,//行计数
		input [9:0] Y_Pos,//场计数
		output reg [3:0] R,//颜色显示
		output reg [3:0] G,
		output reg [3:0] B
		);	
		wire [15:0]data2;
		wire [15:0]data1;
		reg [18:0]addr;
		localparam StartState=2'b10,//开始状态
					  DieState=2'b00,//死亡状态
					  PlayState=2'b01,//游戏状态
					  WinState=2'b11;//胜利状态
GAME_END ROM1(.clka(clk),.addra(addr),.douta(data1));//三个分别是时钟信号、地址线、数据输出
Start_State ROM2(.clka(clk),.addra(addr),.douta(data2));
//Win ROM3(.clka(clk),.addra(addr),.douta(data3));

		always@(posedge clk or posedge rst)begin
			if(rst)begin
							R<=0;
							G<=0;
							B<=0;
			end
			else begin
				if(disValid)begin
					if( X_Pos >= 0 && X_Pos < 640 && Y_Pos >= 0 && Y_Pos < 480 ) begin
						case(state)
						PlayState://游戏状态
							if(pixel==3'b100)begin
									R<=4'b0000;
									G<=4'b0000;
									B<=4'b1111;
							end
							else if( pixel == 3'b000 )//00显示没有东西的地方，白色
								begin
									R<=4'b1111;
									G<=4'b1111;
									B<=4'b1111;
							end	
							else if( pixel == 3'b001 )//01显示墙壁
							begin
									R<=0;
									G<=4'b1111;
									B<=0;
							end	
							else if(pixel == 3'b010)//10显示蛇头	
							begin
									R<=4'b1111;
									G<=0;
									B<=0;
							end
							else if(pixel == 3'b110)//11显示蛇身
							begin
									R<=0;
									G<=4'b1111;
									B<=4'b1111;
							end
						DieState:begin//死亡状态 显示GameOver
							addr<=Y_Pos*640+X_Pos;
							R<=data1[14:11];
							G<=data1[8:5];
							B<=data1[3:0];
							end
						WinState:begin//胜利状态，显示GameOver
							addr<=Y_Pos*640+X_Pos;
							R<=data1[14:11];
							G<=data1[8:5];
							B<=data1[3:0];
							end
						StartState:begin//开始状态，显示开始游戏画面
							addr<=Y_Pos*640+X_Pos;
							R<=data2[14:11];
							G<=data2[8:5];
							B<=data2[3:0];
							end
						endcase
					end
				else //非有效显示区域
						begin
								R<=0;
								G<=0;
								B<=0;
						end	
			end
		end 
	end
endmodule