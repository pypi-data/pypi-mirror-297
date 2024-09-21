import json
import os

import prettytable as pt
from HF_QuickUtils.QuickUtils import QuickDownload
import shutil


def remove_empty_dirs(path, verbose=False):
    """
    递归删除给定路径下的所有空文件夹

    :param path: 字符串，指定要检查的根目录
    :param verbose: 布尔值，是否打印删除的文件夹信息
    """
    if not os.path.isdir(path):
        return

        # 获取目录下所有项（文件和子目录）
    items = os.listdir(path)

    # 如果目录下没有任何项，则删除该目录
    if not items:
        os.rmdir(path)
        if verbose:
            print(f"Deleted empty directory: {path}")
    else:
        # 递归检查子目录
        for item in items:
            item_path = os.path.join(path, item)
            remove_empty_dirs(item_path, verbose)


def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # os.path.getsize() 返回文件大小（以字节为单位）
            total_size += os.path.getsize(file_path)
    power = 2 ** 10
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB', 5: 'PB'}
    while total_size > power:
        total_size /= power
        n += 1
    size_str = f"{total_size:.2f} {power_labels[n]}"
    return size_str

def traverse_two_levels(root_dir):
    """
    遍历指定文件夹及其直接子文件夹
    :param root_dir: 顶层文件夹的路径
    """
    items = []
    # 检查路径是否存在
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a directory.")
        return
        # 遍历顶层文件夹
    for item in os.listdir(root_dir):
        if [".cache", ".locks", "hub"].__contains__(item):
            continue
        full_path = os.path.join(root_dir, item)
        if os.path.isdir(full_path):
            for sub_item in os.listdir(full_path):
                relative_path_sub = os.path.join(item, sub_item)
                items.append(relative_path_sub)
    return items
def to_hub_name(name: str) -> str:
    rev=name
    rev=rev.replace("\\", "-")
    rev=rev.replace("/", "-")
    rev="model--"+rev
    return rev

class ModelManager:
    def __init__(self):
        from HF_QuickUtils import get_hf_home
        self.hf_home = get_hf_home()
        if self.hf_home == "":
            raise Exception("hf_home is empty")
        self.model_path = traverse_two_levels(self.hf_home)
    def get_model_path(self):
        return self.model_path
    def print_model_info(self):
        tb = pt.PrettyTable()
        tb.field_names=["Model","size","tf_version","architectures"]
        for path in self.model_path:
            with open(self.hf_home+"/"+path+'/config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                #load data
                name = path
                size_str =get_folder_size(self.hf_home+"/"+path)
                tf_version =data["transformers_version"] if data.keys().__contains__("transformers_version") else "Unknown"
                architectures=data["architectures"]
                tb.add_row([name,size_str,tf_version,architectures])
        print(tb)
    def install(self,repo,maxworkers=8):
        QuickDownload(repo=repo).download(maxworkers)
    def remove(self,repo):
        print("try deleting the repository:"+repo)
        shutil.rmtree(self.hf_home+"/"+repo)
        remove_empty_dirs(self.hf_home)
        if os.path.exists(self.hf_home+"/hub/"+to_hub_name(repo)):
            print("Try deleting the model in hub")
            shutil.rmtree(self.hf_home+"/hub/"+to_hub_name(repo))
        print("remove completely")
