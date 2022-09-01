module Wrapper_tb;
// fpga4student.com: FPGA project, Verilog project, VHDL project 
// Verilog project: Verilog code for microcontroller
// Inputs
reg clk;
reg neg_clk;
reg rst;
reg neg_rst;
wire [9:0] Pc;
wire [31:0] out;
// Instantiate the Unit Under Test (UUT)
top top_tb(
.out(out),
.neg_clk(neg_clk),
.neg_rst(neg_rst),
.clk(clk), 
.rst(rst),
.Pc(Pc)
);
initial begin
clk = 0;
neg_clk = 1;
forever begin
     #10 clk = ~clk;
     #10 neg_clk = ~neg_clk;
end
end 

initial begin 
$dumpfile("test.vcd"); 
$dumpvars(0, Wrapper_tb); 

// Initialize Inputs
rst = 1;
neg_rst = 1;
//Pc=0;
// Wait 100 ns for global reset to finish
#100;
rst = 0;
neg_rst = 0;


#2000 $finish; 

end 
endmodule