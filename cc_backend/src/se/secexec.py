from ctypes import *

class ExecArgs(Structure):
    _fields_ = [("timelimit", c_int),
                ("memlimit", c_int),
                ("maxfilesz", c_int),
                ("infile", c_char_p),
                ("outfile", c_char_p),
                ("errfile", c_char_p),
                ("jailroot", c_char_p),
                ("execname", c_char_p)
                ]
    
                
def secure_spawn(ea):
    se = cdll.LoadLibrary("./libsecexec.so")
    se.secure_spawn(ea)


if __name__ == "__main__":
    infile = c_char_p("in")
    outfile = c_char_p("out")
    errfile = c_char_p("err")
    jailroot = c_char_p("jail")
    execname = c_char_p("./helloworld")
    timelimit = c_int(1)
    memlimit = c_int(32)
    maxfilesz = c_int(32)

    ea = ExecArgs(timelimit, memlimit, maxfilesz, infile, outfile, errfile, jailroot, execname)
    secure_spawn(ea)
