# read design

read_verilog iiitb_riscv.v

# generic synthesis
synth -top top

# mapping to mycells.lib
dfflibmap -liberty /home/ubuntu/Downloads/RV32IM_aug17/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
abc -liberty /home/ubuntu/Downloads/RV32IM_aug17/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
clean
flatten
# write synthesized design
write_verilog -noattr synth_riscv.v
