# README #

* Everywhere on the internet shops are selling low cost DDS (Direct Digital synthesizer, signal generators) [DDS at wikipedia](http://en.wikipedia.org/wiki/Direct_digital_synthesizer) devices called USB1202s, UDB1205s, UDB1210s or UDB1201s. (about US $50)
* These devices can also measure Frequency upto 60MHz, and have counting function.
* Also a ADC is present to measure a voltage
* I found software and documentation here at the manufacturers site  [Zhengzhou Minghe Electronic Technolgy Co., Ltd](http://www.mhinstek.com/down/html/?83.html) and other places on that site.
* These devices ship without documentation and software.
* I noticed a serial port present and investigated how to control the device by serial protocol.
* What you find here is the results. 
* It is possible and easy to control these devices, read the ADC en Freq counters over the serial.
* Documentation can be found on the [WIKI pages](https://bitbucket.org/tweetand/udb120x/wiki) 

### How do I get set up? ###

* You need a UDB120x device (tested with UDB1210s firmware 6.6)
* A serial connection to your PC (by TTL level serial) like a USB/Serial converter
* A linux machine (maybe you can get it working on Windows, I do not care about that)

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Whom do I talk to? ###

* You can try to report an issue in the [bitbucket issue tracker](https://bitbucket.org/tweetand/udb120x/issues)
