`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    14:49:55 01/02/2018 
// Design Name: 
// Module Name:    Snake_Top 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module Snake_Top(
		input clk,
		input [15:0] SW,
		input RSTN,
		input [3:0] BTN,
		output wire [4:0]K_ROW,
		output wire H_sync,
		output wire V_sync,
		output wire [3:0] R,
		output wire [3:0] G,
		output wire [3:0] B,
		output wire Buzzer,
		output wire RDY,
		output wire CR
    );
	 wire [31:0] clkDiv;//时钟信号
	 wire [3:0] Button_Out;//阵列键盘去抖动输入
	 wire [1:0] state;//游戏当前状态
	 wire [15:0] SW_OK;
	 wire [9:0] X_Pos,Y_Pos;//扫描像素点坐标
	 wire rst;
	 wire disValid,refresh,grow,die,win;
	 wire [2:0]pixel;//扫描像素点的类型
	 wire [6:0]length;//蛇的长度
	 assign Buzzer=1'b1;
	 
	 SAnti_jitter(.clk(clk), 
					 .RSTN(RSTN),
					 .readn(1),
					 .Key_y(BTN),
					 .Key_x(K_ROW),
					 .SW(SW), 
					 .Key_ready(RDY),
					 .BTN_OK(Button_Out),
					 .SW_OK(SW_OK),
					 .CR(CR),
					 .rst(rst)
					 );


	GameModule   M3(.clk(clkDiv[24]),
						 .rst(rst),
						 .mov_clk(clkDiv[10]),
						 .state(state),
						 .Button_Control(BTN),
						 .X_Pos(X_Pos),
						 .Y_Pos(Y_Pos),
						 .length(length),
						 .pixel(pixel),
						 .die(die),
						 .win(win)
						 );
						 
	State_ctrl   M4(.clk(clkDiv[5]),
						 .rst(rst),
						 .BTN(BTN),
						 .die(die),
						 .state(state),
						 .win(win)
						 );
	clk_div      M5(.clk(clk),
	                .clkdiv(clkDiv)
						 );
							 
	 
	VGA_Display  M6(.clk(clkDiv[1]),
						 .rst(rst),
						 .pixel(pixel),
						 .X_Pos(X_Pos),
						 .Y_Pos(Y_Pos),
						 .state(state),
						 .H_sync(H_sync),
						 .V_sync(V_sync),
						 .R(R),
						 .G(G),
						 .B(B)
						 );

endmodule
