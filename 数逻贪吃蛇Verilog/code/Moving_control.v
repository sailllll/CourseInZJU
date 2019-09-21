`timescale 1ns / 1ps

module Moving_control(
	 input clk,
	 input rst,
    input [3:0] Control,//[3]下 [2]右 [1]左 [0]上
	 output reg [1:0]direction//蛇头的移动方向 00上,01左,10右,11下 
    );
	 localparam up=2'b00,
					left=2'b01,
					right=2'b10,
					down=2'b11;
					
	initial begin//初始化
		direction<=down;
	end
	 always @(posedge clk or posedge rst) begin
		if(rst)begin//复位蛇头向下
			direction <= down;
			end
		else begin
			if(!Control[0]&&direction!=down) direction <= up;//蛇头向上，且保证原方向不是向下
			else if(!Control[1]&&direction!=right) direction <= left;//左
			else if(!Control[2]&&direction!=left) direction <= right;//右
			else if(!Control[3]&&direction!=up) direction <= down;//下
			else direction <= direction;//保持原方向
		end
	end


endmodule
