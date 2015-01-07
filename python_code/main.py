#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time

__author__ = 'oetelaar'


class UDB120x():
    def __init__(self):
        self._serialport = None
        self._devicename = None

    def _send_command(self,command=None):
        """send a command to serial port, wait for 'ok' reponse message
           add the needed \r\n to the command message
           read response from device upto including \r\n
           :returns response (str)
        """
        assert command is not None,'Can not send empty command'
        self._serialport.timeout=1
        # write data to device
        self._serialport.write(command)
        self._serialport.write(b'\x0d\x0a')
        # read data
        state=0
        response = ''
        while state != 2:

            b = self._serialport.read(size=1)
            if len(b) == 0:
                print 'nothing from serial'
            else:
                if state == 0 and b == b'\x0d':
                    state = 1
                elif state == 1 and b == '\x0a':
                    state = 2
                else:
                    # append to response string
                    response += b

        print 'got CR/LF'
        print 'response was {xx}'.format(xx=response)
        return response

    def _probe_device(self):
        assert self._serialport is not None
        name = self._send_command('a')
        if name.startswith('UDB'):
            self._devicename = name
        else:
            print('unknown name')

    def connect(self):
        self._serialport = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, bytesize=8, parity='N', stopbits=1,
                                         timeout=1, xonxoff=0, rtscts=0)
        print('port {p} is open'.format(p=self._serialport.name))
        # try to find the device on serial
        retries = 10
        while True:
            self._probe_device()
            if self._devicename is not None:
                print('Device {d} is found'.format(d=self._devicename))
                break
            if retries == 0:
                break
            retries -= 1
            # sleep(1)
        if retries == 0:
            print "device not found"

    def disconnect(self):
        assert self._serialport is not None
        self._serialport.close()

    def set_frequency(self, freq_hz):
        assert self._serialport is not None, "no serial port configured"
        assert freq_hz < 10e6, 'Maximum freqency is 10Mhz for device'
        assert freq_hz > 0,'Frequency must be positive value'
        if freq_hz < 1000 :
            # use low freq setup
            self._send_command('bu3')
            tmp = 'bf{freq:0>9}'.format(freq=int(freq_hz*1000.0))
            print(tmp)
            self._send_command(tmp)
        else:
            # use high freq setup
            self._send_command('bu1')
            tmp = 'bf{freq:0>9}'.format(freq=int(freq_hz*10.0))
            print(tmp)
            self._send_command(tmp)

if __name__ == "__main__":
    my_udb = UDB120x()
    my_udb.connect()
    print('setting freq to 999.001 Hz')
    my_udb.set_frequency(freq_hz=999.001)
    time.sleep(5)
    print('setting freq to 20.0 kHz')
    my_udb.set_frequency(freq_hz=20000)
    my_udb.disconnect()
