#!/bin/bash

g++ -lm -lcrypt -O2 -std=c++11 -DONLINE_JUDGE main.cpp -o main

./rig > input.txt
