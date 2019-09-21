`timescale 1ns / 1ps
module State_ctrl(
    input clk,
    input rst,
    input [3:0] BTN,
	 input die,
	 input win,
	 output reg[1:0] state
    );
	 reg [31:0] cnt;
	 localparam StartState=2'b10,//开始状态
					DieState=2'b00,//死亡状态
					PlayState=2'b01,//游戏状态
					WinState=2'b11;//胜利状态
	
	initial begin
		state <= StartState;//初始化为开始状态
		cnt <= 0;
	end
	
	always@(posedge clk or posedge rst)begin
		if(rst) begin
			state <= StartState;
		end
		else begin
			case(state)
			WinState:begin//死亡后延时若干时间回到初始状态
				if(cnt <= 10000000)begin
					cnt <= cnt + 1;
					state <= state;
				end
				else begin
					cnt<=0;
					state<=StartState;//延时结束，回到初始状态
				end
			end
			
			DieState:begin//胜利后延时若干时间回到初始状态
				if(cnt <= 10000000)begin
					cnt <= cnt + 1;
					state <= state;
				end
				else begin
					cnt <= 0;
					state <= StartState;//延时结束，回到初始状态
				end
			end
			PlayState:
				if(die) state <= DieState;//进入死亡状态
				else if(win) state <= WinState;//胜利状态
				else state <= state;
				
			StartState://在开始状态时，按键进入游戏状态
				if(BTN != 4'b1111) state <= PlayState;
				else state <= state;
			default:
				state <= state;
			endcase
		end
	end
endmodule
