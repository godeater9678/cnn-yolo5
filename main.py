import os
import pandas as pd
from common.gpuTest import check_cuda
from domain.yolo.classifier.foodFighter import classify_image
from common.util import normalize_filenames
from deep_translator import GoogleTranslator

_PATH_SHEET = 'resources/yolo/음식분류 AI 데이터 영양DB.xlsx'
_PATH_IMAGES = 'resources/yolo/images'
_SHEET_NAME = '400외식메뉴'
_KEY_COLUMN = '음 식 명'
_NAME_DICT = {
    'bulgogi': '불고기덮밥',
    'bibimbap': '일반비빔밥',
    'Japchae': '잡채',
    'fried rice': '볶음밥',
}


def display_food_info(foodName: str):
    # Load the Excel file
    file_path = f"{_PATH_SHEET}"
    # Load the data from the sheet
    df = pd.read_excel(file_path, sheet_name=_SHEET_NAME)
    filtered_data = df[df[_KEY_COLUMN] == foodName]
    if filtered_data.empty:
        print(font_red(f"Food name {foodName} not found in the database(excel)."))
        return
    # Convert the filtered data to the desired format
    filtered_data_dict = filtered_data.to_dict(orient='records')[0]
    formatted_output = format_aligned(filtered_data_dict)
    print(formatted_output)


def format_aligned(data):
    # Determine the maximum length of column names for alignment
    max_col_len = max(len(col) for col in data.keys())
    # Create formatted string with aligned columns
    formatted_str = "\n".join([f"{col.ljust(max_col_len)} : {val}" for col, val in data.items()])
    return formatted_str


def list_files_full_path(directory):
    normalize_filenames(directory=directory)
    files_list = os.listdir(directory)
    full_paths = [os.path.join(directory, file) for file in files_list]
    return sorted(full_paths)


def font_yellow(string):
    return f"\033[93m{string}\033[0m"


def font_red(string):
    return f"\033[91m{string}\033[0m"


# ---------------main.py----------------
# GPU 활성화 확인
print(font_red('\n\n하드웨어 확인'))
check_cuda()
print(font_yellow(f'\n\n이미지 분석 : {_PATH_IMAGES}'))
# 이미지 파일 경로 리스트
files = list_files_full_path(_PATH_IMAGES)
for file in files:
    print("\n-------------------------------------------------------------\n")
    result = classify_image(file)
    names = None if result is None else result['names']
    if names is None:
        print(font_red(f"file: {file} : No food detected(yolo)."))
        continue
    for name in names:
        name_kr = _NAME_DICT.get(name, GoogleTranslator(source='en', target='ko').translate(name))
        print(font_yellow(f"file: {file} : detected as {name} / {name_kr}"))
        display_food_info(name_kr)
    #result['results'].show()
    #input("Press any key to continue...")