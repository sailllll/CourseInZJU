NET "clk" LOC = AC18 | IOSTANDARD = LVCMOS18;
NET "clk" TNM_NET = TM_CLK;
TIMESPEC TS_CLK_100M = PERIOD "TM_CLK" 10ns HIGH 50%;
NET "RSTN" LOC = W13 | IOSTANDARD = LVCMOS18;
NET "K_ROW[0]" LOC = V17 | IOSTANDARD = LVCMOS18;
NET "K_ROW[1]" LOC = W18 | IOSTANDARD = LVCMOS18;
NET "K_ROW[2]" LOC = W19 | IOSTANDARD = LVCMOS18;
NET "K_ROW[3]" LOC = W15 | IOSTANDARD = LVCMOS18;
NET "K_ROW[4]" LOC = W16 | IOSTANDARD = LVCMOS18;
NET "BTN[0]" LOC = V18 | IOSTANDARD = LVCMOS18;
NET "BTN[1]" LOC = V19 | IOSTANDARD = LVCMOS18;
NET "BTN[2]" LOC = V14 | IOSTANDARD = LVCMOS18;
NET "BTN[3]" LOC = W14 | IOSTANDARD = LVCMOS18;
#NET "readn"    LOC = U21 | IOSTANDARD = LVCMOS33;
NET "RDY"      LOC = U22 | IOSTANDARD = LVCMOS33;
NET "CR"       LOC = V22 | IOSTANDARD = LVCMOS33;
#NET "SEGCLK"   LOC = M24 | IOSTANDARD = LVCMOS33;
#NET "SEGCLR"   LOC = M20 | IOSTANDARD = LVCMOS33;
#NET "SEGDT"    LOC = L24 | IOSTANDARD = LVCMOS33;
#NET "SEGEN"    LOC = R18 | IOSTANDARD = LVCMOS33;
#LED
#NET "LEDCLK"   LOC = N26 | IOSTANDARD = LVCMOS33;
#NET "LEDCLR"   LOC = N24 | IOSTANDARD = LVCMOS33;
#NET "LEDDT"    LOC = M26 | IOSTANDARD = LVCMOS33;
#NET "LEDEN"    LOC = P18 | IOSTANDARD = LVCMOS33;
#switch
NET "SW[0]"   LOC = AA10 | IOSTANDARD = LVCMOS15;
NET "SW[1]"   LOC = AB10 | IOSTANDARD = LVCMOS15;
NET "SW[2]"   LOC = AA13 | IOSTANDARD = LVCMOS15;
NET "SW[3]"   LOC = AA12 | IOSTANDARD = LVCMOS15;
NET "SW[4]"   LOC = Y13  | IOSTANDARD = LVCMOS15;
NET "SW[5]"   LOC = Y12  | IOSTANDARD = LVCMOS15;
NET "SW[6]"   LOC = AD11 | IOSTANDARD = LVCMOS15;
NET "SW[7]"   LOC = AD10 | IOSTANDARD = LVCMOS15;
NET "SW[8]"   LOC = AE10 | IOSTANDARD = LVCMOS15;
NET "SW[9]"   LOC = AE12 | IOSTANDARD = LVCMOS15;
NET "SW[10]"  LOC = AF12 | IOSTANDARD = LVCMOS15;
NET "SW[11]"  LOC = AE8  | IOSTANDARD = LVCMOS15;
NET "SW[12]"  LOC = AF8  | IOSTANDARD = LVCMOS15;
NET "SW[13]"  LOC = AE13 | IOSTANDARD = LVCMOS15;
NET "SW[14]"  LOC = AF13 | IOSTANDARD = LVCMOS15;
NET "SW[15]"  LOC = AF10 | IOSTANDARD = LVCMOS15;
NET "B[0]"   LOC = T20 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "B[1]"   LOC = R20 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "B[2]"   LOC = T22 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "B[3]"   LOC = T23 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "G[0]"   LOC = R22 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "G[1]"   LOC = R23 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "G[2]"   LOC = T24 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "G[3]"   LOC = T25 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "R[0]"   LOC = N21 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "R[1]"   LOC = N22 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "R[2]"   LOC = R21 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "R[3]"   LOC = P21 | IOSTANDARD = LVCMOS33 | SLEW = FAST;
NET "H_sync"   LOC = M22 | IOSTANDARD = LVCMOS33;
NET "V_sync"   LOC = M21 | IOSTANDARD = LVCMOS33;

NET "Buzzer"     LOC = AF24 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[0]" LOC = AB22 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[1]" LOC = AD24 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[2]" LOC = AD23 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[3]" LOC = Y21 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[4]" LOC = W20 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[5]" LOC = AC24 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[6]" LOC = AC23 | IOSTANDARD = LVCMOS33;
#NET "SEGMENT[7]" LOC = AA22 | IOSTANDARD = LVCMOS33;
#NET "AN[0]" LOC = AD21 | IOSTANDARD = LVCMOS33;
#NET "AN[1]" LOC = AC21 | IOSTANDARD = LVCMOS33;
#NET "AN[2]" LOC = AB21 | IOSTANDARD = LVCMOS33;
#NET "AN[3]" LOC = AC22 | IOSTANDARD = LVCMOS33;
#NET "LED[0]" LOC = AB26 | IOSTANDARD = LVCMOS33;
#NET "LED[1]" LOC = W24 | IOSTANDARD = LVCMOS33;
#NET "LED[2]" LOC = W23 | IOSTANDARD = LVCMOS33;
#NET "LED[3]" LOC = AB25 | IOSTANDARD = LVCMOS33;
#NET "LED[4]" LOC = AA25 |  IOSTANDARD = LVCMOS33;
#NET "LED[5]" LOC = W21 | IOSTANDARD = LVCMOS33;
#NET "LED[6]" LOC = V21 | IOSTANDARD = LVCMOS33;
#NET "LED[7]" LOC = W26 | IOSTANDARD = LVCMOS33;