# Copyright (C) 2024 Xiaomi Corporation.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


import subprocess
import sys
import time
import json
from appium.webdriver.common.touch_action import TouchAction
# from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium import webdriver

from agent_for_api.API_list import usr_api_list
from agent_for_api.agent_api_prompt import select_api_prompt, select_api_example
from agent_for_api.main_for_api import get_api_list
from data_prompt import *
from app_list import *
from agent_for_api.API_list import *
from selenium.common.exceptions import WebDriverException, InvalidElementStateException, NoSuchElementException

from app_list import app_list
from chatgpt import chatgpt
import re

if __name__ == '__main__':
    # prompt = data_prompt.format(task_description=multiapp_description,
    #                                         examples=multiapp_examples, app_list=app_list, api_list=usr_api_list, requirement=multiapp_requirement)
    # # print(prompt)
    # res = chatgpt(prompt)[0]
    # # print(res)
    # with open("data_instruction.txt", "a") as outfile:
    #     outfile.write(res)
    with open('s_app_s_step.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
    # 使用字典统计每个domain的数量
    domain_count = {}
    for item in data:
        domain = item['domain']
        if domain in domain_count:
            domain_count[domain] += 1
        else:
            domain_count[domain] = 1
    # 输出结果
    print(len(domain_count))
    for domain, count in domain_count.items():
        print(f"{domain}: {count}")
