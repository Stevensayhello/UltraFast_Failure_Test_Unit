# UltraFast Failure Test Unit

This repo contains front end software for Xilinx rftool developed for Xilinx ZCU111. Developed by UBC Capstone group CG-045.

`CMD_Interface.c` is the Command-line Server where ADC and PLL clock can be set.
`Data_Interface.c` is the Data Server for receiving ADC Data and converting them to .csv file.

## Windows User:

Use Microsoft Visual Studio to compile the .c code as terminal app.

## Linux/Mac User:

Use gcc to compile the c code
`gcc CMD_Interface.c/Data_Interface.c -o pick_a_name`

## Initialization Guide

After rftool reset itself, connect Data Server first and then run CMD Server. After cmd server showing Restart Data server, enter D on data server to restart the interface. And then press enter on cmd server to continue initialization. There are some preset settings for ADC which can be use directly.
