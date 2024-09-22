import find_homework_yuketang.tool as tool

# 获取cookie
cookies_list = tool.getCookies()
cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}

# 获取课堂数据与本地数据
class_list = tool.getClasses(cookies)
choosed_class = tool.getLocalChoseClass() or []

# 每次都会检查课程是否还存在
choosed_class = [_class1 for _class1 in choosed_class if any(_class2['classroom_id'] == _class1['classroom_id'] for _class2 in class_list)]
tool.writeLocalChoseClass(choosed_class)

opt_list = [
    '添加课程入本地已选择课程',
    '查询当前本地已选择课程',
    '删除当前本地已选择课程',
    '查询作业',
]

while True:
    print('-' * 20)
    for indice, opt_name in enumerate(opt_list, 1):
        print(f'{indice}.{opt_name}')
    opt = int(input())
    if opt == 1:
        for indice, _class in enumerate(class_list, 1):
            print(f'{indice}.课程名：{_class['name']}\n老师名：{_class['teacher']['name']}\n')
        print('-' * 20)
        print('请选择需要加入的课程：')
        serial_num = int(input())
        if 0 < serial_num <= len(class_list):
            selected_class = class_list[serial_num - 1]
            if not any(_class['classroom_id'] == selected_class['classroom_id'] for _class in choosed_class):
                choosed_class.append(selected_class)
                tool.writeLocalChoseClass(choosed_class)
            else:
                print('课程早已保存')
        else:
            print('该索引不存在')
    elif opt == 2:
        print('-' * 20)
        print('当前本地已选课程：')
        for indice, _class in enumerate(choosed_class, 1):
            print(f'{indice}.课程名：{_class['name']}\n老师名：{_class['teacher']['name']}\n')
    elif opt == 3:
        print('-' * 20)
        print('当前本地已选课程：')
        for indice, _class in enumerate(choosed_class, 1):
            print(f'{indice}.课程名：{_class['name']}\n老师名：{_class['teacher']['name']}\n')
        print('请输入需要删除的课程：')
        serial_num = int(input())
        if 0 < serial_num <= len(choosed_class):
            del choosed_class[serial_num - 1]
            tool.writeLocalChoseClass(choosed_class)
        else:
            print("索引不存在")
    elif opt == 4:
        print('-' * 20)
        tool.queryClassListWork(choosed_class, cookies)