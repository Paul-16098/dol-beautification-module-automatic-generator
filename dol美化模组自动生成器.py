# coding=utf-8
import os
import json
import shutil
import zipfile
import atexit
from logger import logger
from retry import retry # type: ignore
from timing import get_time

# 初始化
logger = logger()

@get_time
def main():
    ver = "1.0.0.0"
    temp = 'temp'
    readme = ['LICENSE', 'LICENSE.txt', 'README.md', 'README.txt', 'CREDITS.md']

    @get_time
    @retry()
    def cleanup():
            # 刪除臨時目錄
            logger.del_temp()
    # 註冊清理函數
    atexit.register(cleanup)

    @retry()
    @get_time
    def zip_files_and_folders(file_paths, zip_name):
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                if os.path.isdir(file_path):
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.dirname(file_path)))
                else:
                    try:
                        zipf.write(file_path, os.path.basename(file_path))
                    except FileNotFoundError:
                        logger.log_(f"檔案不存在: {file_path}", 'warn')

    @retry()
    @get_time
    def list_files_and_subdirectories(directory, output_dict):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), directory)
                file_extension = os.path.splitext(file_path)[1].lower()
                if file_extension != '.png' and file_extension != '.gif':
                    output_dict["additionFile"].append('img/' + file_path.replace("\\", "/"))
                else:
                    output_dict["imgFileList"].append('img/' + file_path.replace("\\", "/"))

    os.makedirs('img', exist_ok=True)

    output_dict = {}
    
    logger.log_("===========================")
    logger.log_("dol美化模组自动生成器")
    logger.log_(f"v{ver}    By Paul-16098")
    logger.log_("===========================")
    
    while True:
        output_dict['name'] = logger.input_('請輸入模組名稱: ')
        output_dict['version'] = logger.input_('請輸入類似於1.0.0的模組版本號: ')
        yne = logger.input_("確定? (Yes/Not/Exit): ", "log", "red").lower()
        if yne in ("y", "yes"):
            break
        elif yne in ("e", "exit"):
            cleanup()
            os._exit(0)
    logger.log_('模組生成中請稍等...')
    output_dict['styleFileList'] = []
    output_dict['scriptFileList'] = []
    output_dict['tweeFileList'] = []
    output_dict['additionFile'] = []
    output_dict['imgFileList'] = []
    for file_path in readme:
        if os.path.exists(file_path) is not False: # 如果file_path存在
            output_dict['additionFile'].append(file_path)
    list_files_and_subdirectories('img', output_dict)
    output_dict['addonPlugin'] = [
        {
        "modName": "ModLoader DoL ImageLoaderHook",
        "addonName": "ImageLoaderAddon",
        "modVersion": "^2.3.0",
        "params": [
        ]
        }
    ]
    output_dict['dependenceInfo'] = [
        {
        "modName": "ModLoader DoL ImageLoaderHook",
        "version": "^2.3.0"
        }
    ]

    os.makedirs('temp', exist_ok=True)

    # 將內容輸出到文本文件
    with open('temp\\boot.json', 'w', encoding='utf-8') as file:
        json.dump(output_dict, file, indent=2, ensure_ascii=False)

    # 要壓縮的文件和文件夾路徑列表
    file_paths = ['img', f'{temp}\\boot.json', 'LICENSE', 'LICENSE.txt', 'README.md', 'README.txt', 'CREDITS.md']

    # 壓縮後的文件名
    zip_name = output_dict['name'] + '.mod.zip'

    zip_files_and_folders(file_paths, os.path.join(temp, zip_name))

    if os.path.exists(zip_name) is not False: # 如果zip_name存在
        os.remove(zip_name) # 刪除 zip_name
    shutil.move(os.path.join(temp, zip_name), os.curdir)
    print('')
    logger.log_(f'模组生成完成: {output_dict["name"] + ".mod.zip"}')
    logger.log_(f'檔案大小: {os.path.getsize(zip_name)}位元組')

    os.system("pause")

if __name__ == '__main__':
    main()