# Copyright (C) 2024 Xiaomi Corporation.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


# coding: utf-8
import argparse
import subprocess
import sys
import signal
import time
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
# from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium import webdriver
from tqdm import tqdm
from agent_for_api.API_list import usr_api_list
from agent_for_api.agent_api_prompt import select_api_prompt, select_api_example
from agent_for_api.main_for_api import get_api_list
from agent_for_ui.agent_html_prompt import *
from selenium.common.exceptions import WebDriverException, InvalidElementStateException, NoSuchElementException, \
    InvalidArgumentException, StaleElementReferenceException
import json
from xml_to_html import any_tree_to_html
from chatgpt import *
import re
from app_list_MIUI import app_list
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from PIL import Image
import numpy as np
from io import StringIO

max_attempts = 5  # Set the maximum number of retry attempts

# currently tasks are all defined on single-app
'''
How does the entire demo work?
Use appium to obtain the xml information of the interface -> convert the local algorithm into html format ->
package and send the task (task description + env_html) -> agent (planning + action) ->
action is converted into appium's action and acts on the environment -> (task Description+env_html+action_history)->
The new action acts on the environment. (loop construction completed)
'''
# How to agent make decision?：
'''
planning action reward memory?
'''

import xml.etree.ElementTree as ET
from anytree import Node

def parse_xml_to_anytree(xml_code):
    root = ET.fromstring(xml_code)

    def build_anytree(node, element, child_index, seen_elements, counter):
        element_type = element.tag
        # print(element_type)
        # Generate a unique key for the element based on its attributes
        element_key = (
            element_type,
            element.get('resource-id', ''),
            #  content-desc， text兼容问题
            element.get('content-desc', ''),
            element.get('text', ''),
            element.get('clickable', ''),
            element.get('scrollable', ''),
            element.get('package', ''),  ##
            element.get('class', ''),
            element.get('displayed', ''),
            element.get('bounds', ''),
        )
        seen_elements.add(element_key)

        # 检查是否有儿子节点
        is_leaf = not bool(list(element))

        # 检查 text 和 content-desc 是否至少有一个为真
        has_text = bool(element.get('text'))
        has_content_desc = bool(element.get('content-desc'))

        visible = has_text or has_content_desc or 'button' in element_type.lower() or 'edittext' in element.tag.lower()

        leaf_id = counter[0]  # 使用计数器作为 leaf_id
        counter[0] += 1  # 递增计数器

        anytree_node = Node(element_type, parent=node, type=element_type, visible=visible, leaf_id=leaf_id,
                            resource_id=element.get('resource-id'), content_desc=element.get('content-desc'),
                            text=element.get('text'), clickable=element.get('clickable'), is_leaf=is_leaf,
                            scrollable=element.get('scrollable'), package=element.get('package'),
                            class_label=element.get('class'), displayed=element.get('displayed'),
                            bounds=element.get('bounds'))

        for idx, child in enumerate(element):
            # print(idx)
            build_anytree(anytree_node, child, idx, seen_elements, counter)

    is_root_leaf = not bool(list(root))

    anytree_root = Node(root.tag, type=root.tag, visible=True, leaf_id=0,  # 初始计数器为 0
                        resource_id=root.get('resource-id'), content_desc=root.get('content-desc'),
                        text=root.get('text'), clickable=root.get('clickable'),
                        is_leaf=is_root_leaf, scrollable=root.get('scrollable'), package=root.get('package'),
                        class_label=root.get('class'), displayed=root.get('displayed'), bounds=root.get('bounds'))

    seen_elements = set()
    counter = [1]  # 使用列表来存储计数器的值，以便在递归中共享

    for idx, child in enumerate(root):
        # print("out",idx)
        build_anytree(anytree_root, child, idx, seen_elements, counter)

    return anytree_root


def screen_swipe(driver, start_x, start_y, end_x, end_y, duration=1000):
    # use duration to control the speed of swipe
    success = False
    while not success:
        try:
            driver.swipe(start_x, start_y, end_x, end_y, duration)
            success = True  # If the page source is acquired, set success to True to exit the loop
        except WebDriverException as e:
            print(f"Encountered an error: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying


def get_memory(history_actions):
    memory_list = []
    # print(history_actions)
    for round_number, action_info in enumerate(history_actions, 1):
        key = None
        if 'action' in action_info:
            key = 'action'
            # round_number += 1  # 仅当键是 'action' 时增加 round_number
        elif 'thought' in action_info:
            key = 'thought'
        elif 'API call' in action_info:
            key = 'API call'
            # round_number += 1  # 仅当键是 'API call' 时增加 round_number
        else:
            key = 'unknown'
            # round_number += 1  # 对于其他未知类型也增加 round_number
        detail = action_info.get(key, 'No detail')
        # print(f"{key}: {detail}")
        memory_list.append(f"{action_info}")
        # memory_list.append(f"{key}: {detail}")

    if memory_list != []:
        # memory_list = memory_list[-10:]   # 记忆压缩。
        memory = "\n".join(memory_list)
    else:
        memory = "No action has been completed yet"
    return memory


from selenium.common.exceptions import WebDriverException
import re, time

def find_element1(element, driver):
    id_match = re.search(r'id="([^"]+)"', element)
    text_match = re.search(r'>\s*([^<>]+)\s*<', element)
    alt_match = re.search(r'description="([^"]+)"', element)
    class_match = re.search(r'class="([^"]+)"', element)
    if id_match:
        id_value = id_match.group(1).strip()
        # print("-----------------------------------------", id_value)
    if text_match:
        text_value = text_match.group(1).strip()
        # print(text_value)
        if text_value.isspace() or not text_value:
            text_match = False
            # print("-----------------------------------------", text_match)

    if alt_match:
        alt_value = alt_match.group(1).strip()
        # print("-----------------------------------------", alt_value)
    if class_match:
        class_value = class_match.group(1).strip()

    find = False
    if text_match and alt_match and id_match :
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR,
                                            f'new UiSelector().text("{text_value}").description("{alt_value}").resourceId("{id_value}")')
                success = True  # 如果页面源获取成功，设置success为True以退出循环
            except WebDriverException as e:
                attempt_count += 1
                print(f"遇到错误: {e}. 重试中...")
                time.sleep(5)  # 重试前等待5秒
        if not success:
            print("服务器端错误")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print(r"警告: 存在多个具有相同text_value\description\id的元素，这可能导致错误！")
        if find:
            return list

    if text_match and alt_match :
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR,
                                            f'new UiSelector().text("{text_value}").description("{alt_value}")')
                success = True  # 如果页面源获取成功，设置success为True以退出循环
            except WebDriverException as e:
                attempt_count += 1
                print(f"遇到错误: {e}. 重试中...")
                time.sleep(5)  # 重试前等待5秒
        if not success:
            print("服务器端错误")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print(r"警告: 存在多个具有相同text_value\description的元素，这可能导致错误！")
        if find:
            return list

    if id_match and text_match:
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{id_value}").text("{text_value}")')
                # print("------------------------",list)
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        # list = driver.find_elements(By.ID, id_value)
        if success == False:
            print("serve side error")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print(r"警告: 存在多个具有相同text_value\id的元素，这可能导致错误！")
        if find:
            return list

    if id_match and alt_match:
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{id_value}").description("{alt_value}")')
                # print("------------------------",list)
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        # list = driver.find_elements(By.ID, id_value)
        if success == False:
            print("serve side error")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print(r"警告: 存在多个具有相同description\id的元素，这可能导致错误！")
        if find:
            return list

    if text_match:
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR,
                                            f'new UiSelector().text("{text_value}")')
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        if success == False:
            print("serve side error")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print("警告: 存在多个具有相同text的元素，这可能导致错误！")
        if find:
            return list

    if alt_match:
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR,
                                            f'new UiSelector().description("{alt_value}")')
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        if success == False:
            print("serve side error")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print("警告: 存在多个具有相同description的元素，这可能导致错误！")
        if find:
            return list

    if class_match:
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR,
                                            f'new UiSelector().className("{class_value}")')
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        # list = driver.find_elements(By.ID, id_value)
        if success == False:
            print("serve side error")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print("警告: 存在多个具有相同class的元素，这可能导致错误！")
        if find:
            return list

    if id_match:
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                list = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR,
                                            f'new UiSelector().resourceId("{id_value}")')
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        if success == False:
            print("serve side error")
            return None
        if len(list) > 0:
            find = True
        if len(list) > 1:
            print("警告: 存在多个具有相同id的元素，这可能导致错误！")
        if find:
            return list



    print("没有定位到对应的元素")
    return None


def find_elements_by_criteria(driver, max_attempts=3, **criteria):
    selectors = []
    if 'id' in criteria:
        selectors.append(f'resourceId("{criteria["id"]}")')
    if 'text' in criteria:
        selectors.append(f'text("{criteria["text"]}")')
    if 'alt' in criteria:
        selectors.append(f'description("{criteria["alt"]}")')
    if 'class' in criteria:
        selectors.append(f'className("{criteria["class"]}")')

    if not selectors:
        print("没有定位到对应的元素")
        return None

    ui_selector = f'new UiSelector().' + '.'.join(selectors)
    attempt_count = 0
    while attempt_count < max_attempts:
        try:
            elements = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR, ui_selector)
            if len(elements) > 0:
                if len(elements) > 1:
                    print(f"警告: 存在多个具有相同属性的元素，这可能导致错误！")
                return elements
            attempt_count += 1
        except WebDriverException as e:
            print(f"遇到错误: {e}. 重试中...")
            time.sleep(5)
            attempt_count += 1

    print("服务器端错误或超过最大尝试次数")
    return None


def find_element(element, driver, max_attempts=3):
    id_match = re.search(r'id="([^"]+)"', element)
    text_match = re.search(r'>\s*([^<>]+)\s*<', element)
    alt_match = re.search(r'description="([^"]+)"', element)
    class_match = re.search(r'class="([^"]+)"', element)

    criteria = {}
    if id_match:
        criteria['id'] = id_match.group(1).strip()
    if text_match and not text_match.group(1).isspace():
        criteria['text'] = text_match.group(1).strip()
    if alt_match:
        criteria['alt'] = alt_match.group(1).strip()
    if class_match:
        criteria['class'] = class_match.group(1).strip()

    return find_elements_by_criteria(driver, max_attempts, **criteria)


def actions(res, history_actions, driver):
    if 'click(' in res:
        first_angle_bracket = res.find('<')
        first_reangle_bracket = res.find('>')
        second_angle_bracket = res.find('>', first_reangle_bracket + 1)
        # Extract the element from between these positions
        text = res[first_angle_bracket:second_angle_bracket + 1]
        list = find_element(text, driver)
        if list == None:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element click({text})"})
        elif len(list) == 0:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element click({text})"})
        else:
            try:
                list[0].click()
                history_actions.append({"Action": f"click({text})"})
            except WebDriverException as e:
                print(f"Encountered an error: {e}. Retrying...")
                history_actions.append({"Action": f"[Fail]: Unsuccessful click click({text})"})

    elif 'press(' in res:
        action = TouchAction(driver)
        first_angle_bracket = res.find('<')
        first_reangle_bracket = res.find('>')
        second_angle_bracket = res.find('>', first_reangle_bracket + 1)
        # Extract the element from between these positions
        text = res[first_angle_bracket:second_angle_bracket + 1]
        list = find_element(text, driver)
        if list == None:
            print("Warning: Invalid element")
        elif len(list) == 0:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element press({text})"})
        else:
            try:
                action.press(list[0]).wait(1000).release().perform()
                history_actions.append({"Action": f"press({text})"})
            except WebDriverException as e:
                print(f"Encountered an error: {e}. Retrying...")
                history_actions.append({"Action": f"[Fail]: Unsuccessful press({text})"})

    elif 'zoom(' in res:
        action1 = TouchAction(driver)
        action2 = TouchAction(driver)
        zoom_action = MultiAction(driver)
        first_angle_bracket = res.find('<')
        first_reangle_bracket = res.find('>')
        second_angle_bracket = res.find('>', first_reangle_bracket + 1)
        # Extract the element from between these positions
        text = res[first_angle_bracket:second_angle_bracket + 1]
        list = find_element(text, driver)
        if list == None:
            print("Warning: Invalid element")
        elif len(list) == 0:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element Zoom({text})"})
        else:
            try:
                action1.press(list[0]).move_to(x=0, y=-100)  # 向上移动
                action2.press(list[0]).move_to(x=0, y=100)  # 向下移动
                zoom_action.add(action1, action2)
                zoom_action.perform()
                history_actions.append({"Action": f"Zoom({text})"})
            except WebDriverException as e:
                print(f"Encountered an error: {e}. Retrying...")
                history_actions.append({"Action": f"[Fail]: Unsuccessful zoom({text})"})

    elif 'pinch(' in res:
        action1 = TouchAction(driver)
        action2 = TouchAction(driver)

        first_angle_bracket = res.find('<')
        first_reangle_bracket = res.find('>')
        second_angle_bracket = res.find('>', first_reangle_bracket + 1)
        # Extract the element from between these positions
        text = res[first_angle_bracket:second_angle_bracket + 1]
        list = find_element(text, driver)
        if list == None:
            print("Warning: Invalid element")
        elif len(list) == 0:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element pinch({text})"})
        else:
            try:
                action1.press(x=list[0].location['x'], y=list[0].location['y'] - 100).move_to(list[0])
                action2.press(x=list[0].location['x'], y=list[0].location['y'] + 100).move_to(list[0])

                pinch_action = MultiAction(driver)
                pinch_action.add(action1, action2)
                pinch_action.perform()
                history_actions.append({"Action": f"pinch({text})"})
            except WebDriverException as e:
                print(f"Encountered an error: {e}. Retrying...")
                history_actions.append({"Action": f"[Fail]: Unsuccessful pinch({text})"})

    elif 'input(' in res:
        first_angle_bracket = res.find('<')
        first_reangle_bracket = res.find('>')
        second_angle_bracket = res.find('>', first_reangle_bracket + 1)
        # Extract the element from between these positions
        element = res[first_angle_bracket:second_angle_bracket + 1]
        input_context = res[second_angle_bracket + 2:-1].strip()
        input_context = input_context.strip('\'\"')
        # print(element)
        # print(input_context)
        list = find_element(element, driver)
        if list == None:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element. input({element}, {input_context})"})
        elif len(list) == 0:
            print("Warning: Invalid element")
            history_actions.append({"Action": f"[Fail]: Invalid element. input({element}, {input_context})"})
        else:
            try:
                # 点击元素
                list[0].click()
                history_actions.append({"Action": f"click({element})"})
                try:
                    WebDriverWait(driver, 1).until(
                        EC.staleness_of(list[0])
                    )
                    # 等待刷新

                except TimeoutException:
                    # 如果元素不存在或不可见，不执行input操作
                    list[0].send_keys(input_context)
                    history_actions.append({"Action": f"input({element}, {input_context})"})

            except InvalidElementStateException as e:
                print(f"Encountered an error: {e}. Retrying...")
                history_actions.append(
                    {"Action": f"[Fail]: InvalidElementStateException input({element}, {input_context})"})
            except NoSuchElementException as e:
                print(f"Encountered an error: {e}. Retrying...")
                history_actions.append({"Action": f"[Fail]: NoSuchElementException input({element}, {input_context})"})
            except InvalidArgumentException as e:
                print(f"Encountered an error: {e}. Input value might be invalid for the element.")
                history_actions.append(
                    {"Action": f"[Fail]: InvalidArgumentException input({element}, {input_context})"})
            except StaleElementReferenceException as e:
                print(f"Encountered an error: {e}. The element might have been detached from the DOM.")
                history_actions.append(
                    {"Action": f"[Fail]: StaleElementReferenceException input({element}, {input_context})"})

    elif 'scroll(' in res or 'swipe(' in res:
        action = TouchAction(driver)

        numbers = re.findall(r'\d+', res)
        # 将找到的数字转换成整数并分配给相应的变量
        x1, y1, x2, y2 = map(int, numbers[:4])
        max_value = max(x1, y1, x2, y2)
        # 对滑动操作的参数进行调整，以免超出边界。
        if x1 == max_value:
            x1 -= 50
        if y1 == max_value:
            y1 -= 50
        if x2 == max_value:
            x2 -= 50
        if y2 == max_value:
            y2 -= 50

        # 如果某个数等于0，则加50
        if x1 == 0:
            x1 += 50
        if y1 == 0:
            y1 += 50
        if x2 == 0:
            x2 += 50
        if y2 == 0:
            y2 += 50
        success = False
        attempt_count = 0
        while not success and attempt_count < max_attempts:
            try:
                action.press(x=x1, y=y1).wait(ms=1000).move_to(x=x2, y=y2).release().perform()
                # driver.swipe(x1, y1, x2, y2, duration=1000) # swipe的效果不够好。
                success = True  # If the page source is acquired, set success to True to exit the loop
            except WebDriverException as e:
                attempt_count += 1
                print(f"Encountered an error: {e}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        if success:
            history_actions.append({"Action": f"scroll([{x1},{y1}][{x2},{y2}])"})
        else:
            print("[Fail]: unsucess scroll.")
            history_actions.append({"Action": f"[Fail]: unsuccessful scroll scroll([{x1},{y1}][{x2},{y2}])"})


def get_page_source(driver):
    attempt_count = 0
    success = False
    xml_source = None
    while not success and attempt_count < max_attempts:
        try:
            xml_source = driver.page_source
            success = True  # If the page source is acquired, set success to True to exit the loop
        except WebDriverException as e:
            attempt_count += 1
            print(f"Encountered an error: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            # driver.quit()
            # driver = open_driver()
    return xml_source, driver


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return "API execution successful"
    else:
        return f"API execution failed with error: {result.stderr}"


def api(res, history_actions):
    matches = re.findall(r'\[(.*)\]', res)
    success = False
    for match in matches:
        adb_command = match
        print("[API CALL]: ", adb_command)
        result = run_command(adb_command)
        print("[APi Function Call Result]: \033[34m" + result + "\033[0m")
        if 'success' in result:
            success = True
        # 有待商榷，执行失败的信息是否应该放在记录里，这样可以避免重复生成错误的API
        if "successful" in result:
            history_actions.append({f"API call": f"{adb_command}. [Call result]:{result}"})
        # history_actions.append({f"[API call]": f"{adb_command}. [Call result]:{result}"})
    return success


def get_success_memory(history_actions):
    memory_list = []
    counter = 0  # Initialize a counter
    for action_info in history_actions:
        key = None
        # 检查动作类型
        if 'action' in action_info or 'thought' in action_info:
            if 'action' in action_info:
                key = 'action'
            elif 'thought' in action_info:
                key = 'thought'

            # 当遇到 'action' 或 'thought' 时，每两次迭代增加一次计数
            if counter % 2 == 0:
                round_number = counter // 2 + 1
            counter += 1

        elif 'API call' in action_info:
            key = 'API call'
            round_number = counter // 2 + 1  # 保持当前的 round_number

        elif 'App Select and Plan' in action_info:
            key = 'App Select and Plan'
            round_number = counter // 2 + 1  # 保持当前的 round_number

        else:
            key = 'unknown'
            round_number = counter // 2 + 1  # 保持当前的 round_number

        detail = action_info.get(key, 'No detail')
        memory_list.append(f"Step {round_number}: {key}: {detail}")

    memory = "\n".join(memory_list)
    return memory


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extracting only id, app, packagename, query, and check_point information
    extracted_data = []
    for item in data:
        id = item.get('id')
        app = item.get('app')
        package_name = item['check_point'].get('package', [])
        query = item.get('query')
        check_point = item.get('check_point')
        extracted_data.append({
            'id': id,
            'app': app,
            'packagename': package_name,
            'query': query,
            'check_point': check_point
        })

    return extracted_data


def calculate_package_coverage(data_item, action_history):
    # 初始化覆盖数量
    coverage_count = 0
    if 'check_point' in data_item and 'package' in data_item['check_point']:
        package_names = data_item['check_point']['package']
        # 遍历 package_names 中的每个元素
        for package_name in package_names:
            # 检查元素是否出现在 action_history 的任何动作中
            if any(package_name in action for action in action_history):
                coverage_count += 1

        return coverage_count / len(package_names)
    else:
        return 0


def check_point_passed(check_point_value, action_history):
    if '|' in check_point_value:
        # 如果列表中有 '|', 那么任何一个 action_history 中的动作包含至少一个元素即通过
        return any(cp_elem in action for cp_elem in check_point_value if cp_elem != '|' for action in action_history), 1
    elif '&' in check_point_value:
        # 如果列表中有 '&', 那么 action_history 中的动作需要包含所有元素
        return all(cp_elem in action for cp_elem in check_point_value if cp_elem != '&' for action in action_history), 1
    else:
        if isinstance(check_point_value, list):
            total_elems = len(check_point_value)
            passed_elems = sum(any(cp_elem in action for action in action_history) for cp_elem in check_point_value)
            return passed_elems, total_elems
        else:
            return any(check_point_value in action for action in action_history), 1


# check point scores
def check_points(data_item, action_history):
    checkpoints = ['activity', 'resource-id', 'text', 'package', 'api']
    total_checkpoints = 0
    passed_checkpoints = 0

    for cp in checkpoints:
        if cp in data_item['check_point'] and data_item['check_point'][cp]:  # check existence
            check_point_value = data_item['check_point'][cp]
            if isinstance(check_point_value, list):
                passed, total = check_point_passed(check_point_value, action_history)
                passed_checkpoints += passed
                total_checkpoints += total
            else:
                # 直接比较
                total_checkpoints += 1
                if any(check_point_value in action for action in action_history):
                    passed_checkpoints += 1

    return passed_checkpoints / total_checkpoints if total_checkpoints > 0 else 0


def format_api_info_as_text(text, data):
    """
    Format the API information as text in the specified format if the name_ch or name_en of an app is found in the text.
    :param text: The string in which to search for app names.
    :param data: The JSON data containing app information.
    :return: A string formatted as a dictionary with app names as keys and their API information as values.
    """
    formatted_info = {}
    general_keys_api = [
        {
            "ADB Command": "adb shell input keyevent KEYCODE_BACK",
            "Function Description": "Return to previous page",
            "Parameter Information": "No additional parameters required."
        },
        {
            "ADB Command": "adb shell input keyevent KEYCODE_HOME",
            "Function Description": "go to home page, which is equal to click the home button",
            "Parameter Information": "No additional parameters required."
        },
        {
            "ADB Command": "adb shell input keyevent KEYCODE_SLEEP",
            "Function Description": "Set the device to sleep",
            "Parameter Information": "No additional parameters required."
        },
        {
            "ADB Command": "adb shell screencap -p /sdcard/screenshot.png",
            "Function Description": "Takes a screenshot and saves it.",
            "Parameter Information": "No additional parameters required."
        },
        {
            "ADB Command": "adb shell input keyevent KEYCODE_WAKEUP",
            "Function Description": "Wake up the device",
            "Parameter Information": "No additional parameters required."
        }
    ]
    formatted_info["通用按键"] = general_keys_api
    # 如果text是中文，则应该直接匹配, \b带有词边界。
    # if app['name_ch'] in text or app['name_en'] in text
    for app in data:
        # if re.search(r'\b' + re.escape(app['name_ch']) + r'\b', text) or re.search(
        #         r'\b' + re.escape(app['name_en']) + r'\b', text):
        if app['name_ch'] in text or app['name_en'] in text:
            api_info = app['api']
            if api_info:
                formatted_info[app['name_ch']] = api_info

    # Convert the dictionary to a string formatted as a dictionary
    formatted_text = json.dumps(formatted_info, indent=2, ensure_ascii=False)
    return formatted_text


def map_and_reverse_complete_interactive_elements(html_content):  # 建立元素和数值的映射关系；
    lines = html_content.split('\n')
    interactive_elements = {}
    counter = 1  # Start numbering from 1

    for line in lines:
        # Check if the line contains a clickable, scrollable or input element
        if 'clickable="true"' in line or 'scrollable="true"' in line or 'input' in line:
            # Map the entire line (HTML tag) to the number
            interactive_elements[counter] = line.strip()
            counter += 1  # Increment the counter for the next interactive element

    return interactive_elements


def calculate_scroll_parameters(window_size, html, direction, scroll_type='short'):
    width = window_size['width']
    height = window_size['height']
    safe_margin = 10   # 安全边界距离
    match = re.search(r'bounds="\[([0-9]+,[0-9]+)\]\[([0-9]+,[0-9]+)\]"', html)
    bounds = [match.group(1), match.group(2)]
    # 解析bounds字符串"[x1,y1][x2,y2]"
    x1, y1 = map(int, bounds[0].split(','))
    x2, y2 = map(int, bounds[1].split(','))

    # 计算中点坐标
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    if scroll_type == 'short':
        # 短距离滚动
        offset_x = (x2 - x1) // 4
        offset_y = (y2 - y1) // 4
        scroll_coordinates = {
            'up': ([mid_x, mid_y + offset_y], [mid_x, mid_y - offset_y]),
            'down': ([mid_x, mid_y - offset_y], [mid_x, mid_y + offset_y]),
            'left': ([mid_x + offset_x, mid_y], [mid_x - offset_x, mid_y]),
            'right': ([mid_x - offset_x, mid_y], [mid_x + offset_x, mid_y])
        }
    elif scroll_type == 'long':
        # 长距离滚动
        if direction == 'up':
            start_x = end_x = mid_x
            start_y = y2 - safe_margin
            end_y = safe_margin
        elif direction == 'down':
            start_x = end_x = mid_x
            start_y = y1 + safe_margin
            end_y = height - safe_margin
        elif direction == 'left':
            start_y = end_y = mid_y
            start_x = x2 - safe_margin
            end_x = safe_margin
        elif direction == 'right':
            start_y = end_y = mid_y
            start_x = x1 + safe_margin
            end_x = width - safe_margin
        else:
            return None  # 无效方向
        scroll_coordinates = {
            direction: ([start_x, start_y], [end_x, end_y])
        }
    else:
        return None  # 无效的滚动类型

    return scroll_coordinates[direction]

    # # 定义滚动偏移量
    # offset_x = (x2 - x1) // 4
    # offset_y = (y2 - y1) // 4
    #
    # # 根据方向计算滚动起始和结束坐标
    # scroll_directions = {
    #     'up': ([mid_x, mid_y + offset_y], [mid_x, mid_y - offset_y]),
    #     'down': ([mid_x, mid_y - offset_y], [mid_x, mid_y + offset_y]),
    #     'left': ([mid_x + offset_x, mid_y], [mid_x - offset_x, mid_y]),
    #     'right': ([mid_x - offset_x, mid_y], [mid_x + offset_x, mid_y])
    # }

    # return scroll_directions[direction]


def process_user_input(window_size, user_input, elements_map):  # 将用户的输入转化为实际的执行指令
    # Splitting the input for action and parameters
    parts = user_input.split('(', 1)
    action = parts[0].strip().lower()  # Action: click, scroll, input
    params = parts[1].rstrip(')').split(',') if len(parts) > 1 else []  # Parameters in the parentheses

    # Defining the action command and parameters
    action_command = ''
    params_command = ''

    # Determine the action and construct corresponding command
    if action == 'click':
        action_command = 'click'
        if params and params[0].isdigit() and int(params[0]) in elements_map:
            params_command = elements_map[int(params[0])]
    elif action == 'press':
        action_command = 'press'
        if params and params[0].isdigit() and int(params[0]) in elements_map:
            params_command = elements_map[int(params[0])]
    elif action == 'zoom':
        action_command = 'zoom'
        if params and params[0].isdigit() and int(params[0]) in elements_map:
            params_command = elements_map[int(params[0])]
    elif action == 'pinch':
        action_command = 'pinch'
        if params and params[0].isdigit() and int(params[0]) in elements_map:
            params_command = elements_map[int(params[0])]
    elif action == 'scroll':
        action_command = 'scroll'
        # Defining scroll directions as start and end coordinates
        if params and params[0].isdigit() and int(params[0]) in elements_map:
            html_element = elements_map[int(params[0])]
            direction = str(params[1]).strip()
            if len(params) > 2:
                scroll_type = 'long'
            else:
                scroll_type = 'short'
            params_command = calculate_scroll_parameters(window_size, html_element, direction, scroll_type)
    elif action == 'input':
        action_command = 'input'
        if params and params[0].isdigit() and int(params[0]) in elements_map:
            params_command = elements_map[int(params[0])]
            if len(params) > 1:
                params_command += f", '{params[1]}'"

    # Construct the final command
    final_command = f"{action_command}({params_command})"

    return final_command


# def display_html_and_mapping(html_content, elements_map):
#     # Outputting the entire HTML content
#     print("[HTML Content]:")
#     print(html_content)
#     print("[Interactive Elements Mapping]:")
#     # Iterating through the elements map and printing the index and description
#     # Initialize categories
#     clickables = {}
#     scrollables = {}
#     inputs = {}  # Assuming we could identify input elements somehow
#
#     # Iterating through the elements map to categorize
#     for index, html in elements_map.items():
#         if 'input' in html:
#             inputs[index] = html
#         elif 'scrollable="true"' in html:
#             scrollables[index] = html
#         elif 'clickable="true"' in html:
#             clickables[index] = html
#
#
#     # Outputting categorized elements
#     categories = [("Clickables", clickables), ("Scrollables", scrollables), ("Inputs", inputs)]
#     for category_name, category_map in categories:
#         if category_map:  # Only print if category has items
#             print(f"[{category_name}]:")
#             max_index_length = len(str(max(category_map.keys()))) if category_map else 0
#             for index, html in category_map.items():
#                 # Attempting to extract a brief description
#                 if 'description="' in html:
#                     description = html.split('description="')[1].split('"')[0]
#                 else:
#                     text_content = html.split('>')[1].split('<')[0] if '>' in html and '<' in html else ""
#                     description = text_content.strip()
#                     # Adding bounds if the element is scrollable
#                 if 'scrollable="true"' in html and 'bounds="' in html:
#                     bounds = html.split('bounds="')[1].split('"')[0]
#                     description += f" ({bounds})" if bounds else ""
#                 if description:  # Only print if there's a description or text content
#                     print(f"{index:{max_index_length}}: {description}")

def display_html_and_mapping(html_content, elements_map):
    from io import StringIO

    # Initialize categories
    clickables = {}
    scrollables = {}
    inputs = {}  # Assuming we could identify input elements somehow

    # Iterating through the elements map to categorize
    for index, html in elements_map.items():
        if 'input' in html:
            inputs[index] = html
        elif 'EditText' in html:
            inputs[index] = html
        elif 'scrollable="true"' in html:
            scrollables[index] = html
        elif 'clickable="true"' in html:
            clickables[index] = html

    # Using StringIO to capture output
    output = StringIO()

    # Outputting categorized elements
    categories = [("Clickables", clickables), ("Scrollables", scrollables), ("Inputs", inputs)]
    for category_name, category_map in categories:
        if category_map:  # Only print if category has items
            output.write(f"[{category_name}]:\n")
            max_index_length = len(str(max(category_map.keys()))) if category_map else 0
            for index, html in category_map.items():
                description = ""
                # Extracting a brief description
                if 'description="' in html:
                    description = html.split('description="')[1].split('"')[0]
                elif 'class="' in html:
                    class_name = html.split('class="')[1].split('"')[0]
                    # Check if there is visible text inside the element
                    inner_text = html.split('>')[1].split('<')[0] if '>' in html and '<' in html else ""
                    if not inner_text.strip():
                        description = f"Empty {class_name}"
                    else:
                        description = inner_text.strip()

                # Adding bounds if the element is scrollable
                if 'scrollable="true"' in html and 'bounds="' in html:
                    bounds = html.split('bounds="')[1].split('"')[0]
                    description += f" ({bounds})" if bounds else ""

                if description:  # Only print if there's a description or text content
                    output.write(f"{index:{max_index_length}}: {description}\n")

    # Return the output as a string
    return output.getvalue()
def display_html_and_mapping_1(html_content, elements_map):
    # Outputting the entire HTML content
    # Initialize categories
    clickables = {}
    scrollables = {}
    inputs = {}  # Assuming we could identify input elements somehow

    # Iterating through the elements map to categorize
    for index, html in elements_map.items():
        if 'input' in html:
            inputs[index] = html
        elif 'EditText' in html:
            inputs[index] = html
        elif 'scrollable="true"' in html:
            scrollables[index] = html
        elif 'clickable="true"' in html:
            clickables[index] = html

    # Outputting categorized elements
    categories = [("Clickables", clickables), ("Scrollables", scrollables), ("Inputs", inputs)]
    for category_name, category_map in categories:
        if category_map:  # Only print if category has items
            print(f"[{category_name}]:")
            max_index_length = len(str(max(category_map.keys()))) if category_map else 0
            for index, html in category_map.items():
                description = ""
                # Extracting a brief description
                if 'description="' in html:
                    description = html.split('description="')[1].split('"')[0]
                elif 'class="' in html:
                    class_name = html.split('class="')[1].split('"')[0]
                    # Check if there is visible text inside the element
                    inner_text = html.split('>')[1].split('<')[0] if '>' in html and '<' in html else ""
                    if not inner_text.strip():
                        description = f"Empty {class_name}"
                    else:
                        description = inner_text.strip()

                # Adding bounds if the element is scrollable
                if 'scrollable="true"' in html and 'bounds="' in html:
                    bounds = html.split('bounds="')[1].split('"')[0]
                    description += f" ({bounds})" if bounds else ""

                if description:  # Only print if there's a description or text content
                    print(f"{index:{max_index_length}}: {description}")

def click_cancel(driver):
    # cancel_button = driver.find_element_by_id("com.miui.systemAdSolution:id/cancel_dialog")
    # if cancel_button:
    #     cancel_button.click()
    cancel_button = driver.find_elements(MobileBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("取消")')
    if cancel_button:
        cancel_button[0].click()


def open_driver(command_executor, desired_caps):
    success = False
    attempt_count = 0
    while not success and attempt_count < max_attempts:
        try:
            driver = webdriver.Remote(command_executor, desired_caps)
            success = True
        except WebDriverException as e:
            attempt_count += 1
            print(f"Encountered an error: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
    if not success:
        print(f"Failed to connect after {max_attempts} attempts. Exiting program.")
        driver.quit()
        sys.exit()  # Exit the program if connection is not successful
    else:
        print("[Device connected successfully!]")
        return driver


def compare_images(img_path1, img_path2, threshold):
    """
    Compare two images and determine if they are the same based on pixel values.

    :param img_path1: Path to the first image.
    :param img_path2: Path to the second image.
    :param threshold: The threshold for considering the images as the same.
                      This is the percentage of pixels that must be the same.
    :return: True if the images are the same based on the given threshold, False otherwise.
    """
    # Open the images
    try:
        img1 = Image.open(img_path1)
        img2 = Image.open(img_path2)
    except IOError:
        print("Error in opening one of the images.")
        return False

    # Convert images to numpy arrays
    img1_array = np.array(img1)
    img2_array = np.array(img2)

    # Check if dimensions are the same
    if img1_array.shape != img2_array.shape:
        print("Images have different dimensions.")
        return False

    # Calculate the number of equal pixels
    equal_pixels = np.sum(img1_array == img2_array)

    # Total number of pixels
    total_pixels = img1_array.size

    # Calculate the ratio of equal pixels
    similarity_ratio = equal_pixels / total_pixels
    dif_ratio = 1 - similarity_ratio


    return dif_ratio > threshold


def get_parser():
    parser = argparse.ArgumentParser(description="Agent for mobile phone")
    parser.add_argument('--temperature', type=float, default=0.3, help='temperature')
    parser.add_argument('--model', type=str, default='gpt-4-turbo-2024-04-09', help='model to use')
    parser.add_argument('--user_name', type=str, default='xuweikai', help='user name')
    parser.add_argument('--dataset', type=str, default='../data/s_app_s_step.json', help='dataset to use')
    parser.add_argument('--max_steps', type=int, choices=range(0, 50), default=10, help='numbers of steps')
    parser.add_argument('--start_index', type=int, default=4, help='start_index')
    parser.add_argument('--device_name', type=str, default='YD7HAEKB49Q4PZOJ', help='device to use')
    parser.add_argument('--systemPort', type=int, default=8201, help='appium client port')
    parser.add_argument('--command_executor', type=str, default='http://127.0.0.1:4723/wd/hub', help='appium server port')
    parser.add_argument('--appPackage', type=str, default='ctrip.android.view',
                        help='which app to randomly walk')
    return parser


parser = get_parser()
args = parser.parse_args()
should_continue = True
# STOP_SIGNAL_FILE = "../html/stop_signal.txt"


def main():
    global should_continue
    t = time.localtime()
    model_name = args.model.replace('/', '-')
    logfilename = '../result/results-' + model_name + '--t' + str(
        args.temperature) + '--' + time.strftime("%Y-%m-%d-%H-%M-%S", t) + '.jsonl'
    with open(logfilename, 'w', encoding='utf-8') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", t) + '\n')  # write each result as a new line
        f.write('model: ' + str(args.model) + '\n')
        f.write('max_steps: ' + str(args.max_steps) + '\n')
        f.write("--------------------------------\n")

    # read data
    data = read_json_file(args.dataset)
    # read APP list
    with open('../app_list_MIUI.json', 'r', encoding='utf-8') as file:
        all_app_list = json.load(file)

    print("***[TEST BEGIN]***")

    cnt = 0
    total_steps = 0
    pass_cnt = 0
    check_result_1 = 0
    check_result_2 = 0
    app_Packagename = "com.miui.weather2"
    device_name = args.device_name
    systemPort = args.systemPort
    command_executor = args.command_executor
    desired_caps = {
        "platformName": "Android",
        "deviceName": device_name,
        "udid": device_name,
        "platformVersion": "13.0",
        'automationName': 'uiautomator2',
        'noReset': True,
        'newCommandTimeout': 6000,
        'uiautomator2ServerLaunchTimeout': 60000,
        'systemPort': systemPort
    }
    print(desired_caps)
    print("[start connected]")
    # driver to connect to the emulator
    global driver
    driver = open_driver(command_executor, desired_caps)

    start_index = args.start_index  # Change this to the index you want to start testing from
    # screenshot_path = f"C:/Users/mi/PycharmProjects/Agent_base_appium/result/screenshot/screenshot_{systemPort}_0.png"
    # adb_command = f"adb exec-out screencap -p > {screenshot_path}"
    # result = subprocess.run(adb_command, shell=True)
    # result 用于对ADB的指令测试。
    for data_item in tqdm(data[start_index:], desc="Automatic Testing"):
        # for data_item in tqdm(data, desc="Automatic Testing"):
        driver.close_app()
        # 清理正在前台的app
        history_actions = []
        cnt += 1
        task = ''.join(data_item['query'])
        # stop_command = ["adb", "-s", device_name, "shell", "am", "force-stop", app_Packagename]
        # subprocess.run(stop_command)
        # click_cancel(driver)
        #

        # 这个方式会导致 socket hang up 目前尚未解决。
        # open switch app
        # switch_command = f"adb shell input keyevent KEYCODE_APP_SWITCH"
        # subprocess.run(switch_command)
        # time.sleep(3)
        # # 清理所有正在后台运行的程序
        # id_value = "com.miui.home:id/clearAnimView"
        # try:
        #     x = driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{id_value}")')
        #     x.click()
        #     print("[All apps delete.]")
        # except NoSuchElementException:
        #     print(f"[No app is running.]")
        # 保证在主界面
        reboot_command = f"adb shell input keyevent KEYCODE_HOME"
        # 执行命令
        subprocess.run(reboot_command)
        print("\n[Go back to Home page]")

        # start_command = f"./emulator -avd miui_emulator_phone_34 -snapshot reset-env-3 -sysdir ~/.miui/system-images/android-34/miui_emulator_phone_34/xiaomi/x86_64"
        # # start device and load the snapshot.
        # avd_name = "emulator-5554"
        # snapshot_name = "reset-env-3"
        # emulator_path = r"emulator"
        #
        # print("[ReSet The Environment]: ", start_command)
        # try:
        #     # 执行命令
        #     subprocess.run(start_command, shell=True, check=True)
        #
        # except subprocess.CalledProcessError as e:
        #     print(f"命令执行失败: {e}")
        # except FileNotFoundError:
        #     print("找不到'emulator'命令，请确保已将其添加到您的 PATH 环境变量中。")
        # except Exception as e:
        #     print(f"发生了未知错误: {e}")

        # select the app
        xml_source, driver = get_page_source(driver)
        # print(xml_source)
        anytree_root = parse_xml_to_anytree(xml_source)
        # translate xml to html
        html_code = any_tree_to_html(anytree_root, 0, None)
        # print("[HTML UI]：", html_code)
        print(time.strftime("%Y-%m-%d-%H-%M-%S", t))
        prompt = app_selection_prompt.format(app_selection_example=app_selection_example,
                                             task_description=task, apps_information=app_list)
        res = get_model_response(args, prompt)
        # res = ('This is a overall plan. ')
        print("[Task]: ", task)
        print("[App Select and Plan]: \033[34m" + res + "\033[0m")
        plan = res
        api_list = format_api_info_as_text(plan, all_app_list)

        # # agent with environment
        round_number = 0
        task_continue = True
        thought = "I have just specified the plan. Now I should execute it according to the plan and take the first step of the plan."
        # 每一轮决策中，api和ui只能调用一个。
        # screenshot_path = f"C:/Users/mi/PycharmProjects/Agent_base_appium/result/screenshot_{device_name}/screenshot{device_name}_0.png"
        # adb_command = f"adb exec-out screencap -p > {screenshot_path}"
        # subprocess.run(adb_command, shell=True)

        while round_number < args.max_steps:
            print(r"------------Round {round}------------".format(round=round_number))
            api_use = False
            round_number += 1

            xml_source, driver = get_page_source(driver)
            if xml_source == None:
                print("error")
                sys.exit()
            anytree_root = parse_xml_to_anytree(xml_source)
            # translate xml to html
            html_code = any_tree_to_html(anytree_root, 0, None)
            print("[thought]: \033[34m" + thought + "\033[0m")
            # is there api could use??  # 先检查api的调用，再做ui操作。
            # api_prompt = select_api_prompt.format(select_api_example=select_api_example, api_list=api_list, task=task,
            #                                       memory=get_memory(history_actions),
            #                                       planning=plan, thought=thought, ui_information=html_code)
            # api_res = get_model_response(args, api_prompt)
            # print("[API]: \033[34m" + api_res + "\033[0m")
            # if 'ERROR' in api_res:
            #     time.sleep(8)
            #     api_use = False
            #     continue
            # elif 'sorry' not in api_res.lower():
            #     if re.search(r'\[(.*)\]', api_res):
            #         result = api(api_res, history_actions)
            #         if result:
            #             api_use = True
            #         else:
            #             api_use = False
            #     else:
            #         print("[Wrong API command format]")
            #         api_use = False
            # else:
            #     print("[No API Use]")
            #     api_use = False
            # multi action making to finish a task.
            # if not api_use:
            # print("[HTML UI]：", html_code)
            # previous_history_actions = history_actions
            # # gpt4/3.5 API call
            # actions_prompt = actions_making_prompt.format(actions_making_example=actions_making_example,
            #                                               task_description=task,
            #                                               ui_information=html_code,
            #                                               memory=get_memory(history_actions),
            #                                               planning=plan, thought=thought)
            # print("[Prompt]: ", prompt)
            # action_res = chatgpt(actions_prompt)[0]
            # 保存动作前的页面信息

            # finish\adb\ui actions decision making
            type_prompt = action_type_prompt.format(action_type_example=action_type_example, task_description=task,
                                                           adb_api=api_list, action_history=get_memory(history_actions),
                                                           thought=thought, planning=plan)
            action_type = get_model_response(args, type_prompt)
            # action_type = input("[Has the task been completed? If it is not completed, what type of action do we need to do?]: ")
            print("[Action Type]: \033[34m" + action_type + "\033[0m")
            action_res = None
            if "task is finished" in action_type.lower():
                task_continue = False
                break
            elif "adb" in action_type.lower() and "not finished" in action_type.lower():
                api_prompt = select_api_prompt.format(select_api_example=select_api_example, api_list=api_list, task=task,
                                                      memory=get_memory(history_actions),
                                                      planning=plan, thought=thought, ui_information=html_code)
                action_res = get_model_response(args, api_prompt)
                print("[API Action]: \033[34m" + action_res + "\033[0m")
                # print("[API List]: ", api_list)
                # action_res = input("[Which ADB command do we need?]: ")
                result = api(action_res, history_actions)
                if result:
                    api_use = True
                else:
                    api_use = False
            elif "ui action" in action_type.lower():
                mapping = map_and_reverse_complete_interactive_elements(html_code)
                print(mapping)
                action_space = display_html_and_mapping(html_code, mapping)
                actions_prompt = actions_making_prompt.format(actions_making_example=actions_making_example,
                                                              task_description=task,
                                                              action=action_space,
                                                              memory=get_memory(history_actions),
                                                              planning=plan, thought=thought)
                action_res = get_model_response(args, actions_prompt)
                print("[UI Action]: \033[34m" + action_res + "\033[0m")
                # # USER input
                # action_res = input("[Which UI action do we need to do? click/scroll/input]: ")
                window_size = driver.get_window_size()
                action_res = process_user_input(window_size, action_res, mapping)
                print("[Actual Action]: \033[34m" + action_res + "\033[0m")
                actions(action_res, history_actions, driver)
            else:
                print("[no usful action in this round!]")
                continue
            # if the request reach the limit;
            time.sleep(1)

            xml_source, driver = get_page_source(driver)
            anytree_root = parse_xml_to_anytree(xml_source)
            # translate xml to html
            new_html_code = any_tree_to_html(anytree_root, 0, None)
            print("New HTML code:", new_html_code)
            # planning 放在最后面的原因是我们希望thought代表的是对当前动作的反思和对未来动作的思考。
            print("[Action History]: ", get_memory(history_actions))
            thought_prompt = Thought_prompt.format(thought_example=Thought_example, task_description=task,
                                                    planning=plan, action=action_res,
                                                    ui_information=html_code,
                                                    action_history=get_memory(history_actions),
                                                    now_ui_information=new_html_code,
                                                    api_list=usr_api_list)

            round_result = {
                "round_number": round_number,
                "old_html": html_code,
                "new_html": new_html_code,
                "action": action_res
            }
            with open(logfilename, 'a', encoding='utf-8') as f:
                # Use json.dump() with indent=4 to write with indentation
                json.dump(round_result, f, indent=4)
                f.write('\n')  # Add a newline to separate each result
            # # save the screenshot
            # screenshot_path = f"C:/Users/mi/PycharmProjects/Agent_base_appium/result/screenshot/screenshot_{systemPort}_{round_number}.png"
            # adb_command = f"adb exec-out screencap -p > {screenshot_path}"
            # result = subprocess.run(adb_command, shell=True)
            # if result.returncode == 0:
            #     print("截图成功！")
            # else:
            #     print("截图失败。")
            #     print("错误信息:", result.stderr)
            thought_res = get_model_response(args, thought_prompt)
            # thought_res = input("what is your thought?")
            # thought_res = "This is a test."
            # print("Thought Prompt:", thought_prompt)
            print("[thought]: \033[34m" + thought_res + "\033[0m")
            thought = thought_res  # 更新对下一步动作的思考。
            # history_actions.append({"thought": f"{res}"})



        # Task_description_example
        total_steps += round_number
        if task_continue:
            result = "Task failed"
        else:
            result = "Task finished successfully"
            pass_cnt += 1
        successful_actions_action = [action['Action'] for action in history_actions if
                                     action.get('Action', '') and 'Fail' not in action['Action']]
        successful_actions_api_call = [action['API call'] for action in history_actions if
                                       action.get('API call', '') and 'failed' not in action['API call']]
        successful_actions = successful_actions_action + successful_actions_api_call

        # check point
        check_result_1 += calculate_package_coverage(data_item, successful_actions)
        check_result_2 += check_points(data_item, successful_actions)

        result = {
            "id": data_item["id"],
            "app": data_item["app"],
            'query': data_item["query"],
            'action history': ' '.join(successful_actions),
            'check_point': data_item["check_point"],
            "result": result,
            "passrate": pass_cnt / cnt,
            "steps": round_number,
            "average steps": total_steps / cnt,
            "level1_check_result": check_result_1 / cnt,
            "level2_check_result": check_result_2 / cnt,
        }
        print("[passrate]: ", pass_cnt / cnt)
        print("[level1_check_result]: ", check_result_1 / cnt)
        print("[level2_check_result]: ", check_result_2 / cnt)

        with open(logfilename, 'a', encoding='utf-8') as f:
            # Use json.dump() with indent=4 to write with indentation
            json.dump(result, f, indent=4)
            f.write('\n')  # Add a newline to separate each result

    # task finished
    driver.quit()


def signal_handler(sig, frame):
    driver.quit()
    print("driver cleaned")
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()
