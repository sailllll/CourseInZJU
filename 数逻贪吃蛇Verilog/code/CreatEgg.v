`timescale 1ns / 1ps

module CreatEgg (
	input clk,
	input rst,
	input state,
	input [5:0] Head_X,
	input [5:0] Head_Y,
	input refresh,
	output reg [5:0] Food_X,
	output reg [5:0] Food_Y,
	output reg Grow
);
	localparam PlayState = 2'b01;
	reg [11:0] Random_Generator;

	initial begin//初始化
		Food_X <= 10;
		Food_Y <= 20;
		Grow <= 0;
	end
	
	always @( posedge clk or posedge rst ) begin
		if(rst) begin
			Food_X <= 24;
			Food_Y <= 10;
			Grow <= 0;
		end

		else if(state==PlayState)begin//判断食物是否被吃并随机生成食物位置
				//使用计数器取模获得食物随机位置
				Random_Generator <= Random_Generator + 666;
				if( (Food_X == Head_X && Food_Y == Head_Y) | refresh ) begin
					if(Food_X == Head_X && Food_Y == Head_Y)//食物被吃
						Grow <= 1;
					
					//随机生成食物位置 已避免食物生成在墙里					
					Food_X <= (Random_Generator[11:6])%38+1'b1;
					Food_Y <= Random_Generator[5:0]%28+1'b1;
				end
				else 
					Grow <= 0;
			end
		else begin//非游戏状态，初始化食物位置以及增长信号
			Food_X <= 10;
			Food_Y <= 20;
			Grow <= 0;
		end
	end
endmodule
