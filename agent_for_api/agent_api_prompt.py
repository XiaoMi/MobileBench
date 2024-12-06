# Copyright (C) 2024 Xiaomi Corporation.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


from agent_for_api.API_list import *
select_api_prompt = '''
You are the largest large language model agent stored on the phone.
It will give you a list of APIs that the phone can call, the tasks that need to be completed, what has been done, and what needs to be done now.
You need to choose one of the above APIs to complete the action that needs to be completed now.
You should not use the API to complete the work that has been completed by the UI interaction components in the previous steps.
Your decision should consider the following factors:
1. You must only choose one API that should be executed most at the moment to complete the first action in next action.
2. If there is no suitable API, you only need to say sorry without providing any additional suggestions.
The string in <> needs to be replaced with specific parameters and must return a fully executable adb command.
API list: {api_list}
Below are some examples.
-----
{select_api_example}
-----

Your [Answer] can only follow the two templates: "Yes, the most suitable api function call is [adb command]" or "Sorry,[explain]" 
[Task]: {task}
[Planning]: {planning}
[UI information]: {ui_information}
[Actions History]: {memory}
[WARNING]: It is strictly prohibited to use any commands other than the ADB commands listed in the API list.
[Answer]: 
'''
#
# shell 似乎可以直接调用基本运算，这是意料之外的事情。
#
'''
Notice!
You must choose only one API that should be executed most at present and give the specific adb command in [].
The API you choose must come from the API list. APIs from unknown sources are prohibited from being used.
If an API command fails to execute in the actions history, you should no longer use it as an answer.
'''

select_api_example = '''
Example 1：
[Task]：I'm going to travel to Beijing next week. Please help me determine the hotel and specific time.
[Planning]: Open the travel APP, check Beijing hotels, sort by rating, recommend the top three, then open Google search, search and check the weather conditions in Beijing next week.
[UI inforamtion]: 
<div id="com.google.android.apps.nexuslauncher:id/workspace" class="android.widget.ScrollView" clickable="false" scrollable="true" bounds="[0,0][1080,1857]">  </div>
<p class="android.widget.TextView" description="ClevCalc" clickable="true"> ClevCalc </p>
<p class="android.widget.TextView" description="New event" clickable="true"> New event </p>
<p class="android.widget.TextView" description="Traveloka" clickable="true"> Traveloka </p>
<p class="android.widget.TextView" description="Weather" clickable="true"> Weather </p>
<p class="android.widget.TextView" description="Clock" clickable="true"> Clock </p>
<p class="android.widget.TextView" description="Maps" clickable="true"> Maps </p>
<p class="android.widget.TextView" description="Play Store" clickable="true"> Play Store </p>
<p class="android.widget.TextView" description="Agent-LLM" clickable="true"> Agent-LLM </p>
<div class="android.view.View" description="Home" clickable="false">  </div>
<p class="android.widget.TextView" description="Phone" clickable="true"> Phone </p>
<p class="android.widget.TextView" description="Messages" clickable="true"> Messages </p>
<p class="android.widget.TextView" description="Play Store" clickable="true"> Play Store </p>
<p class="android.widget.TextView" description="Chrome" clickable="true"> Chrome </p>
<p class="android.widget.TextView" description="Camera" clickable="true"> Camera </p>
<img id="com.google.android.apps.nexuslauncher:id/g_icon" class="android.widget.ImageView" description="Google app" clickable="true">  </img>
<img id="com.google.android.apps.nexuslauncher:id/mic_icon" class="android.widget.ImageView" description="Voice search" clickable="true">  </img>
<button id="com.google.android.apps.nexuslauncher:id/lens_icon" class="android.widget.ImageButton" description="Google Lens" clickable="true">  </button>
[Actions history]: No action has been completed yet
[Thought]: I am on the home page. No action has been completed yet. I will open the Traveloka app first and check the flight.
[Answer]：Yes, the most suitable api function call is [adb shell am start -n com.traveloka.android/.appentry.splash.SplashActivity]

Example 2:
[Task]: Recommend to me the most suitable ticket to Beijing this Saturday
[Planning]: 
1. Open Traveloka: 
   - Search for flights from Chengdu to Beijing for the desired date.
   - Take screenshots of the flight options, including prices and timings.
   - Save the screenshots in a designated folder on your phone for easy access.
[UI information]: 
<button id="com.traveloka.android:id/tray_text_button_left" class="android.widget.Button" clickable="true">  </button>
<p id="com.traveloka.android:id/tray_title" class="android.widget.TextView" clickable="false"> Your Trip </p>
<button id="com.traveloka.android:id/tray_text_button" class="android.widget.Button" clickable="true">  </button>
<button id="com.traveloka.android:id/tray_text_button2" class="android.widget.Button" clickable="true">  </button>
<p id="com.traveloka.android.flight:id/text_title_journey" class="android.widget.TextView" clickable="true"> Chengdu   Beijing </p>
<p id="com.traveloka.android.flight:id/text_card_title_departure" class="android.widget.TextView" clickable="true"> Sat, 25 Nov 2023 </p>
<p id="com.traveloka.android.flight:id/text_departure_time" class="android.widget.TextView" clickable="true"> 07:20 </p>
<p id="com.traveloka.android.flight:id/text_flight_duration" class="android.widget.TextView" clickable="true"> 2h 40m </p>
<p id="com.traveloka.android.flight:id/text_arrival_time" class="android.widget.TextView" clickable="true"> 10:00 </p>
<p id="com.traveloka.android.flight:id/badge_departure_airport" class="android.widget.TextView" clickable="true"> CTU </p>
<p id="com.traveloka.android.flight:id/text_flight_transit" class="android.widget.TextView" clickable="true"> Direct </p>
<p id="com.traveloka.android.flight:id/badge_arrival_airport" class="android.widget.TextView" clickable="true"> PKX </p>
<p id="com.traveloka.android.flight:id/text_airline_name" class="android.widget.TextView" clickable="true"> China Eastern Airlines </p>
<p id="com.traveloka.android.flight:id/text_seat_class" class="android.widget.TextView" clickable="true"> Economy </p>
<p id="com.traveloka.android.flight:id/text_details" class="android.widget.TextView" clickable="true"> Details </p>
<p id="com.traveloka.android.flight:id/text_title" class="android.widget.TextView" clickable="false"> Your ticket type </p>
<p id="com.traveloka.android.flight:id/text_title" class="android.widget.TextView" clickable="true"> Original </p>
<p id="com.traveloka.android.flight:id/text_price" class="android.widget.TextView" clickable="true"> USD  125.71 </p>
<p id="com.traveloka.android.flight:id/text_per_pax" class="android.widget.TextView" clickable="true"> /pax </p>
<p id="com.traveloka.android.flight:id/text" class="android.widget.TextView" clickable="true"> Cabin baggage 1 x 5 kg </p>
<p id="com.traveloka.android.flight:id/text" class="android.widget.TextView" clickable="true"> Baggage 1 x 20 kg </p>
<p id="com.traveloka.android.flight:id/text" class="android.widget.TextView" clickable="true"> Reschedule not available </p>
<p id="com.traveloka.android.flight:id/text" class="android.widget.TextView" clickable="true"> Refund info unavailable </p>
<p id="com.traveloka.android.flight:id/text_see_detail" class="android.widget.TextView" clickable="true"> Learn more </p>
<p id="com.traveloka.android.flight:id/text_view_label" class="android.widget.TextView" clickable="true"> Total price for 1 person(s) </p>
<p class="android.widget.TextView" description="pre_booking_price" clickable="true"> USD  125.71 </p>
<p id="com.traveloka.android.flight:id/text_description" class="android.widget.TextView" clickable="true"> Inclusive of all fares & taxes </p>
<button id="com.traveloka.android.flight:id/button_select" class="android.widget.Button" clickable="true"> Continue </button>
[Actions history]: 
{'[API call]': 'adb shell am start -n com.traveloka.android/.appentry.splash.SplashActivity. [Call result]:API execution successful'}
{'[Action]': 'click(<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Flights </p>)'}
{'[Action]': 'click(<input id="com.traveloka.android:id/edit_text_field" class="android.widget.EditText" clickable="true"> Saturday, 25 Nov 2023 </input>)'}
{'[Action]': 'click(<div id="com.traveloka.android:id/calendar_date_text" class="android.view.View" description="25" clickable="true">  </div>)'}
{'[Action]': 'click(<button id="com.traveloka.android.flight:id/btn_search" class="android.widget.Button" description="flight_searchform_button_search" clickable="true"> Search </button>)'}
{'[Action]': 'click(<p id="com.traveloka.android.flight:id/text_flight_name" class="android.widget.TextView" description="text_view_flight_name " clickable="true"> China Eastern Airlines </p>)'}

[Thought]: I have already opened the traveloka, searched for flight from chengdu to beijing this Saturday, And i found the cheapest flight. Then, I will take the screenshot and save it.
[Answer]：Yes, the most suitable api function call is [adb shell screencap -p /sdcard/flight_info.png]
'''
# Task: 今晚8点要洗衣服， 请建立备忘录提醒我
# Ans：Yes, the api function call is :"adb shell am start -a android.intent.action.INSERT -t vnd.android.cursor.item/event --es title "洗衣服" --es description "今晚不要忘记洗衣服" --ez allDay false --ei beginTime 1662820800000 --ei endTime 1662824400000"
'''
Example 1:
[Task]：Hello, I plan to travel from Chengdu to Beijing on business next week to attend the Xiaomi Technology Park meeting on Sunday. Please help me plan the specific travel time and mode, and make simple suggestions.

[Planning]: To plan your travel from Chengdu to Beijing, we can use the following apps:

1. Open Traveloka: 
   - Search for flights from Chengdu to Beijing for the desired date.
   - Take screenshots of the flight options, including prices and timings.
   - Save the screenshots in a designated folder on your phone for easy access.

2. Open Weather:
   - Check the weather forecast for both Chengdu and Beijing for the upcoming week.
   - Take screenshots of the weather forecast for each city.
   - Save the screenshots in the same folder as the flight options.

3. Open New event:
   - Create a memo titled "Travel Plan to Beijing."
   - Write down the recommended flight options, including the airline, departure time, and arrival time.
   - Mention the weather conditions in Chengdu and Beijing for the travel dates.
   - Save the memo for easy review.

By using Traveloka, Weather, and New event apps, you can gather the necessary information and save it on your phone for future reference. Remember, this plan does not involve directly booking the tickets; it's solely for collecting information and making suggestions.
[UI information]: 
<div id="com.traveloka.android:id/recycler_view" class="androidx.recyclerview.widget.RecyclerView" clickable="false" scrollable="true" bounds="[0,63][1080,1723]">  </div>
<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Flights </p>
<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Hotels </p>
<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Xperience </p>
<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Airport Transfer </p>
<p id="com.traveloka.android:id/text_view_product_text" class="android.widget.TextView" clickable="true"> Car Rental </p>
<p id="com.traveloka.android:id/text_background_banner" class="android.widget.TextView" clickable="false"> Get access to Traveloka's complete features by choosing to enable location service all the time. </p>
<p id="com.traveloka.android:id/text_allow_background" class="android.widget.TextView" clickable="false"> Enable </p>
<p id="com.traveloka.android:id/text_widget_item_description" class="android.widget.TextView" clickable="true"> You're missing security alerts, booking updates, and chat replies. </p>
<p id="com.traveloka.android:id/text_widget_item_button" class="android.widget.TextView" clickable="true"> Check notification settings </p>
<p id="com.traveloka.android:id/text_view_title" class="android.widget.TextView" clickable="true"> Flight Discount up to 10% is yours! </p>
<p id="com.traveloka.android:id/text_view_subtitle" class="android.widget.TextView" clickable="true"> Just book a trip and explore the world </p>
<p id="com.traveloka.android:id/text_more_button" class="android.widget.TextView" clickable="true"> More </p>
<button id="com.traveloka.android:id/icon_notification" class="android.widget.ImageButton" description="Open Notification" clickable="true">  </button>
<button id="com.traveloka.android:id/icon_inbox" class="android.widget.ImageButton" description="Open Inbox" clickable="true">  </button>
<p id="com.traveloka.android:id/text_label" class="android.widget.TextView" clickable="true"> Home </p>
<p id="com.traveloka.android:id/text_label" class="android.widget.TextView" clickable="true"> Explore </p>
<p id="com.traveloka.android:id/text_label" class="android.widget.TextView" clickable="true"> Bookings </p>
<p id="com.traveloka.android:id/text_label" class="android.widget.TextView" clickable="true"> Saved </p>
<p id="com.traveloka.android:id/text_label" class="android.widget.TextView" clickable="true"> My Account </p>

[Actions history]: 
{'[API call]': 'adb shell am start -n com.traveloka.android/.appentry.splash.SplashActivity. [Call result]:API execution successful'}

[Thought]: Based on the changes in UI information and action history, the following steps have been completed:

1. The Traveloka app was opened by clicking on the "Traveloka" option.
2. The app successfully launched, and the current UI information shows the available products: Flights, Hotels, Xperience, Airport Transfer, and Car Rental.

Next, you should perform the following actions:

1. Click on the "Flights" option in the Traveloka app to search for flights.
2. Enter the necessary travel details, such as the origin (Chengdu) and destination (Beijing), and select the desired travel dates.
3. Take screenshots of the flight options, including prices and timings.
4. Save the screenshots in a designated folder on your phone for easy access.
5. Open the Weather app to check the weather forecast for both Chengdu and Beijing for the upcoming week.
6. Take screenshots of the weather forecast for each city.
7. Save the weather forecast screenshots in the same folder as the flight options.
8. Open the New event app and create a memo titled "Travel Plan to Beijing."
9. Write down the recommended flight options, including the airline, departure time, and arrival time.
10. Mention the weather conditions in Chengdu and Beijing for the travel dates.
11. Save the memo for easy review.

Remember, this plan does not involve directly booking the tickets but focuses on collecting information and making suggestions.

[Answer]：Sorry, the next action is to click the "Flights" option. I cannot complete it through the appropriate API. I suggest handing over this task to the UI interaction module.



Example 1:
[Task description]: Calculate 9.5×5+2
[Planning]: Open a computing-related application and click the buttons one by one.
[UI information]: 
<img class="android.widget.ImageView" description="小窗" clickable="true">  </img>
<p class="android.widget.TextView" clickable="true"> 计算 </p>
<p class="android.widget.TextView" clickable="true"> 换算 </p>
<img id="com.miui.calculator:id/more" class="android.widget.ImageView" description="更多选项" clickable="true">  </img>
<div id="com.miui.calculator:id/view_pager" class="androidx.viewpager.widget.OriginalViewPager" clickable="false" scrollable="true" bounds="[0,275][1080,2400]">  </div>
<div id="com.miui.calculator:id/expression" class="android.view.View" description="9.5×5" clickable="true">  </div>
<p id="com.miui.calculator:id/result" class="android.widget.TextView" description="= 47.5" clickable="true"> = 47.5 </p>
<img id="com.miui.calculator:id/btn_c_s" class="android.widget.ImageView" description="清除" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_7" class="android.widget.TextView" clickable="true"> 7 </p>
<p id="com.miui.calculator:id/digit_4" class="android.widget.TextView" clickable="true"> 4 </p>
<p id="com.miui.calculator:id/digit_1" class="android.widget.TextView" clickable="true"> 1 </p>
<img id="com.miui.calculator:id/btn_switch" class="android.widget.ImageView" description="切换" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_del_s" class="android.widget.ImageView" description="退格" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_8" class="android.widget.TextView" clickable="true"> 8 </p>
<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5 </p>
<p id="com.miui.calculator:id/digit_2" class="android.widget.TextView" clickable="true"> 2 </p>
<p id="com.miui.calculator:id/digit_0" class="android.widget.TextView" clickable="true"> 0 </p>
<img id="com.miui.calculator:id/op_pct" class="android.widget.ImageView" description="百分号" clickable="true">  </img>
<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9 </p>
<p id="com.miui.calculator:id/digit_6" class="android.widget.TextView" clickable="true"> 6 </p>
<p id="com.miui.calculator:id/digit_3" class="android.widget.TextView" clickable="true"> 3 </p>
<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" description="小数点" clickable="true"> . </p>
<img id="com.miui.calculator:id/op_div" class="android.widget.ImageView" description="除" clickable="true">  </img>
<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" description="乘" clickable="true">  </img>
<img id="com.miui.calculator:id/op_sub" class="android.widget.ImageView" description="减" clickable="true">  </img>
<img id="com.miui.calculator:id/op_add" class="android.widget.ImageView" description="加" clickable="true">  </img>
<img id="com.miui.calculator:id/btn_equal_s" class="android.widget.ImageView" description="等于" clickable="true">  </img>
[Actions history]: 
adb shell am start -n com.cleveni.app.calculator/com.cleveni.app.calculator.MainActivity
click(<p id="com.miui.calculator:id/digit_9" class="android.widget.TextView" clickable="true"> 9,  </p>)
click(<p id="com.miui.calculator:id/dec_point" class="android.widget.TextView" description="小数点" clickable="true"> . </p>)
click(<p id="com.miui.calculator:id/digit_5" class="android.widget.TextView" clickable="true"> 5,  </p>)
click(<img id="com.miui.calculator:id/op_mul" class="android.widget.ImageView" description="乘" clickable="true">  </img>)
[Thought]: Calculate 9.5×5+2, I have clicked on 9.5 and the multiplication sign, now I should click on 5.
Ans：Sorry, I can't help you click on 5 with suitbale api. I suggest handing over this task to the UI interaction module.

'''
