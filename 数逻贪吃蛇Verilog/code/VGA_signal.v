`timescale 1ns / 1ps

module VGA_signal(
		input clk,
		input rst,
		output reg[9:0] HS_cnt,//行计数
		output reg[9:0] VS_cnt,//场计数
		output H_sync,//行同步信号（低有效）
		output V_sync,//场同步信号（低有效）
		output  disValid//是否为有效显示区域,1为有效
		);
		localparam H_PIXEL=10'd799,//行像素800
					  VLINE=10'd520,//行数521
					  //下面是有效显示区域的行列坐标边界值
					  UP_BOUND=31,
					  DOWN_BOUND=510,
					  LEFT_BOUND=144,
					  RIGHT_BOUND=783;
					  
		reg DisValid;//displayValid 当前是否为有效显示区域
		assign disValid=DisValid;
		initial begin//初始化
			HS_cnt<=0;
			VS_cnt<=0;
			DisValid<=0;
		end
		
		//列计数与行同步
		assign H_sync=(HS_cnt<96)?0:1;
		always@(posedge clk or posedge rst)
		begin
			if(rst)
				HS_cnt<=0;
			else if(HS_cnt==H_PIXEL)//当前行扫描完毕
				HS_cnt<=0;
			else
				HS_cnt<=HS_cnt+1;
		end
		
		
		//行计数与场同步
		assign V_sync=(VS_cnt<2)?0:1;
		always@(posedge clk or posedge rst)
		begin
			if(rst)
				VS_cnt<=0;
			else if(HS_cnt==H_PIXEL)
			begin
				if(VS_cnt==VLINE)
					VS_cnt<=0;
				else
					VS_cnt<=VS_cnt+1;
			end
			else
				VS_cnt<=VS_cnt;
		end
		
		always@(posedge clk)begin
			if((HS_cnt>=LEFT_BOUND)&&(HS_cnt<=RIGHT_BOUND)&&(VS_cnt<DOWN_BOUND)&&(VS_cnt>UP_BOUND))
				DisValid<=1;//有效显示区
			else
				DisValid<=0;//非有效显示区
		end
endmodule

