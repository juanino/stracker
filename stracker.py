#!/usr/bin/python

from gpiozero import MotionSensor
import time
import socket

# get the graphite server from config file
import stracker_config as cfg


def now():
        return int(time.time())


def collect_metric(name, value, timestamp):
    sock = socket.socket()
    sock.connect( (cfg.graphite_server, 2003) )
    sock.send("%s %d %d\n" % (name, value, timestamp))
    sock.close()

pir = MotionSensor(4,1,1)

moves = 0 # stores how many movements in a sample
nomoves = 0 # how many samples were not movements
sampletime = 5 # how long to sample for

timer = now() # init the timer
while True:
    if pir.motion_detected:
        moves += 1
    else:
        nomoves += 1
    # check if sample time has passed
    if (now() - timer) > sampletime:
        print str(sampletime) + " second sample"
        print "moves are ", moves
        print "nomoves are ", nomoves
        if moves > 0:
            print "move percent is ",
            pct =  (float(moves)/(moves+nomoves)*100)
            print pct
        else:
            print "move percent is",
            print 0
        print "sending to graphite: ",
        print now(), " ", "stracker.moves", moves

        # send to graphite
        collect_metric("stracker.moves", moves, now())
        collect_metric("stracker.nomoves", nomoves, now())

        # reset for next sample period
        timer = now()
        moves = 0
        nomoves = 0
