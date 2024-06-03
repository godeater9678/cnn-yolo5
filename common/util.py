
import os
import unicodedata


def get_root_path():
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 프로젝트 루트 경로 (필요에 따라 상위 디렉토리로 이동)
    project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
    return project_root

# 디렉토리 내 모든 파일 이름을 NFC 형식으로 변환
def normalize_filenames(directory):
    for filename in os.listdir(directory):
        nfc_filename = unicodedata.normalize('NFC', filename)
        if filename != nfc_filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, nfc_filename)
            os.rename(old_path, new_path)
            #print(f'Renamed: {filename} -> {nfc_filename}')