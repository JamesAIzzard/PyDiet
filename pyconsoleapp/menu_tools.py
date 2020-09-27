from typing import List, Dict


def create_number_name_map(list_to_map: List, start_num=1) -> Dict[int, str]:
    num_map: Dict[int, str] = {}
    for i, key in enumerate(list_to_map, start=start_num):
        num_map[i] = key
    return num_map
