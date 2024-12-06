# Copyright (C) 2024 Xiaomi Corporation.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


import pandas as pd

def get_app_info(csv_file, app_name):
    # 读取CSV文件
    df = pd.read_csv(csv_file, delimiter=',')  # 请根据实际情况修改分隔符

    # 根据app_name查询行
    app_row = df[df['app_name'] == app_name]

    # 如果找到匹配的行，返回对应的信息
    if not app_row.empty:
        info = {
            'package_name': app_row.iloc[0]['package_name'],
            'level1_category_name': app_row.iloc[0]['level1_category_name'],
            'key_words': app_row.iloc[0]['key_words'],
            'introduction': app_row.iloc[0]['introduction'],
            # 'change_log': app_row.iloc[0]['change_log'],
            # 'date': app_row.iloc[0]['date']
        }
        return info
    else:
        return None


csv_file_path = 'adhoc.csv'
app_name_to_search = 'Slots 2019 Casino'
app_info = get_app_info(csv_file_path, app_name_to_search)

if app_info:
    print(f"App Info for {app_name_to_search}:")
    for key, value in app_info.items():
        print(f"{key}: {value}")
else:
    print(f"No information found for {app_name_to_search}.")

