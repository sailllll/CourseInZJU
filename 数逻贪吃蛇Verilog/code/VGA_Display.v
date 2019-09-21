`timescale 1ns / 1ps

module VGA_Display(
		input clk,
		input rst,
		input [1:0]state,
		input [2:0]pixel,//即将显示的像素类别
		input [11:0] EggPos,//蛋的位置(以像素块为单位)
		output wire [9:0] X_Pos,//行计数
		output wire [9:0] Y_Pos,//场计数
		output wire H_sync,//行同步信号（低有效）
		output wire V_sync,//场同步信号（低有效）
		output wire [3:0] R,//颜色显示
		output wire [3:0] G,
		output wire [3:0] B
		);
		localparam
					 UP_BOUND=31,//Y方向有效显示区域的下界
					 LEFT_BOUND=144;//X方向有效显示区域的下界
					 
		wire disValid;//displayValid 当前是否为有效显示区域
		wire [9:0] HS_cnt,VS_cnt;//行坐标和列坐标(包括行同步、后沿、有效数据区、前沿)
		assign X_Pos = HS_cnt - LEFT_BOUND;//有效显示区域的X Y坐标
		assign Y_Pos = VS_cnt - UP_BOUND;

		
		VGA_signal M1(.clk(clk),
						  .rst(rst),
						  .HS_cnt(HS_cnt),
						  .VS_cnt(VS_cnt),
						  .H_sync(H_sync),
						  .V_sync(V_sync),
						  .disValid(disValid)
						  );
		VGA_Color M2(.clk(clk),
						 .rst(rst),
						 .disValid(disValid),
						 .pixel(pixel),
						 .state(state),
						 .EggPos(EggPos),
						 .X_Pos(X_Pos),
						 .Y_Pos(Y_Pos),
						 .R(R),
						 .G(G),
						 .B(B)
						 );

endmodule

