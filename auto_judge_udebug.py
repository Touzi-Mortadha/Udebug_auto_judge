#!/usr/bin/env python
import requests
import json
import sys
import os
import subprocess
import re
import difflib

# you need to specify your cookie, you can get it from /udebug/api/
cookie = 'Basic "Unl1dWs6MjcwNjk0MTU="'
headers = {'Authorization': cookie}
s = requests.Session()
s.headers.update(headers)


class Udebug:

    def __init__(self, judge_alias, problem_id):

        self.judge_alias = judge_alias
        self.problem_id = str(problem_id)
        # os.system("g++ -std=c++11 -DONLINE_JUDGE main.cpp -o main")

    def get_list_id_test(self):
        url = "https://www.udebug.com/input_api/input_list/retrieve.json?judge_alias=" + self.judge_alias + "&problem_id=" + problem_id
        content = json.loads(s.get(url).content.decode('utf-8'))
        ids = []
        for i in content:
            ids.append(i['id'])
        return ids

    def get_input(self, id):
        url = "https://www.udebug.com/input_api/input/retrieve.json?input_id=" + str(id)
        content = json.loads(s.get(url).content.decode('utf-8'))
        return content[0]

    def get_output(self, id):
        url = "https://www.udebug.com/output_api/output/retrieve.json?input_id=" + str(id)
        content = json.loads(s.get(url).content.decode('utf-8'))
        return content[0]

    def run_user_solution(self):
        # input = bytes(input+'\n','utf-8')
        run_program = subprocess.run(['./run_and_compare.sh'], stdout=subprocess.PIPE)
        # output = run_program.stdout.decode('utf-8')
        # return output

    def run_test(self, input_, expected_output):
        if expected_output.find('Invalid input') != -1:
            return 'ii'

        self.run_user_solution()
        my_output = None
        with open('./my_out.txt', 'r') as content_file:
            my_output = content_file.read()

        if expected_output == my_output:
            return 'y'
        else:
            if output == '':
                print('probably you have segmentation fault as error !!!')
            else:
                print('your output does not match with expected output, and this is the difference: ')
                d = difflib.Differ()
                diff = d.compare(output, expected_output)
                print('\n'.join(diff))
            print('you will find the input where your code failed in the input.txt file')
            return 'n'

    def run_stress_code(self):
        idx = 1
        while True:
            subprocess.run(['./run_rig.sh'], stdout=subprocess.PIPE)
            files = {
                'judge_alias': (None, self.judge_alias),
                'problem_id': (None, self.problem_id),
                'data': ('input.txt', open('input.txt', 'rb')),
            }
            content = json.loads(s.post('https://www.udebug.com/output_api/post_custom_input/output.json',files=files).content.decode('utf-8'))
            input_ = None
            with open('./input.txt', 'r') as content_file:
                input_ = content_file.read()
            expected_output = content[0]
            out = self.run_test(input_=input_, expected_output=expected_output)

            if out =='n':
                return
            elif out=='y':
                print('test ', idx, ': Passed')
            elif out=='ii':
                print('test ', idx, ': Invalid Input')
            idx += 1

    def run_udebug_tests(self):
        l = self.get_list_id_test()
        idx = 1
        for i in l:
            input_ = self.get_input(i)
            # save the input file
            file = open('input.txt', 'w')
            file.write(input_)
            file.close()

            expected_output = self.get_output(i)
            out = self.run_test(input_=input_, expected_output=expected_output)
            if out =='n':
                return
            elif out=='y':
                print('test ', idx, ': Passed')
            elif out=='ii':
                print('test ', idx, ': Invalid Input,  id = ',i)
            idx += 1


if __name__ == '__main__':
    problem_id = input("set your problem id ?\n")
    judge = Udebug('UVA', problem_id)
    # judge.run_udebug_tests()
    judge.run_stress_code()
