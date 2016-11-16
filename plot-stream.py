#!/usr/bin/env python

import subprocess

with open("data-stream-for-plot.txt","w") as fpw:
  with open("data-stream-soc.txt","w") as fpsoc:
    with open("data-stream.txt","r") as fp:
        con = fp.read()
        for l in con.split("\n"):
            soc_flag = False
            if len(l)<=0 or l[0]=="#":
                continue
            if l[0]=="S":
               l = l[2:]
               soc_flag = True
            words = l.split()
            y,m,d = [float(s) for s in words[0].split(".")]
            t = y + m/12.0 + d/365.0

            bf = 4.0 / float(words[5])
            if soc_flag:
                fpsoc.write("{} {}\n".format(t,bf))
            else:
                fpw.write("{} {}\n".format(t,bf))

with open("data-stream.gnuplot","w") as fpw:
    fpw.write("""
#!/usr/bin/gnuplot

set term postscript eps enhanced 22
set out "data-stream.eps"

set style data lines
set style line 1  linetype -1 linewidth 3 lc rgb "#808080"
set style line 2  linetype -1 linewidth 3 lc rgb "#dfcf00"
set style line 3  linetype -1 linewidth 3 lc rgb "#005197"
set style line 4  linetype -1 linewidth 3 lc rgb "#00D317"
set style line 5  linetype -1 linewidth 3 lc rgb "#971c00"
set style line 6  linetype -1 linewidth 3 lc rgb "#000000"
set style line 7  linetype -1 linewidth 3 lc rgb "#ff0000"
set style increment user


set size 1.15,1.15
set border linewidth 1.5

set logscale y
set xrange [1991:2016]
    set yrange [0.01:30]
set key samplen 6 spacing 3.0
set key top right
set grid lw 3
set ylabel "Byte per FLOP"
set xlabel "Beginning of Year"
plot 'data-stream-for-plot.txt'     using 1:2 with p pt 1 ps 3.0 title "STREAM Benchmark entries", \
     'data-stream-soc.txt'          using 1:2 with p pt 1 ps 3.0 title "SoC-based Machines", \
     'data-intel.txt'     using 1:($5/$2)           with linesp pt  9 ps 3.0 title "INTEL Xeon CPUs", \
     'data-sp-nvidia.txt' using 1:($4/$2)           with linesp pt  5 ps 3.0 title "NVIDIA Geforce GPUs", \
     'data-amd.txt'       using 1:($5/$2)           with linesp pt  7 ps 3.0 title "AMD Radeon GPUs", \
     'data-intel-phi.txt' using 1:($5/$2)           with linesp pt 11 ps 3.0 title "INTEL Xeon Phis",\
     'data-top-10.txt'    using 1:2                 with p pt 1  ps 3.0 title "Top 10 machines"


""")

subprocess.call("gnuplot data-stream.gnuplot",shell=True)
