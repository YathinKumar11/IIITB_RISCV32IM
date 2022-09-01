from typing import List
import sys
from nmigen import *
from nmigen.sim import *
from nmigen import Elaboratable, Module, Signal
from nmigen.build import Platform
from nmigen.cli import main_parser, main_runner
from nmigen.back import rtlil, verilog
from all_stages.If_stage import *
from all_stages.ID_stage import *
from all_stages.ALU import *
from all_stages.Mem_stage import *
from all_stages.Writeback_stage import *
from all_stages.memory import *
from all_stages.register_file import *
import sys


class Wrapper(Elaboratable):
    def __init__(self):
        self.pc = Signal(10)
        self.wb_stop_beq = Signal(1)
        self.counter_branch = Signal(3)
        self.counter_jump = Signal(3)
        self.Busy = Array([Signal(1) for i in range(32)])
        self.Busy1 = Array([Signal(1) for i in range(32)])
        self.Busy_csr = Array([Signal(1) for i in range(2**1)])
        self.nthforwarding = Array([Signal(1) for i in range(32)])
        self.IF = IF_stage()
        self.ID = ID()
        self.ALU = ALU()
        self.reg_file = Register_file()
        self.memory = Memory_file()
        self.test = Signal(5)
        self.s_type = 0b011
        self.temp = Signal(32)


    def elaborate(self,platform:Platform)->Module:
        m = Module()
        
        m.submodules.IF = self.IF
        m.submodules.ID = self.ID
        m.submodules.ALU = self.ALU
        m.submodules.reg_file = self.reg_file
        m.submodules.memory = self.memory
        #m.d.sync += self.IF.mem[Const(0)].eq(0b00000000001100010000000010110011) #add x1 x2 x3
        #m.d.sync += self.IF.mem[Const(1)].eq(0b00000000001000001000001000110011) #add x4 x1 x2
        #m.d.sync += self.IF.mem[Const(2)].eq(0b00000000001100001000001000110011) #add x4 x1 x3
        # mydomain = ClockDomain("clk", clk_edge="pos")
        # m.domains += mydomain

        #m.d.sync += self.IF.mem[Const(1)].eq(0b00000000010000010000001001100111) #jalr inst
        # print(mydomain.clk)

        # m.d.sync += self.IF.mem[Const(0)].eq(0b00000010001000001000000110110011 )#Mul r3 r1 r2
        # m.d.sync += self.IF.mem[Const(1)].eq(0b00000010001000001001000110110011 )#MulH r3 r1 r2
        # m.d.sync += self.IF.mem[Const(2)].eq(0b00000010001000001010000110110011 )#MulHSU r3 r1 r2
        # m.d.sync += self.IF.mem[Const(3)].eq(0b00000010001000001011000110110011 )#MulHU r3 r1 r2
        # m.d.sync += self.IF.mem[Const(4)].eq(0b00000010001000001100000110110011 )#DIV r3 r1 r2
        # m.d.sync += self.IF.mem[Const(5)].eq(0b00000010001000001101000110110011 )#DIVU r3 r1 r2
        # m.d.sync += self.IF.mem[Const(6)].eq(0b00000010001000001110000110110011 )#REM r3 r1 r2
        # m.d.sync += self.IF.mem[Const(7)].eq(0b00000010001000001111000110110011 )#REMU r3 r1 r2
        
      	    # 0:	fe010113          	addi	sp,sp,-32
            # 4:	00812e23          	sw	s0,28(sp)
            # 8:	02010413          	addi	s0,sp,32
            # c:	00300793          	li	a5,3
            # 10:	fef42623          	sw	a5,-20(s0)
            # 14:	fec42783          	lw	a5,-20(s0)
            # 18:	02f787b3          	mul	a5,a5,a5
            # 1c:	fec42703          	lw	a4,-20(s0)
            # 20:	02f707b3          	mul	a5,a4,a5
            # 24:	fef42423          	sw	a5,-24(s0)
            # 28:	00000013          	nop
            # 2c:	01c12403          	lw	s0,28(sp)
            # 30:	02010113          	addi	sp,sp,32
            # 34:	00008067          	ret  

        # filename = sys.argv[-1]
        # print(filename)
        # filename = input()
        # f = open(filename, "r")

        # inst = f.readlines()

        # for i in range(len(inst)):
        #     instruction = "0x"+inst[i]
        #     m.d.sync += self.IF.mem[Const(i)].eq(int(instruction,16))

        # m.d.sync += self.IF.mem[Const(0)].eq(0b00000000000100001010000101110011)
        # m.d.sync += self.IF.mem[Const(1)].eq(0b00000000000100001010000101110011)


        
        with m.If(self.ID.ifload==Const(1)):
            with m.If(self.ID.des == self.IF.out[15:20]):
                m.d.sync += self.IF.Pc.eq(self.pc-1) #mem of IF needed to be hardcoded 
                m.d.sync += self.ID.instruction.eq(0x00000000) 

            with m.Elif(self.ID.des == self.IF.out[20:25]):
                m.d.sync += self.IF.Pc.eq(self.pc-1) #mem of IF needed to be hardcoded 
                m.d.sync += self.ID.instruction.eq(0x00000000) 
              #m.d.sync += self.IF.Pc.eq(self.pc-1) #mem of IF needed to be hardcoded 
              #m.d.sync += self.ID.instruction.eq(0x00000000) 
            with m.Else():
                m.d.sync += self.IF.Pc.eq(self.pc)
                m.d.sync += self.ID.instruction.eq(self.IF.out) 

        with m.Else():
            m.d.sync += self.IF.Pc.eq(self.pc)
            m.d.sync += self.ID.instruction.eq(self.IF.out) 
        m.d.comb += self.reg_file.load_Rs1_addr.eq(self.ID.s1)
        m.d.comb += self.reg_file.load_Rs2_addr.eq(self.ID.s2)
        m.d.comb += self.reg_file.load_csr_addr.eq(self.ID.csr_addr)
    
        with m.If(self.ID.des != Const(0)):
            with m.If(self.ID.instruction_type == Const(3)):  #for sw, 'des' will not be busy
                m.d.sync += self.Busy[self.ID.des].eq(Const(0))
            with m.Elif(self.ID.instruction_type == Const(4)):  #for beq, 'des' will not be busy
                m.d.sync += self.Busy[self.ID.des].eq(Const(0))
            with m.Elif(self.ALU.jump == Const(1)):
                m.d.sync += self.Busy[self.ID.des].eq(Const(0))
            with m.Elif(self.ALU.branching == Const(1)):
                m.d.sync += self.Busy[self.ID.des].eq(Const(0))
            with m.Elif(self.counter_branch == Const(1)):
                m.d.sync += self.Busy[self.ID.des].eq(Const(0))
            with m.Elif(self.counter_branch == Const(2)):
                m.d.sync += self.Busy[self.ID.des].eq(Const(0))
            with m.Else():
                m.d.sync += self.Busy[self.ID.des].eq(Const(1))

        with m.If(self.ID.csr_addr != Const(0)):
                m.d.sync += self.Busy_csr[self.ID.csr_addr].eq(Const(1))

            



        with m.If(self.Busy[self.ID.s1] == Const(1)):
            with m.If(self.Busy1[self.ID.s1] == Const(0)):
                m.d.neg += self.ID.s1_data_in.eq(self.ALU.result)
            with m.Else():
                with m.If(self.ALU.inst_type!=0b011):
                    with m.If(self.ALU.inst_type!=0b100):
                        with m.If(self.ALU.reg_addr_out == self.ID.s1):
                            m.d.neg += self.ID.s1_data_in.eq(self.ALU.result)
                        with m.Else():
                            m.d.neg += self.ID.s1_data_in.eq(self.memory.data_out)
                    with m.Else(): 
                        m.d.neg += self.ID.s1_data_in.eq(self.memory.data_out)

                with m.Else():
                    m.d.neg += self.ID.s1_data_in.eq(self.memory.data_out)

            

        with m.If(self.Busy[self.ID.s2] == Const(1)):
            with m.If(self.Busy1[self.ID.s2] == Const(0)):
                m.d.neg += self.ID.s2_data_in.eq(self.ALU.result)
            with m.Else():
                with m.If(self.ALU.inst_type!=0b011):
                    with m.If(self.ALU.inst_type!=0b100):
                        with m.If(self.ALU.reg_addr_out == self.ID.s2):
                            m.d.neg += self.ID.s2_data_in.eq(self.ALU.result)
                        with m.Else():
                            m.d.neg += self.ID.s2_data_in.eq(self.memory.data_out)

                    with m.Else(): 
                        m.d.neg += self.ID.s2_data_in.eq(self.memory.data_out)
                with m.Else():
                    m.d.neg += self.ID.s2_data_in.eq(self.memory.data_out)

        with m.If(self.Busy[self.ID.s1]==Const(0)):
            m.d.neg += self.ID.s1_data_in.eq(self.reg_file.write_Rs1_data)

        with m.If(self.Busy[self.ID.s2]==Const(0)):
            m.d.neg += self.ID.s2_data_in.eq(self.reg_file.write_Rs2_data)


        with m.If(self.Busy_csr[self.ID.csr_addr] == Const(1)):
            m.d.neg += self.ID.csrdata_in.eq(self.ALU.result)
        with m.Else():
            m.d.neg += self.ID.csrdata_in.eq(self.reg_file.write_csr_data)
     
    

    

        m.d.sync += self.ALU.reg_addr_in.eq(self.ID.des)
        m.d.sync += self.ALU.csr_addr.eq(self.ID.csr_addr)
        m.d.sync += self.ALU.inst_type.eq(self.ID.instruction_type)
        m.d.sync += self.ALU.pc.eq(self.pc)
        m.d.sync += self.ALU.Ra.eq(self.ID.s1data_out)
        m.d.sync += self.ALU.Rb.eq(self.ID.s2data_out)
        m.d.sync += self.ALU.CSR_in.eq(self.ID.csrdata_out)
        m.d.sync += self.ALU.src2_addr.eq(self.ID.s2)
        m.d.sync += self.ALU.src1_addr.eq(self.ID.s1)
        m.d.sync += self.ALU.shamt.eq(self.ID.shamt)

        
        m.d.sync += self.ALU.immediate.eq(self.ID.signextended_immediate)
        with m.If(self.ID.des!=self.ALU.reg_addr_in):
            with m.If(self.ALU.inst_type==Const(3)):
                m.d.sync += self.Busy1[self.ALU.reg_addr_in].eq(Const(0))
            with m.Else():
                 m.d.sync += self.Busy1[self.ALU.reg_addr_in].eq(Const(1))

        with m.If(self.ALU.branching == Const(1)):
            m.d.comb += self.temp.eq(self.ALU.immediate//4)
            with m.If(self.counter_branch != Const(1)):
                m.d.sync += self.pc.eq(self.pc+(self.ALU.immediate//4)-Const(3))

        with m.Elif(self.ALU.jump == Const(1)):
            m.d.sync += self.pc.eq(self.ALU.Ra+(self.ALU.immediate//4))


        with m.Elif(self.ID.ifload == Const(1)):
            #m.d.comb += self.test.eq(self.IF.out[15:20])
            with m.If(self.ID.des == self.IF.out[15:20]):
                m.d.sync += self.pc.eq(self.pc) 

            with m.Elif(self.ID.des == self.IF.out[20:25]):
                m.d.sync += self.pc.eq(self.pc)  
            with m.Else():
                m.d.sync += self.pc.eq(self.pc+Const(1)) 
        with m.Else():
            m.d.sync += self.pc.eq(self.pc+Const(1))  
        with m.If(self.ALU.branching == Const(1)):
            m.d.sync += self.counter_branch.eq(self.counter_branch+Const(1))
            m.d.sync += self.ID.prev_branch.eq(Const(1))   # previous instruction(pc-2) is giving branch signal to id stage. 
        with m.If(self.ALU.jump == Const(1)):
            m.d.sync += self.counter_branch.eq(self.counter_branch+Const(1))
       


        with m.If(self.counter_branch == Const(0)):

            m.d.sync += self.ALU.inst_type0.eq(self.ID.it0)
            m.d.sync += self.ALU.inst_type1.eq(self.ID.it1)
            m.d.sync += self.ALU.inst_type2.eq(self.ID.it2)
            m.d.sync += self.ALU.inst_type3.eq(self.ID.it3)
        

            m.d.comb += self.memory.load.eq(self.ALU.load_mem)
            m.d.comb += self.memory.write.eq(self.ALU.write_mem)

            with m.If(self.Busy[self.memory.src_reg_addr] == Const(0)):
                m.d.comb += self.memory.data_in.eq(self.ALU.Rb)
            with m.Else():
                m.d.comb += self.memory.data_in.eq(self.memory.data_out)
               
            m.d.comb += self.memory.addr.eq(self.ALU.result)

    
            m.d.sync += self.memory.load_wb.eq(self.ALU.load_wb)
            m.d.sync += self.memory.load_wb_csr.eq(self.ALU.load_wb_csr)
            m.d.sync += self.memory.reg_addr_out.eq(self.ALU.reg_addr_out)
            m.d.sync += self.memory.csr_addr.eq(self.ALU.csr_addr)
            m.d.comb += self.memory.src_reg_addr.eq(self.ALU.src2_addr)
            m.d.comb += self.memory.alu_result.eq(self.ALU.result)
            m.d.sync += self.memory.temp_csr.eq(self.ALU.temp_csr)

        
        with m.Elif(self.counter_branch == Const(4)):

            m.d.sync += self.ALU.inst_type0.eq(self.ID.it0)
            m.d.sync += self.ALU.inst_type1.eq(self.ID.it1)
            m.d.sync += self.ALU.inst_type2.eq(self.ID.it2)
            m.d.sync += self.ALU.inst_type3.eq(self.ID.it3)

            m.d.comb += self.memory.load.eq(self.ALU.load_mem)
            m.d.comb += self.memory.write.eq(self.ALU.write_mem)

            with m.If(self.Busy[self.memory.src_reg_addr] == Const(1)):
                m.d.comb += self.memory.data_in.eq(self.memory.data_out)
            with m.Else():
                m.d.comb += self.memory.data_in.eq(self.ALU.Rb)
            m.d.comb += self.memory.addr.eq(self.ALU.result)

    
            m.d.sync += self.memory.load_wb.eq(self.ALU.load_wb)
            m.d.sync += self.memory.load_wb_csr.eq(self.ALU.load_wb_csr)
            m.d.sync += self.memory.reg_addr_out.eq(self.ALU.reg_addr_out)
            m.d.sync += self.memory.csr_addr.eq(self.ALU.csr_addr)
            m.d.comb += self.memory.src_reg_addr.eq(self.ALU.src2_addr)
            m.d.comb += self.memory.alu_result.eq(self.ALU.result)
            m.d.sync += self.memory.temp_csr.eq(self.ALU.temp_csr)
            with m.If(self.ALU.branching == Const(1)):
                m.d.sync += self.counter_branch.eq(Const(1))
            with m.Else():
                m.d.sync += self.counter_branch.eq(Const(0))

        with m.Else():

            with m.If(self.counter_branch == Const(1)):
                m.d.sync += self.ALU.inst_type0.eq(0)
                m.d.sync += self.ALU.inst_type1.eq(0)
                m.d.sync += self.ALU.inst_type2.eq(0)
                m.d.sync += self.ALU.inst_type3.eq(0)
                m.d.sync += self.ID.prev_branch.eq(0)
              
            with m.Elif(self.counter_branch == Const(2)):
                m.d.sync += self.Busy[self.memory.reg_addr_out].eq(Const(0))
                m.d.sync += self.Busy[self.ALU.reg_addr_out].eq(Const(0))
                m.d.sync += self.Busy1[self.memory.reg_addr_out].eq(Const(0))
                m.d.sync += self.Busy1[self.ALU.reg_addr_out].eq(Const(0))
                m.d.sync += self.ALU.inst_type0.eq(0)
                m.d.sync += self.ALU.inst_type1.eq(0)
                m.d.sync += self.ALU.inst_type2.eq(0)
                m.d.sync += self.ALU.inst_type3.eq(0)
            
            with m.Else():
                m.d.sync += self.ALU.inst_type0.eq(self.ID.it0)
                m.d.sync += self.ALU.inst_type1.eq(self.ID.it1)
                m.d.sync += self.ALU.inst_type2.eq(self.ID.it2)
                m.d.sync += self.ALU.inst_type3.eq(self.ID.it3)


            m.d.sync += self.counter_branch.eq(self.counter_branch+Const(1))
            m.d.comb += self.memory.load.eq(0b00)
            m.d.comb += self.memory.write.eq(0b00)
            m.d.comb += self.memory.data_in.eq(0x00000000)
            m.d.comb += self.memory.addr.eq(0x00000000)

    
            m.d.sync += self.memory.load_wb.eq(0b0)
            m.d.sync += self.memory.load_wb_csr.eq(0b0)
            m.d.sync += self.memory.reg_addr_out.eq(0b00000)
            m.d.sync += self.memory.csr_addr.eq(self.ALU.csr_addr)
            m.d.comb += self.memory.src_reg_addr.eq(0b00000)
            m.d.comb += self.memory.alu_result.eq(0x00000000)
            m.d.sync += self.memory.temp_csr.eq(self.ALU.temp_csr)



        m.d.comb += self.reg_file.write.eq(self.memory.load_wb)  #pos->comb
        m.d.comb += self.reg_file.write_addr.eq(self.memory.reg_addr_out)
        m.d.comb += self.reg_file.write_csr_addr.eq(self.memory.csr_addr)
        m.d.comb += self.reg_file.write_data.eq(self.memory.data_out)
        m.d.comb += self.reg_file.write_csr.eq(self.memory.load_wb_csr)
        m.d.comb += self.reg_file.temp_csr.eq(self.memory.temp_csr)
    
        with m.If(self.ALU.reg_addr_out !=self.reg_file.write_addr):
            with m.If(self.ID.des != self.reg_file.write_addr):
                m.d.sync += self.Busy[self.reg_file.write_addr].eq(Const(0))#Busy[reg_file.write_addr]-Const(1))
                m.d.sync += self.Busy1[self.reg_file.write_addr].eq(Const(0))

        with m.If(self.ALU.csr_addr != self.reg_file.write_csr_addr):
            with m.If(self.ID.csr_addr != self.reg_file.write_csr_addr):
                m.d.sync += self.Busy_csr[self.reg_file.write_csr_addr].eq(Const(0))

        return m

    def ports(self)->List[Signal]:
        return []

# if __name__ == "__main__":            

    # sys.setrecursionlimit(10000000)
    # parser = main_parser()
    # args = parser.parse_args()

    # m = Module()
    # m.domains.sync = sync = ClockDomain("sync", async_reset=True)
    # pos = ClockDomain("pos", async_reset=True)
    # neg = ClockDomain("neg",clk_edge="neg",async_reset=True)
    # neg.clk = pos.clk
    # m.domains += [neg,pos]

    # m.submodules.Wrapper1 = Wrapper1 = Wrapper()




    # sim = Simulator(m)
    # sim.add_clock(1e-6, domain="sync")
    # sim.add_clock(1e-6,domain="pos")
    # sim.add_clock(1e-6,domain = "neg")


    # def process():
    #     yield 
        #yield Delay(1e-6)


# sim.add_sync_process(process,domain="sync")  # or sim.add_sync_process(process), see below
# with sim.write_vcd("test.vcd", "test.gtkw", traces=Wrapper1.IF.ports()+Wrapper1.ID.ports()+Wrapper1.ALU.ports()+Wrapper1.memory.ports()+Wrapper1.reg_file.ports()):
#     sim.run_until(10000e-6, run_passive=True)

Wrapper  = Wrapper()
frag = Wrapper.elaborate(platform=None)
#print(rtlil.convert(frag, ports=[sys.adr, sys.dat_r, sys.dat_w, sys.we]))
print(verilog.convert(frag, ports=Wrapper.IF.ports()+Wrapper.ID.ports()+Wrapper.ALU.ports()+Wrapper.memory.ports()+Wrapper.reg_file.ports()))
