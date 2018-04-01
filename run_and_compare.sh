#!/bin/bash

g++ -lm -lcrypt -O2 -std=c++11 -DONLINE_JUDGE main.cpp -o main

cat input.txt | ./main > my_out.txt
# if(diff my_out.txt output.txt); then
#   echo "yes"
# else
#   echo "no"
# fi
