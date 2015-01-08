#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# this code was written by Edwin van den Oetelaar
# no garantees whatsoever, it was for personal use
# you can use it at your own risk, under a GPL2 license

import time

import serial

__author__ = 'oetelaar'


class UDB120x():
    SINE = 0 # sine wave output constant
    TRI = 1  # Triangle wave output constant
    SQR = 2  # square wave output constant

    def __init__(self):
        self._serialport = None
        self._devicename = None

    def _send_command(self, command=None):
        """send a command to serial port, wait for 'ok' reponse message
           add the needed \r\n to the command message
           read response from device upto including \r\n
           :returns response (str)
        """
        assert command is not None, 'Can not send empty command'
        self._serialport.timeout = 1
        # write data to device
        self._serialport.write(command)
        self._serialport.write(b'\x0d\x0a')
        # read data
        state = 0
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

    def connect(self, portname=None):
        """"connect serial and handshake with DDS device"""
        assert portname is not None
        self._serialport = serial.Serial(port=portname, baudrate=57600, bytesize=8, parity='N', stopbits=1,
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
            time.sleep(1)

        if retries == 0:
            print "device not found"

    def disconnect(self):
        assert self._serialport is not None
        self._serialport.close()

    def set_frequency(self, freq_hz):
        """set output frequency, if > 1Khz resolution is lower"""
        assert self._serialport is not None, "no serial port configured"
        assert freq_hz < 10e6, 'Maximum freqency is 10Mhz for device'
        assert freq_hz > 0, 'Frequency must be positive value'
        if freq_hz < 1000:
            # use low freq setup
            self._send_command('bu3')
            tmp = 'bf{freq:0>9}'.format(freq=int(freq_hz * 1000.0))
            print(tmp)
            self._send_command(tmp)
        else:
            # use high freq setup
            self._send_command('bu1')
            tmp = 'bf{freq:0>9}'.format(freq=int(freq_hz * 10.0))
            print(tmp)
            self._send_command(tmp)

    def set_waveform(self, waveform=SINE):
        """set output wave form"""
        assert waveform in (UDB120x.SINE, UDB120x.TRI, UDB120x.SQR)
        self._send_command('bw{x}'.format(x=waveform))

    def set_amplitude(self, amplitude=None):
        """set amplitude of output signal max 255"""
        assert amplitude >= 0, 'amplitude out of range 0..255'
        assert amplitude < 256, 'amplitude out of range 0..255'
        self._send_command('ba{x}'.format(x=int(amplitude)))

    def get_amplitude(self):
        """get amplitude of output signal max 255"""
        x = self._send_command('ca')
        if x.startswith('ca'):
            return int(x[2:])
        else:
            return -1

    def get_frequency(self):
        """get frequency from DDS device, not working as expected"""
        x = self._send_command('cf')
        if x.startswith('cf'):
            return int(x[2:])


if __name__ == "__main__":
    dds = UDB120x()
    dds.connect(portname='/dev/ttyUSB0')
    print ('setting freq to 999.001 Hz, ampl=128')
    dds.set_amplitude(amplitude=128)
    dds.set_frequency(freq_hz=999.001)
    print (dds.get_frequency())  # reports 200000 not 999001, so not working as expected
    print ('active amplitude={a}'.format(a=dds.get_amplitude()))
    time.sleep(5)
    print ('setting freq to 20.0 kHz, full amplitude')
    dds.set_frequency(freq_hz=20000)
    dds.set_amplitude(amplitude=255)
    print (dds.get_frequency())  # reporing correct frequency, but only in bu1 mode ??

    time.sleep(2)
    print ('set tot triangle wave')
    dds.set_waveform(waveform=UDB120x.TRI)
    dds.disconnect()
