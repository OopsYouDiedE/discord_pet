# list[dict[名称，主人名，经验，饥饿，娱乐，精力]]有一部分需要用修正器，也就是buff记录器。
import os.path
import random

import yaml


class PetManager:
    """
    包含：名称，主人名，经验，饥饿，娱乐，精力等一系列属性。
    包含一个buff管理器。自带tick方法。
    """

    @staticmethod
    def yaml_load(path, default=None):
        if default is None:
            default = {}
        if not os.path.exists(path):
            print('没有该路径，下次调用时创建。')
            return default
        else:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

    def __init__(self):
        # 加载以下内容：buff管理器，宠物属性记录，初始化属性。
        self.buff = self.yaml_load('buff_data.yaml')
        self.pet_attr = self.yaml_load('pet_attributes.yaml')
        self.pet_init = self.yaml_load('pet_init.yaml')

    def tick(self, delt: float = 1):
        # 首先根据buff更新pet_attr；然后减去buff的维持时间。buff:{buffa:{buff:{xx:x},left_time:x}}
        for buff in self.buff.values():
            buff['left_time'] -= delt
            b_dict = buff['buff']
            for i in b_dict:
                self.pet_attr[i] += b_dict[i]
        for buff in tuple(self.buff.keys()):
            if self.buff[buff]['left_time'] <= 0:
                self.buff.pop(buff)

    def add_pet(self, owner_id: str, name: str, image: str):
        ID = str(random.randint(0, 10000000))
        self.pet_attr[ID] = {
            'owner': {'value': owner_id},
            'name': {'value': name},
            'image': {'value': image},
            'hunger': {
                'max': 100,
                'value': 50
            },
            'happiness': {
                'max': 100,
                'value': 50
            },
            'experience': {
                'max': 100,
                'value': 0
            },
            'level': {
                'max': 10,
                'value': 0
            },
        }
        self.pet_init[ID] = {
            '基础变动': {
                'buff': {
                    'hunger': -0.2,
                    'happiness': -0.1
                },
                'left_time': 999999
            }
        }

    def get_values(self):
        return {k: {k1: v1['value'] for k1, v1 in v} for k, v in self.pet_attr}

    def save(self):
        with open('buff_data.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.buff, f, allow_unicode=True)
        with open('pet_attributes.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.pet_attr, f, allow_unicode=True)
        with open('pet_init.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.pet_init, f, allow_unicode=True)
