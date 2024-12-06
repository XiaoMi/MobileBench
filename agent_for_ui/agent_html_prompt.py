# Copyright (C) 2024 Xiaomi Corporation.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# maybe we can use the guidance format
# DengSHIHAN write this prompt for test.
actions_making_prompt = '''
You are a large language model agent stored on a mobile phone, You need to give the current one-step action that needs to be taken to complete the task.
Below I will provide you with a task, a plan, the actionspace of the current page, action history, thought about the next action.
You need to select the most suitable one element and give the corresponding one action based on the actionspace and thought.
Your selection should also consider action history, and have the courage to try new buttons instead of the same buttons from history. 
You just need to give the object number. There are four directions for scrolling, and you need to choose one of them.
Action can only be the following three functions: 
    1.click(number) 
    2.input(number, text) 
    3.scroll(number,up)|scroll(number,down)|scroll(number,left)|scroll(number,right) 
------Below is examples：
{actions_making_example} 
------examples ended

REMEMBER: 
1.Click and input have higher priority than scrolling. Scrolling is only considered when all elements of the current interface are indeed irrelevant to the task.
2.When you fail to try repeatedly in one interface, maybe you can try to turn back to select other options.
3.When you need to switch apps, you need to return to the HOME page first.
4.When you find that the current page does not have the APP you want, you need to scroll left and right to find more APPs.

Let's Begin!
[Task description]: {task_description}
[Planning]: {planning}
[Action Space]: {action}
[Actions history]: {memory}
[Thought]: {thought}
[Answer]: The only action that should be taken below is: 
'''


actions_making_example = '''
Example 1:
[Task description]: Calculate 9.5×5+2
[Planning]: Open a computing-related application and click the buttons one by one.
[Action Space]: 
[Clickables]:
 1: 小窗
 2: 计算
 3: 换算
 6: 清除
 7: 7
 8: 4
 9: 1
10: 切换
11: 退格
12: 8
13: 5
14: 2
15: 0
16: 百分号
17: 9
18: 6
19: 3
20: 小数点
21: 除
22: 乘
23: 减
24: 加
25: 等于
[Scrollables]:
4: Empty androidx.viewpager.widget.OriginalViewPager ([0,231][1080,2280])
[Inputs]:
5: 0
[Actions history]: 
adb shell am start -n com.cleveni.app.calculator/com.cleveni.app.calculator.MainActivity
click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>)
click(<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" description="小数点" clickable="true"> . </p>)
click(<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>)
click(<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" description="乘" clickable="true">  </img>)
[Thought]: Calculate 9.5×5+2, I have clicked on 9.5 and the multiplication sign, now I should click on 5.
[Answer]: click(13)

Example 2:
[Task description]: Write a note for me, title: Sunday, content: Complete the work and finish the file
[Planning]: Open the calendar, create a new event, fill in the title: Sunday, fill in the content: Complete the work and finish the file.
[Action Space]
[Clickables]:
 3: 7月4日 上午11:55
 4: 0字
 5: 开始书写或
 6: mind_map
 7: 创建思维笔记
 8: Empty android.widget.TextView
 9: 录音
10: 添加图片
11: 涂鸦
12: 任务列表
13: 展开富文本编辑
14: 返回
15: 撤销
16: 恢复
17: 完成编辑
[Scrollables]:
1: 小米笔记 ([0,231][1080,1232])
[Inputs]:
2: 标题
[Thought]: I clicked on voice input, but my device doesn't support this feature, so I need to use another input method, such as manual ways to input sunday.
[Answer]: input(2,Sunday)

Example 3:
[Task description]: Help me set an Write a memorandum for me on November 23, title: work, content: Complete the work and finish the file.
[Planning]: Open the calendar, create a new event, fill in the title: work, fill in the content: Complete the work and finish the file.
[Action Space]:
[Clickables]:
 2: 11:51
 3: 7月4日
 4: 周四
 5: 点击获取数据
 6: 天气
 7: 小米商城
 8: 小米商城
 9: 小米视频
10: 小米视频
11: 游戏中心
12: 游戏中心
13: 应用商店
14: 应用商店
15: 设置
16: 设置
17: 相册
18: 相册
19: 手机管家
20: 手机管家
21: 笔记
22: 笔记
24: 智能助理
25: 第1屏
26: 第2屏
28: 电话
29: 短信
30: 浏览器
31: 相机
[Scrollables]:
 1: Empty com.miui.home.launcher.ScreenView ([0,0][1080,2280])
23: Empty com.miui.home.launcher.ScreenView ([0,1909][1080,1962])
27: Empty com.miui.home.launcher.ScreenView ([11,1972][1069,2155])
[Actions history]: None
[Thought]: I need to find and open the calendar first.
[Answer]: scroll(1,left)
'''

'''
Example 3:
[Task description]: Help me set an alarm clock for five o'clock.
[Planning]: Turn on the clock, set an alarm, and adjust the time to five o'clock.
[UI information]: 
<button id="android:id/button1" class="android.widget.Button" description="取消" clickable="true">  </button>
<p id="android:id/title" class="android.widget.TextView" clickable="false"> 添加闹钟 </p>
<p id="com.android.deskclock:id/alarm_in_future" class="android.widget.TextView" clickable="false"> 23小时56分钟后响铃 </p>
<button id="android:id/button2" class="android.widget.Button" description="确定" clickable="true">  </button>
<div id="com.android.deskclock:id/amPm" class="com.android.deskclock.widget.NumberPicker" descript  ion="下午" clickable="true" scrollable="true" bounds="[31,319][369,1036]"> 1.0 </div>
<div id="com.android.deskclock:id/hour" class="com.android.deskclock.widget.NumberPicker" descript  ion="12时" clickable="true" scrollable="true" bounds="[370,319][709,1036]"> 12.0 </div>
<div id="com.android.deskclock:id/minute" class="com.android.deskclock.widget.NumberPicker" descript  ion="11分" clickable="true" scrollable="true" bounds="[710,319][1049,1036]"> 11.0 </div>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 铃声 </p>
<p id="com.android.deskclock:id/summary" class="android.widget.TextView" clickable="true"> 元素动态铃声 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 重复 </p>
<p id="com.android.deskclock:id/summary" class="android.widget.TextView" clickable="true"> 只响一次 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 响铃时振动 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 响铃后删除此闹钟 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 备注 </p>
<p id="com.android.deskclock:id/summary" class="android.widget.TextView" clickable="true"> 请输入 </p>
[Actions history]: 
click(<img id="com.miui.home:id/icon_icon" class="android.widget.ImageView" description="时钟" clickable="true">  </img>)
click(<img id="com.android.deskclock:id/end_btn2" class="android.widget.ImageButton" description="添加闹钟" clickable="true">  </img>)
click(<div id="com.android.deskclock:id/hour" class="com.android.deskclock.widget.NumberPicker" description="11时" clickable="true" scrollable="true" bounds="[370,319][709,1036]"> 11.0 </div>)
[Thought]: What I need is 5, the current page is 11, so I need to slide the page until it is 5
[Answer]: scroll([359,558][359,797])

Example：
Task description: Calculate 9×5+2
UI information: 
<img class="android.widget.ImageView" description="小窗" clickable="true" scrollable="false" bounds="[55,143][165,253]">  </img>
<p class="android.widget.TextView" clickable="true" scrollable="false" bounds="[398,158][508,238]"> 计算 </p>
<p class="android.widget.TextView" clickable="true" scrollable="false" bounds="[572,158][682,238]"> 换算 </p>
<img id="com.miui.calculator:id/more" class="android.widget.ImageView" description="更多选项" clickable="true" scrollable="false" bounds="[926,143][1036,253]">  </img>
<div id="com.miui.calculator:id/expression" class="android.view.View" description="0" clickable="true" scrollable="false" bounds="[58,887][1022,1083]">  </div>
<img id="com.miui.calculator:id/btn_c_s" class="android.widget.ImageView" description="清除" clickable="true" scrollable="false" bounds="[76,1149][275,1347]">  </img>
<p id="com.miui.calculator:id/digit_7" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[76,1391][275,1589]"> 7 </p>
<p id="com.miui.calculator:id/digit_4" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[76,1633][275,1832]"> 4 </p>
<p id="com.miui.calculator:id/digit_1" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[76,1876][275,2075]"> 1 </p>
<img id="com.miui.calculator:id/btn_switch" class="android.widget.ImageView" description="切换" clickable="true" scrollable="false" bounds="[76,2119][275,2318]">  </img>
<img id="com.miui.calculator:id/btn_del_s" class="android.widget.ImageView" description="退格" clickable="true" scrollable="false" bounds="[319,1149][518,1347]">  </img>
<p id="com.miui.calculator:id/digit_8" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[319,1391][518,1589]"> 8 </p>
<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[319,1633][518,1832]"> 5 </p>
<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[319,1876][518,2075]"> 2 </p>
<p id="com.miui.calculator:id/digit_0" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[319,2119][518,2318]"> 0 </p>
<img id="com.miui.calculator:id/op_pct" class="android.widget.ImageView" description="百分号" clickable="true" scrollable="false" bounds="[562,1149][761,1347]">  </img>
<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[562,1391][761,1589]"> 9 </p>
<p id="com.miui.calculator:id/digit_6" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[562,1633][761,1832]"> 6 </p>
<p id="com.miui.calculator:id/digit_3" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[562,1876][761,2075]"> 3 </p>
<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" description="小数点" clickable="true" scrollable="false" bounds="[562,2119][761,2318]"> . </p>
<img id="com.miui.calculator:id/op_div" class="android.widget.ImageView" description="除" clickable="true" scrollable="false" bounds="[805,1149][1004,1347]">  </img>
<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" description="乘" clickable="true" scrollable="false" bounds="[805,1391][1004,1589]">  </img>
<img id="com.miui.calculator:id/op_sub" class="android.widget.ImageView" description="减" clickable="true" scrollable="false" bounds="[805,1633][1004,1832]">  </img>
<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" description="加" clickable="true" scrollable="false" bounds="[805,1876][1004,2075]">  </img>
<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" description="等于" clickable="true" scrollable="false" bounds="[805,2119][1004,2318]">  </img>

Actions history: none
Answer: click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true" scrollable="false" bounds="[562,1391][761,1589]"> 9 </p>)

Example 3:
Task description: Calculate 9×5+2
UI information: 
<img class="android.widget.ImageView" alt="小窗" clickable="true">  </img>
<p class="android.widget.TextView" clickable="true"> 计算,  </p>
<p class="android.widget.TextView" clickable="true"> 换算,  </p>
<img id="com.miui.calculator:id/more" class="android.widget.ImageView" alt="更多选项" clickable="true">  </img>
<div id="com.miui.calculator:id/expression" class="android.view.View" alt="9.5×5" clickable="true">  </div>
<p id="com.miui.calculator:id/result" class="android.widget.TextView" alt="= 47.5" clickable="true"> = 47.5,  </p>
<img id="com.miui.calculator:id/btn_c_s" class="android.widget.ImageView" alt="清除" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_7" class="android.widget.TextView" clickable="true"> 7,  </p>
<p id="com.miui.calculator:id/digit_4" class="android.widget.TextView" clickable="true"> 4,  </p>
<p id="com.miui.calculator:id/digit_1" class="android.widget.TextView" clickable="true"> 1,  </p>
<img id="com.miui.calculator:id/btn_switch" class="android.widget.ImageView" alt="切换" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_del_s" class="android.widget.ImageView" alt="退格" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_8" class="android.widget.TextView" clickable="true"> 8,  </p>
<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>
<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true"> 2,  </p>
<p id="com.miui.calculator:id/digit_0" class="android.widget.TextView" clickable="true"> 0,  </p>
<img id="com.miui.calculator:id/op_pct" class="android.widget.ImageView" alt="百分号" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>
<p id="com.miui.calculator:id/digit_6" class="android.widget.TextView" clickable="true"> 6,  </p>
<p id="com.miui.calculator:id/digit_3" class="android.widget.TextView" clickable="true"> 3,  </p>
<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" alt="小数点" clickable="true"> .,  </p>
<img id="com.miui.calculator:id/op_div" class="android.widget.ImageView" alt="除" clickable="true">  </img>
<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>
<img id="com.miui.calculator:id/op_sub" class="android.widget.ImageView" alt="减" clickable="true">  </img>
<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" alt="加" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" alt="等于" clickable="true">  </img>
Actions history: 
Action: click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>)
Action: click(<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>)
Answer: click(<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>)
'''
'''
Example 4:
Task description: Write a note for me, title: Sunday, content: Complete the work and finish the file
UI information:
<div class="android.widget.FrameLayout" clickable="false">  </div>
<img id="com.miui.notes:id/home" class="android.widget.ImageView" alt="返回" clickable="true">  </img>
<div class="android.view.View" clickable="false">  </div>
<img id="com.miui.notes:id/undo" class="android.widget.ImageView" alt="撤销" clickable="true">  </img>
<img id="com.miui.notes:id/redo" class="android.widget.ImageView" alt="恢复" clickable="true">  </img>
<img id="com.miui.notes:id/done" class="android.widget.ImageView" alt="完成编辑" clickable="true">  </img>
<input class="android.widget.EditText" clickable="true"> Sunday </input>
<p class="android.widget.TextView" clickable="true"> 11月10日 上午9:35 </p>
<p class="android.widget.TextView" clickable="true"> 0字 </p>
<p class="android.widget.TextView" clickable="true"> 开始书写或 </p>
<img class="android.widget.Image" clickable="true"> mind_map </img>
<p class="android.widget.TextView" clickable="true"> 创建思维笔记 </p>
<p class="android.widget.TextView" clickable="true">  </p>
<div id="com.miui.notes:id/mix_view" class="android.view.View" clickable="true">  </div>
<img id="com.miui.notes:id/audio" class="android.widget.ImageView" alt="录音" clickable="true">  </img>
<img id="com.miui.notes:id/gallery" class="android.widget.ImageView" alt="添加图片" clickable="true">  </img>
<img id="com.miui.notes:id/edit_image" class="android.widget.ImageView" alt="涂鸦" clickable="true">  </img>
<img id="com.miui.notes:id/check" class="android.widget.ImageView" alt="任务列表" clickable="true">  </img>
<img id="com.miui.notes:id/rich_text_switch" class="android.widget.ImageView" alt="展开富文本编辑" clickable="true">  </img>
<div id="com.miui.notes:id/panel_divide" class="android.view.View" clickable="true">  </div>
<div id="com.miui.notes:id/navi_placeholder" class="android.view.View" clickable="true">  </div>
Actions history: 
Action: {'click(<img id="com.miui.notes:id/content_add" class="android.widget.ImageView" alt="点击创建文字，长按录入语音，松手完成录音并创建，手指上滑取消录音" clickable="true">  </img>)'}
Action: {'action': 'input(<input class="android.widget.EditText" clickable="true"> 标题 </input>, Sunday)'}
Answer: input(<p class="android.widget.TextView" clickable="true"> 开始书写或 </p>, Complete the work and finish the file)
'''

html_ui_understanding = '''
You are a large language model agent stored on a mobile phone, below I will provide you with an environment of the current mobile phone interface.
Please tell me the information contained in this html interface. 
'''
html_ui_examples = '''
You are a large language model agent stored on a mobile phone, below I will provide you with an environment of the current mobile phone interface.
<img id=17 class="com.miui.calculator:id/btn_c_s" alt="清除" clickable="true">  </img>
<button id=17 class="com.miui.calculator:id/digit_7" clickable="true"> 7 </button>
<button id=17 class="com.miui.calculator:id/digit_4" clickable="true"> 4 </button>
Please tell me the information contained in this html interface. 
Answer: There is a picture that says "Clear" and two buttons representing 4 and 7.
'''

# -------------------------------------------------------------------------------------------------------
app_selection_prompt = '''
You are a large language model agent stored on a mobile phone, below I will provide you with a task, the environment of the current mobile phone interface(Apps information).
Please help me choose the correct app to perform the task based on the Apps information. 
On this basis, you should make a simple plan for completing the task.
[Apps information]: 
{apps_information}

----Below are some examples：
{app_selection_example}
----examples ended

[Task description]: {task_description}
[Answer]:
'''
app_selection_example = '''
Example 1:
[Task description]: Read the latest message.
[Answer]: I should open Messages before I can view recent text messages, then using this one application should be enough.

Example 2:
[Task description]: Calculate 7*2.2/4+1
[Answer]: I should open ClevCalc because this is an application directly related to the calculator and since the task only involves calculations, then using this one application should be enough.

Example 3:
[Task description]: I want to go to Wuhan next week. Please help me determine the specific travel time and method. The information you collect can be saved on my phone for easy review by me.
[Answer]: To determine the time and mode of travel, I should at least check the air tickets or train tickets and hotel conditions on Traveloka, and check the weather conditions for the next few days on Weather. Because the collected information needs to be stored on the mobile phone, I will take screenshots of the necessary air and train ticket information and write the most recommended solution in a memo.
'''

# Base passrate
# -------------------------------------------------------------------------------------------------------
Task_finish_prompt = '''
You are a large language model agent stored on a mobile phone, below I will provide you with a task, 
the environment of the current mobile phone interface(UI information), historical action information, thoughts on the current situation.
You need to judge whether the current task has been completed based on the current environment and action history.
If the "Thought" answer indicates that there are no further actions to finish, this means the task is completed.

----Below are the examples：
{task_finish_example}
----examples ended

[Task description]: {task_description}
[UI information]: {ui_information}
[Actions history]: {memory}
[Thought]:{thought}
[Question]: Is the task completed?
[Answer]:
'''
Task_finish_example = '''
Example 1:
[Task description]: Calculate 9×5+2
[UI information]: 
<img class="android.widget.ImageView" alt="小窗" clickable="true">  </img>
<p class="android.widget.TextView" clickable="true"> 计算,  </p>
<p class="android.widget.TextView" clickable="true"> 换算,  </p>
<img id="com.miui.calculator:id/more" class="android.widget.ImageView" alt="更多选项" clickable="true">  </img>
<div id="com.miui.calculator:id/expression" class="android.view.View" alt="9×5+2" clickable="true">  </div>
<p id="com.miui.calculator:id/result" class="android.widget.TextView" alt="= 47" clickable="true"> = 47,  </p>
<img id="com.miui.calculator:id/btn_c_s" class="android.widget.ImageView" alt="清除" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_7" class="android.widget.TextView" clickable="true"> 7,  </p>
<p id="com.miui.calculator:id/digit_4" class="android.widget.TextView" clickable="true"> 4,  </p>
<p id="com.miui.calculator:id/digit_1" class="android.widget.TextView" clickable="true"> 1,  </p>
<img id="com.miui.calculator:id/btn_switch" class="android.widget.ImageView" alt="切换" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_del_s" class="android.widget.ImageView" alt="退格" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_8" class="android.widget.TextView" clickable="true"> 8,  </p>
<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>
<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true"> 2,  </p>
<p id="com.miui.calculator:id/digit_0" class="android.widget.TextView" clickable="true"> 0,  </p>
<img id="com.miui.calculator:id/op_pct" class="android.widget.ImageView" alt="百分号" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>
<p id="com.miui.calculator:id/digit_6" class="android.widget.TextView" clickable="true"> 6,  </p>
<p id="com.miui.calculator:id/digit_3" class="android.widget.TextView" clickable="true"> 3,  </p>
<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" alt="小数点" clickable="true"> .,  </p>
<img id="com.miui.calculator:id/op_div" class="android.widget.ImageView" alt="除" clickable="true">  </img>
<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>
<img id="com.miui.calculator:id/op_sub" class="android.widget.ImageView" alt="减" clickable="true">  </img>
<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" alt="加" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" alt="等于" clickable="true">  </img>
[Actions history]: 
Action: click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>)
Action: click(<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>)
Action: click(<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>)
Action: click(<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" alt="加" clickable="true">  </img>)
Action: click(<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true"> 2,  </p>)
Action: click(<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" alt="等于" clickable="true">  </img>)
[Thought]: I have already calculate 9×5+2 = 47, there is no need for any further action.
[Question]: Is the task completed?
[Answer]: Yes, the task is completed.

Example 2:
[Task description]: Calculate 9×5+2
[UI information]: 
<img class="android.widget.ImageView" alt="小窗" clickable="true">  </img>
<p class="android.widget.TextView" clickable="true"> 计算,  </p>
<p class="android.widget.TextView" clickable="true"> 换算,  </p>
<img id="com.miui.calculator:id/more" class="android.widget.ImageView" alt="更多选项" clickable="true">  </img>
<div id="com.miui.calculator:id/expression" class="android.view.View" alt="9×5" clickable="true">  </div>
<p id="com.miui.calculator:id/result" class="android.widget.TextView" alt="= 45" clickable="true"> = 47,  </p>
<img id="com.miui.calculator:id/btn_c_s" class="android.widget.ImageView" alt="清除" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_7" class="android.widget.TextView" clickable="true"> 7,  </p>
<p id="com.miui.calculator:id/digit_4" class="android.widget.TextView" clickable="true"> 4,  </p>
<p id="com.miui.calculator:id/digit_1" class="android.widget.TextView" clickable="true"> 1,  </p>
<img id="com.miui.calculator:id/btn_switch" class="android.widget.ImageView" alt="切换" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_del_s" class="android.widget.ImageView" alt="退格" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_8" class="android.widget.TextView" clickable="true"> 8,  </p>
<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>
<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true"> 2,  </p>
<p id="com.miui.calculator:id/digit_0" class="android.widget.TextView" clickable="true"> 0,  </p>
<img id="com.miui.calculator:id/op_pct" class="android.widget.ImageView" alt="百分号" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>
<p id="com.miui.calculator:id/digit_6" class="android.widget.TextView" clickable="true"> 6,  </p>
<p id="com.miui.calculator:id/digit_3" class="android.widget.TextView" clickable="true"> 3,  </p>
<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" alt="小数点" clickable="true"> .,  </p>
<img id="com.miui.calculator:id/op_div" class="android.widget.ImageView" alt="除" clickable="true">  </img>
<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>
<img id="com.miui.calculator:id/op_sub" class="android.widget.ImageView" alt="减" clickable="true">  </img>
<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" alt="加" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" alt="等于" clickable="true">  </img>
[Actions history]: 
Action: click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>)
Action: click(<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>)
Action: click(<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>)
[Thought]: I have already calculate 9×5, next I will click +.
[Question]: Is the task completed?
Answer: No, the task is not completed.
'''

# -------------------------------------------------------------------------------------------------------
Thought_prompt = '''
You are a large language model agent stored on a mobile phone, below I will provide you with a task, a plan,
the environment of the current mobile phone interface before action (Previous UI information), action history, the environment of the current mobile phone interface(Now UI information).
Action history records completed operations, including click, input, scroll and api_call.
You need to summarize these four aspects: changes in the UI page, task progress, actions that have been completed, one next action based on UI information and action history.
[Action History] are all previous historical actions, and [current action] is the current action that causes the UI page to change.
[task progress] Where in the plan is the current page?
[One next action] You need to choose one among click, input, scroll and one api as the next action, and give one and only one operation object.
[One next action] Strictly refer to [current action] and [action history] result to do the next action. 
Additional information: If you want to play history records in Ximalaya, you need to open Ximalaya, click "My", view the playback records under the "My" page, and select the most recent one to play.
------Below are examples：
{thought_example}
------examples ended

Let's Begin!
[Task description]: {task_description}
[Planning]: {planning}
[Previous UI information]: {ui_information}
[Now UI information]: {now_ui_information}
[Action History]: {action_history}
[Current Action]:{action}
[Answer]: 
'''
Thought_example = '''
Example 1:
[Task description]: I'm going to travel from chengdu to Beijing next week. Please help me determine the flight and specific time.
[Planning]: Open the travel APP, check flight from chengdu to beijing, sort by price, take a screenshot, then open Google search, search and check the weather conditions in Beijing next week.

[Previous UI information]: <button id="com.traveloka.android:id/toolbar_left" class="android.widget.ImageButton" clickable="true">  </button>
<p id="com.traveloka.android:id/text_view_toolbar_title" class="android.widget.TextView" clickable="false"> Flights </p>
<button id="com.traveloka.android:id/toolbar_right" class="android.widget.ImageButton" clickable="true">  </button>
<div id="com.traveloka.android.flight:id/layout_scroll" class="android.widget.ScrollView" clickable="false" scrollable="true" bounds="[0,210][1080,1717]">  </div>
<p id="com.traveloka.android.flight:id/text_owrt" class="android.widget.TextView" clickable="true"> One-way / Round-trip </p>
<p id="com.traveloka.android.flight:id/text_mc" class="android.widget.TextView" clickable="true"> Multi-city </p>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> From </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Chengdu (CTUA) </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> To </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Beijing (BEIA) </input>
<button id="com.traveloka.android.flight:id/btn_swap" class="android.widget.ImageButton" description="flight_searchform_button_swap" clickable="true">  </button>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Departure Date </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Wednesday, 29 Nov 2023 </input>
<p id="com.traveloka.android.flight:id/text_rt" class="android.widget.TextView" clickable="false"> Round-trip? </p>
<div id="com.traveloka.android.flight:id/switch_rt" class="android.widget.Switch" description="flight_searchform_button_roundtrip" clickable="true">  </div>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Return Date </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Saturday, 2 Dec 2023 </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Passengers </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> 1 passenger </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Seat Class </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Economy </input>
<button id="com.traveloka.android.flight:id/btn_search" class="android.widget.Button" description="flight_searchform_button_search" clickable="true"> Search </button>
<p id="com.traveloka.android.flight:id/flight_searchform_textview_recent_search" class="android.widget.TextView" clickable="false"> Your Recent Searches </p>
<div id="com.traveloka.android.flight:id/flight_searchform_recyclerview_recent_search" class="androidx.recyclerview.widget.RecyclerView" clickable="false" scrollable="true" bounds="[0,1711][1080,1717]">  </div>
<p id="com.traveloka.android.flight:id/textview_search" class="android.widget.TextView" clickable="true"> Search </p>
<p id="com.traveloka.android.flight:id/textview_discover" class="android.widget.TextView" clickable="true"> Discover </p>

[Now UI information]: <button id="com.traveloka.android.flight:id/image_arrow_back" class="android.widget.ImageButton" clickable="true">  </button>
<p id="com.traveloka.android.flight:id/text_title" class="android.widget.TextView" clickable="true"> Chengdu (CTUA)   Beijing (BEIA) </p>
<p id="com.traveloka.android.flight:id/text_subtitle" class="android.widget.TextView" clickable="true"> Wed, 29 Nov • 1 pax • Economy </p>
<div id="com.traveloka.android.flight:id/recycler_date" class="androidx.recyclerview.widget.RecyclerView" clickable="true" scrollable="true" bounds="[0,215][954,387]">  </div>
<p id="com.traveloka.android.flight:id/text_date" class="android.widget.TextView" clickable="true"> Mon, 27 Nov </p>
<p id="com.traveloka.android.flight:id/text_price" class="android.widget.TextView" clickable="true"> See Price </p>
<p id="com.traveloka.android.flight:id/text_date" class="android.widget.TextView" clickable="true"> Tue, 28 Nov </p>
<p id="com.traveloka.android.flight:id/text_price" class="android.widget.TextView" clickable="true"> See Price </p>
<p id="com.traveloka.android.flight:id/text_date" class="android.widget.TextView" clickable="true"> Wed, 29 Nov </p>
<p id="com.traveloka.android.flight:id/text_price" class="android.widget.TextView" clickable="true"> USD  81.49 </p>
<p id="com.traveloka.android.flight:id/text_date" class="android.widget.TextView" clickable="true"> Thu, 30 Nov </p>
<p id="com.traveloka.android.flight:id/text_price" class="android.widget.TextView" clickable="true"> See Price </p>
<p id="com.traveloka.android.flight:id/text_date" class="android.widget.TextView" clickable="true"> Fri, 1 Dec </p>
<p id="com.traveloka.android.flight:id/text_price" class="android.widget.TextView" clickable="true"> See Price </p>
<div id="com.traveloka.android.flight:id/recycler" class="androidx.recyclerview.widget.RecyclerView" clickable="false" scrollable="true" bounds="[0,387][1080,1857]">  </div>
<p id="com.traveloka.android.flight:id/quick_filter_item_name" class="android.widget.TextView" clickable="true"> Smart Combo </p>
<p id="com.traveloka.android.flight:id/text_flight_name" class="android.widget.TextView" description="text_view_flight_name " clickable="true"> China Eastern Airlines </p>
<p id="com.traveloka.android.flight:id/text_departure_time" class="android.widget.TextView" clickable="true"> 20:30 </p>
<p id="com.traveloka.android.flight:id/text_flight_duration" class="android.widget.TextView" clickable="true"> 2h 45m </p>
<p id="com.traveloka.android.flight:id/text_reduced_price" class="android.widget.TextView" clickable="true"> USD 81.49 </p>
<p id="com.traveloka.android.flight:id/text_real_price" class="android.widget.TextView" clickable="true"> USD  84.05/pax </p>
<p id="com.traveloka.android.flight:id/text_arrival_time" class="android.widget.TextView" clickable="true"> 23:15 </p>
<p id="com.traveloka.android.flight:id/text_departure_airport_code" class="android.widget.TextView" clickable="true"> CTU </p>
<p id="com.traveloka.android.flight:id/text_number_of_transit" class="android.widget.TextView" clickable="true"> Direct </p>
<p id="com.traveloka.android.flight:id/text_reduced_price_per_pax" class="android.widget.TextView" clickable="true"> /pax </p>
<p id="com.traveloka.android.flight:id/text_arrival_airport_code" class="android.widget.TextView" clickable="true"> PKX </p>
<p id="com.traveloka.android:id/promo_name" class="android.widget.TextView" clickable="true"> Smart Combo </p>
<p id="com.traveloka.android.flight:id/text_flight_name" class="android.widget.TextView" description="text_view_flight_name " clickable="true"> China Eastern Airlines </p>
<p id="com.traveloka.android.flight:id/text_departure_time" class="android.widget.TextView" clickable="true"> 07:20 </p>
<p id="com.traveloka.android.flight:id/text_flight_duration" class="android.widget.TextView" clickable="true"> 2h 40m </p>
<p id="com.traveloka.android.flight:id/text_reduced_price" class="android.widget.TextView" clickable="true"> USD 102.53 </p>
<p id="com.traveloka.android.flight:id/text_real_price" class="android.widget.TextView" clickable="true"> USD  104.47/pax </p>
<p id="com.traveloka.android.flight:id/text_arrival_time" class="android.widget.TextView" clickable="true"> 10:00 </p>
<p id="com.traveloka.android.flight:id/text_departure_airport_code" class="android.widget.TextView" clickable="true"> CTU </p>
<p id="com.traveloka.android.flight:id/text_number_of_transit" class="android.widget.TextView" clickable="true"> Direct </p>
<p id="com.traveloka.android.flight:id/text_reduced_price_per_pax" class="android.widget.TextView" clickable="true"> /pax </p>
<p id="com.traveloka.android.flight:id/text_arrival_airport_code" class="android.widget.TextView" clickable="true"> PKX </p>
<p id="com.traveloka.android:id/promo_name" class="android.widget.TextView" clickable="true"> Smart Combo </p>
<p id="com.traveloka.android.flight:id/text_title" class="android.widget.TextView" clickable="true"> Be the first to know when prices drop! </p>
<p id="com.traveloka.android.flight:id/text_description" class="android.widget.TextView" clickable="true"> Create a price alert and we’ll let you know as soon as prices have dropped significantly. </p>
<p id="com.traveloka.android.flight:id/text_button_action" class="android.widget.TextView" clickable="true"> Create Price Alert </p>
<p id="com.traveloka.android.flight:id/text_flight_name" class="android.widget.TextView" description="text_view_flight_name " clickable="true"> China Eastern Airlines </p>
<p id="com.traveloka.android.flight:id/text_flight_duration" class="android.widget.TextView" clickable="true"> 2h 25m </p>
<p id="com.traveloka.android.flight:id/text_real_price" class="android.widget.TextView" clickable="true"> USD  118.11/pax </p>
<div id="com.traveloka.android.flight:id/container_pill" class="android.widget.HorizontalScrollView" clickable="true" scrollable="true" bounds="[0,1709][950,1857]">  </div>
<p id="com.traveloka.android.flight:id/pill_title" class="android.widget.TextView" clickable="true"> Stops </p>
<p id="com.traveloka.android.flight:id/pill_title" class="android.widget.TextView" clickable="true"> Airlines </p>
<p id="com.traveloka.android.flight:id/pill_title" class="android.widget.TextView" clickable="true"> Time </p>
<p id="com.traveloka.android.flight:id/pill_sort_title" class="android.widget.TextView" clickable="true"> Cheapest </p>
<p id="com.traveloka.android:id/button_text" class="android.widget.TextView" clickable="true"> Filter </p>

[Action History]: 
{'[Action]': 'click(<p class="android.widget.TextView" description="Traveloka" clickable="true"> Traveloka </p>)'}
{'[Action]': 'click(<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Flights </p>)'}
{'[Action]': 'click(<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Thursday, 23 Nov 2023 </input>)'}
{'[Action]': 'click(<div id="com.traveloka.android:id/calendar_date_text" class="android.view.View" description="19" clickable="true">  </div>)'}
{'[Action]': 'click(<div id="com.traveloka.android:id/calendar_date_text" class="android.view.View" description="26" clickable="true">  </div>)'}
{'[Action]': 'click(<button id="com.traveloka.android.flight:id/btn_search" class="android.widget.Button" description="flight_searchform_button_search" clickable="true"> Search </button>)'}

[Current Action]: {'[Action]': 'click(<button id="com.traveloka.android.flight:id/btn_search" class="android.widget.Button" description="flight_searchform_button_search" clickable="true"> Search </button>)'}

[Answer]: 
Changes: I clicked "Search" button. The page changes from the flight search page to the flight search results page. The page contains two flight information from Chengdu to Beijing.
Actions Complete: I have opened traveloka app, clicked "flight" button, filled the form and clicked the "search" button. 
Task progress: The current mission progress is check flight from chengdu to beijing.
One next action: Click on the cheapest flight to see more detailed information.

Example 2:
[Task description]: I'm going to travel from chengdu to Beijing next week. Please help me determine the flight and specific time.
[Planning]: Open the travel APP, check flight from chengdu to beijing, sort by price, take a screenshot, then open Google search, search and check the weather conditions in Beijing next week.

[Previous UI information]: 
<button id="com.traveloka.android:id/toolbar_left" class="android.widget.ImageButton" clickable="true">  </button>
<p id="com.traveloka.android:id/text_view_toolbar_title" class="android.widget.TextView" clickable="false"> Flights </p>
<button id="com.traveloka.android:id/toolbar_right" class="android.widget.ImageButton" clickable="true">  </button>
<div id="com.traveloka.android.flight:id/layout_scroll" class="android.widget.ScrollView" clickable="false" scrollable="true" bounds="[0,210][1080,1717]">  </div>
<p id="com.traveloka.android.flight:id/text_owrt" class="android.widget.TextView" clickable="true"> One-way / Round-trip </p>
<p id="com.traveloka.android.flight:id/text_mc" class="android.widget.TextView" clickable="true"> Multi-city </p>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> From </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Chengdu (CTUA) </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> To </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Beijing (BEIA) </input>
<button id="com.traveloka.android.flight:id/btn_swap" class="android.widget.ImageButton" description="flight_searchform_button_swap" clickable="true">  </button>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Departure Date </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Saturday, 2 Dec 2023 </input>
<p id="com.traveloka.android.flight:id/text_rt" class="android.widget.TextView" clickable="false"> Round-trip? </p>
<div id="com.traveloka.android.flight:id/switch_rt" class="android.widget.Switch" description="flight_searchform_button_roundtrip" clickable="true">  </div>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Return Date </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Saturday, 2 Dec 2023 </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Passengers </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> 1 passenger </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Seat Class </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Economy </input>
<button id="com.traveloka.android.flight:id/btn_search" class="android.widget.Button" description="flight_searchform_button_search" clickable="true"> Search </button>
<p id="com.traveloka.android.flight:id/flight_searchform_textview_recent_search" class="android.widget.TextView" clickable="false"> Your Recent Searches </p>
<div id="com.traveloka.android.flight:id/flight_searchform_recyclerview_recent_search" class="androidx.recyclerview.widget.RecyclerView" clickable="false" scrollable="true" bounds="[0,1711][1080,1717]">  </div>
<p id="com.traveloka.android.flight:id/textview_search" class="android.widget.TextView" clickable="true"> Search </p>
<p id="com.traveloka.android.flight:id/textview_discover" class="android.widget.TextView" clickable="true"> Discover </p>

[Now UI information]: 
<button id="com.traveloka.android:id/toolbar_left" class="android.widget.ImageButton" clickable="true">  </button>
<p id="com.traveloka.android:id/text_view_toolbar_title" class="android.widget.TextView" clickable="false"> Flights </p>
<button id="com.traveloka.android:id/toolbar_right" class="android.widget.ImageButton" clickable="true">  </button>
<div id="com.traveloka.android.flight:id/layout_scroll" class="android.widget.ScrollView" clickable="false" scrollable="true" bounds="[0,210][1080,1717]">  </div>
<p id="com.traveloka.android.flight:id/text_owrt" class="android.widget.TextView" clickable="true"> One-way / Round-trip </p>
<p id="com.traveloka.android.flight:id/text_mc" class="android.widget.TextView" clickable="true"> Multi-city </p>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> From </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Chengdu (CTUA) </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> To </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Beijing (BEIA) </input>
<button id="com.traveloka.android.flight:id/btn_swap" class="android.widget.ImageButton" description="flight_searchform_button_swap" clickable="true">  </button>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Departure Date </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Saturday, 2 Dec 2023 </input>
<p id="com.traveloka.android.flight:id/text_rt" class="android.widget.TextView" clickable="false"> Round-trip? </p>
<div id="com.traveloka.android.flight:id/switch_rt" class="android.widget.Switch" description="flight_searchform_button_roundtrip" clickable="true">  </div>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Return Date </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Saturday, 2 Dec 2023 </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Passengers </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> 1 passenger </input>
<p id="com.traveloka.android:id/label_text_view" class="android.widget.TextView" clickable="false"> Seat Class </p>
<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Economy </input>
<button id="com.traveloka.android.flight:id/btn_search" class="android.widget.Button" description="flight_searchform_button_search" clickable="true"> Search </button>
<p id="com.traveloka.android.flight:id/flight_searchform_textview_recent_search" class="android.widget.TextView" clickable="false"> Your Recent Searches </p>
<div id="com.traveloka.android.flight:id/flight_searchform_recyclerview_recent_search" class="androidx.recyclerview.widget.RecyclerView" clickable="false" scrollable="true" bounds="[0,1711][1080,1717]">  </div>
<p id="com.traveloka.android.flight:id/textview_search" class="android.widget.TextView" clickable="true"> Search </p>
<p id="com.traveloka.android.flight:id/textview_discover" class="android.widget.TextView" clickable="true"> Discover </p>

[Action History]: 
{'[Action]': 'click(<p class="android.widget.TextView" description="Traveloka" clickable="true"> Traveloka </p>)'}
{'[Action]': 'click(<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Flights </p>)'}
{'[Fail]: InvalidElementStateException action': 'input(<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Chengdu (CTUA) </input>, Chengdu (CTUA))'}

[Current action]:{'[Action]': 'input(<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Chengdu (CTUA) </input>, Chengdu (CTUA))'}

[Answer]: 
Changes: The current page is the flight search form page in the Traveloka app. And There is no change between two pages.
Task progress: From the current action and action history, I am currently on the flight search form page, ready to search for flights from Chengdu to Beijing.
Actions completed: From the current action and action history, I have opened the traveloka app and clicked the flight button to search for flights
One next action: Because the operation of inputting information in Chengdu (CTUA) failed, I will try other operations, such as clicking Chengdu (CTUA) first. The one next action I will do is click "Chengdu (CTUA)" button to select departure city.
'''

'''

Example 3:
Task description: Help me set an alarm clock for five o'clock.
Planning: Open the clock, create a new alarm clock, and set the time to five o'clock.
Previous UI information: 
<button id="android:id/button1" class="android.widget.Button" description="取消" clickable="true">  </button>
<p id="android:id/title" class="android.widget.TextView" clickable="false"> 添加闹钟 </p>
<p id="com.android.deskclock:id/alarm_in_future" class="android.widget.TextView" clickable="false"> 23小时56分钟后响铃 </p>
<button id="android:id/button2" class="android.widget.Button" description="确定" clickable="true">  </button>
<div id="com.android.deskclock:id/amPm" class="com.android.deskclock.widget.NumberPicker" descript  ion="下午" clickable="true" scrollable="true" bounds="[31,319][369,1036]"> 1.0 </div>
<div id="com.android.deskclock:id/hour" class="com.android.deskclock.widget.NumberPicker" descript  ion="12时" clickable="true" scrollable="true" bounds="[370,319][709,1036]"> 12.0 </div>
<div id="com.android.deskclock:id/minute" class="com.android.deskclock.widget.NumberPicker" descript  ion="11分" clickable="true" scrollable="true" bounds="[710,319][1049,1036]"> 11.0 </div>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 铃声 </p>
<p id="com.android.deskclock:id/summary" class="android.widget.TextView" clickable="true"> 元素动态铃声 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 重复 </p>
<p id="com.android.deskclock:id/summary" class="android.widget.TextView" clickable="true"> 只响一次 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 响铃时振动 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 响铃后删除此闹钟 </p>
<p id="com.android.deskclock:id/title" class="android.widget.TextView" clickable="true"> 备注 </p>
<p id="com.android.deskclock:id/summary" class="android.widget.TextView" clickable="true"> 请输入 </p>
[Action]: 
Action: click(<img id="com.miui.home:id/icon_icon" class="android.widget.ImageView" description="时钟" clickable="true">  </img>)
Action: click(<img id="com.android.deskclock:id/end_btn2" class="android.widget.ImageButton" description="添加闹钟" clickable="true">  </img>)
Action: click(<div id="com.android.deskclock:id/hour" class="com.android.deskclock.widget.NumberPicker" description="11时" clickable="true" scrollable="true" bounds="[370,319][709,1036]"> 11.0 </div>)
[Answer]: I need to set the hour to five. In the last step, I tried to click on the eleven hours, but it seems that the element can't be click, now I will try to scroll the element to set the hour to five.
'''

passrate_prompt = '''
You are a large language model agent stored on a mobile phone, below I will provide you with a task, a system logcat.
You need to judge whether the task is completed based on the system logcat.
Task: {task}
Logcat: {logcat}
Ans: 
'''

action_type_prompt = '''
You are a large language model agent stored on a mobile phone, below I will provide you with a task, a plan to accomplish the task, a next action thought, and actions finished history.
Your task is to determine whether the task is finished based on the action history, and if the task is not finished, you need to consider the next action type based on thought.
The main reference you need is thought. If it is clearly stated that click, enter, scroll, then you should not select adb as the next action category.
You have two action categories to choose from, adb or ui action.
    1. adb: If there is an ADB API that can accomplish the action specified in thought
    2. ui action: If you judge that you are already inside an app, you should select ui action to interact with the app.
Remember, your answer should including be one of the following three: "task is finished", "task is not ended, the next action type is adb" or "task is not finished, the next action type is ui action".

------Below are examples：
{action_type_example}
------examples ended

[Task description]: {task_description}
[Planning]: {planning}
[Thought]: {thought}
[ADB API]: {adb_api}
[Action History]: {action_history}
[Answer]: 
'''


action_type_example = '''
Example 1:
[Task description]: Help me set an alarm clock for five o'clock.
[Planning]: Open the clock, create a new alarm clock, and set the time to five o'clock.
[Thought]:
I need to set the hour to five. In the last step, I tried to click on the eleven hours, but it seems that the element can't be click, now I will try to scroll the element to set the hour to five.
[ADB API]: 
{
      "ADB Command": "adb shell am start -a android.intent.action.SET_ALARM --ei android.intent.extra.alarm.HOUR <x> --ei android.intent.extra.alarm.MINUTES <y>",
      "Function Description": "Triggers an intent to open the alarm clock application with a pre-filled time for setting a new alarm.",
      "Parameter Information": "Replace <x> with the hour and <y> with the minutes for the alarm time. For example, for an alarm set at 7:15, <x> would be 7 and <y> would be 15."
    },
    {
      "ADB Command": "adb shell am start -n com.android.deskclock/.DeskClockTabActivity\n",
      "Function Description": "启动时钟到主界面",
      "Parameter Information": "No additional parameters required."
    },
    {
      "ADB Command": "adb shell am start -a android.intent.action.EDIT -d deskclock://details/edit",
      "Function Description": "编辑世界时钟",
      "Parameter Information": "No additional parameters required."
    },
    {
      "ADB Command": "adb shell am start -a android.intent.action.VIEW -d deskclock://deskclock.android.com/main/SettingsActivity",
      "Function Description": "打开时钟设置，铃声、音量、响铃时长",
      "Parameter Information": "No additional parameters required."
    },
    {
      "ADB Command": "adb shell am start -a com.android.deskclock.shortcut.START_TIMER",
      "Function Description": "启动计时器",
      "Parameter Information": "No additional parameters required."
    },
    {
      "ADB Command": "adb shell am start -a com.android.deskclock.shortcut.STOP_WATCH",
      "Function Description": "启动秒表",
      "Parameter Information": "No additional parameters required."
    }
[Action history]: 
Action: click(<img id="com.miui.home:id/icon_icon" class="android.widget.ImageView" description="时钟" clickable="true">  </img>)
Action: click(<img id="com.android.deskclock:id/end_btn2" class="android.widget.ImageButton" description="添加闹钟" clickable="true">  </img>)
Action: click(<div id="com.android.deskclock:id/hour" class="com.android.deskclock.widget.NumberPicker" description="11时" clickable="true" scrollable="true" bounds="[370,319][709,1036]"> 11.0 </div>)
[Answer]: The task is not finished, There is no action in the API that can handle click on the eleven hours, so the next action category is UI action

Example 2:
[Task description]: Calculate 9×5+2
[Planning]: I should turn on my computer and click key by key.
[Thought]: I have already calculate 9×5+2 = 47, there is no need for any further action.
[ADB API]: 
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
[Action history]: 
Action: click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>)
Action: click(<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" alt="乘" clickable="true">  </img>)
Action: click(<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>)
Action: click(<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" alt="加" clickable="true">  </img>)
Action: click(<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true"> 2,  </p>)
Action: click(<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" alt="等于" clickable="true">  </img>)
[Answer]: Yes, in history i have already click 9*5+2= ,the task is ended.

Example 3:
[Task description]: Read the latest message.
[Planning]: I should open Messages before I can view recent text messages, then using this one application should be enough.
[Thought]:
I am on the home page and I should open Messages first.
[ADB API]: 
{
      "ADB Command": "adb shell am start -n com.android.mms/.ui.MmsTabActivity\n",
      "Function Description": "短信打开主界面",
      "Parameter Information": "无额外参数要求"
    },
    {
      "ADB Command": "adb shell am start -a android.intent.action.SEND -n com.android.mms/.ui.ComposeMessageRouterActivity --es sms_body \"消息内容\"",
      "Function Description": "此命令仅用于发送纯文本消息",
      "Parameter Information": "消息内容 替换为要发送的消息内容"
    },
    {
      "ADB Command": "adb shell am start -a android.intent.action.VIEW -n com.android.mms/.ui.ComposeMessageRouterActivity -d \"sms://\" --es address \"电话号码\"",
      "Function Description": "此命令用于查看或发送SMS消息",
      "Parameter Information": "No additional parameters required."
    },
    {
      "ADB Command": "adb shell am start -a miui.intent.action.APP_SETTINGS -n com.android.mms/.ui.MessagingPreferenceActivity",
      "Function Description": "此命令打开短信应用的设置界面",
      "Parameter Information": "No additional parameters required."
    },
    {
      "ADB Command": "adb shell am start -a android.intent.action.VIEW -n com.android.mms/.ui.ManageSimMessages",
      "Function Description": "此命令用于管理SIM卡上的短信",
      "Parameter Information": "No additional parameters required."
    }
[Action history]: There is no action yet.
[Answer]: The task is just begin, I can use adb shell am start -n com.android.mms/.ui.MmsTabActivity to open the SMS main interface, So the next action type is adb.
'''

generate_commands = '''
假设你是最优秀的手机智能助手，我需要你协助我完成以下任务。
你将会被提供一组用户动作交互历史，每个交互描述中包含动作和当前页面信息；
根据历史你需要猜测用户在完成的任务是什么？告诉我任务描述。
你的回答需要满足以下两个要求：
    1. 任务描述不要过于冗长，请尽可能包含动作历史中的信息，尽可能考虑每个动作的必要性。
    2. 不要回答和任务无关的其他内容。
------下面是一组例子：
{command_example}
------例子结束

------以下是你需要回答的任务：
[历史动作]: {action_history}
[任务指令]: 
'''


command_example = '''
例子1：
[历史动作]: 
1. 用户在电子商务平台的首页浏览，通过滚动屏幕查看不同的商品分类和推荐商品。
2. 继续滚动屏幕，用户专注于“运动”类别，查看相关的商品和促销信息。
3. 用户在浏览过程中，注意到特定的产品推荐，如“干性肌肤粉底液”和相关的促销广告。
4. 最后，用户点击“首页”按钮，可能是为了重新定位到应用的主界面或刷新页面以查看新的促销和商品推荐。
[任务指令]: 
查看“运动”和“女装”中包含的商品，查看结束后请确保返回首页。

例子2：
[历史动作]: 
1. 用户点击“运动休闲鞋”分类，表明他们对购买此类鞋子感兴趣。
2. 用户进一步细化搜索，点击“女童”选项，显示出对特定人群（女童）的运动休闲鞋感兴趣。
3. 用户关注商品的特定功能，点击“减震”选项，表明他们在寻找具有减震功能的运动鞋。
[任务指令]: 
为女童寻找具有减震功能的运动休闲鞋。

例子3：
[历史动作]: 
1. 用户选择点击“面膜”类别，进入相关产品页面。
2. 在面膜产品页面，用户看到不同功效的分类标签，选择点击“淡纹紧致”标签，以筛选出具有该特定功效的面膜产品。
3. 在“淡纹紧致”面膜的搜索结果中，用户浏览了不同品牌和价格的面膜，选择点击“睡眠免洗面膜榜”进入该类别的热销榜页面。
4. 在“睡眠免洗面膜榜”页面，用户查看了根据销量和销售指标综合排序的热销产品，界面设计使用户能够快速了解热门商品和推荐产品。
[任务指令]: 
给我推荐具有淡纹紧致功能的睡眠面膜，此外，参考排行榜是必要的。
'''
template = '''
假设你是最优秀的手机智能助手，我需要你协助我完成以下任务。
输入格式是：
你将会被提供一组用户交互历史，每个交互描述中包含当前页面caption和一个动作action；
您的任务是：
分析每个action分别在对应的页面上做了什么动作，把这些动作序列总结成一个任务描述，请注意任务描述应该是一个要求，例如：我想要看VIP的特权有哪些；帮我看看正在打折的裤子；告诉我当前购物车里有什么东西。 
请注意！任务描述和动作序列之间应该有对应的逻辑关系。
输出格式：
“分步描述”：“提供了一组交互历史，其中每个条目对应一个当前手机截图的caption和对该页面的动作action。”
“简洁任务”：“根据分步描述，生成一个符合这个动作顺序的任务”
下面是一个例子：
输入：
Caption 1:
这张图片显示的是一个手机屏幕截图，具体是一个购物应用的界面。
Action 1:
click(护肤套装)
Caption 2:
这张图片显示的是一个手机屏幕截图。在顶部，有一个搜索栏，上面写着“护肤套装”。此外，在页面底部还有一个导航栏，上面有“全部商品”、“新货上架”、“保湿”、“干性肌肤”、“烟酰胺”和“玻尿酸”等选项，当前状态是“全部商品”
Action 2:
click(新货)
Caption 3:
这张图片显示的是一个手机屏幕截图，具体是一个购物应用的界面。在顶部，有一个搜索栏，上面写着“护肤套装”。此外，在页面底部还有一个导航栏，上面有“全部商品”、“新货上架”、“保湿”、“干性肌肤”、“烟酰胺”和“玻尿酸”等选项，当前状态是“新货上架”。下面有多个商品推荐。
Action 3:
click(广告)
Caption 4:
这张图片显示的是一个商品详情页面。页面顶部有一个粉色背景的横幅，上面写着“买一套带走13件”，并配有一张产品照片。
输出：
分步描述：
1. 在购物应用的“推荐”类别下的“美妆”子类别中，点击“护肤套装”商品。
2. 在护肤套装的搜索结果页面，继续点击带有“新货”标签的商品。
3. 在商品详情页面点击“广告”标签。
简洁任务：
帮我找到一个最新的护肤套装，需要是正在进行促销活动的。
这是你需要回答的：
输入：

{chain_description}

请生成“分步描述”和“简洁任务”：

输出：
'''
