

# `parsebar`

Colorful progress bars and with Serial port parser for your terminal, powered by [progressive](https://github.com/hfaran/progressive).

## Introduction

`parsebar` lets you view bargraphs for your values parsed from a serial port:

[![example use](https://raw.githubusercontent.com/ConnyCola/parsebar/master/example.gif)](https://github.com/ConnyCola/parsebar)


## Installation

parsebar depends on progressive, install it first

```
pip install progressive

git clone https://github.com/ConnyCola/parsebar.git
```
## how to use

parse pattern is 'temp: ' and the max value is 50

```
python parsebar.py /dev/tty.ACM0 'temp: ' 50
```


parse the temperature of a sensor on the serial port sending you data like : 
```
temp: 25
temp: 26
temp: 28
```

### advanced use

you can parse as manny arguments as you wish by just adding more to the list


```
python parsebar.py /dev/tty.SerialPort 'arg1' max1 'arg2' max2 'arg3' max3
```
