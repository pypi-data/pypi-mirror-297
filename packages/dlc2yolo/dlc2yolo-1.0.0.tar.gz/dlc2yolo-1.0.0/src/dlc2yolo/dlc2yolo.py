# Copyright 2024 Hakureirm <wbj010101@gmail.com>

import json
import pandas as pd


def __merge_json_csv(json_path, csv_path, key) -> pd.DataFrame:
    # 打开并读取 JSON 文件
    with open(json_path, "r") as f:
        data_json = json.load(f)

    # 将 JSON 数据中的 "images" 字段转换为 DataFrame
    df_json = pd.DataFrame(data_json["images"])

    # 读取并处理 CSV 文件，将 'scorer' 列名改为 'file_name' 并将 key 字段重命名为 "{key}.0"
    df_csv = pd.read_csv(csv_path).rename(
        columns={"scorer": "file_name", key: f"{key}.0"}
    )

    # 处理 file_name 列，将路径中的 '/' 替换为 '_'
    df_csv.file_name = df_csv.file_name.apply(lambda x: "_".join(x.split("/")[1:]))

    # 合并 JSON 和 CSV 数据
    return pd.merge(df_json, df_csv, on=["file_name"])


def __norm_coords(row, key, count) -> list:
    # 归一化坐标
    normalized = []
    for i in range(0, count, 2):
        # 归一化 x 坐标
        px = (
            max(0, min(1, float(row[f"{key}.{i}"]) / row["width"]))
            if not pd.isna(row[f"{key}.{i}"])
            else None
        )
        # 归一化 y 坐标
        py = (
            max(0, min(1, float(row[f"{key}.{i+1}"]) / row["height"]))
            if not pd.isna(row[f"{key}.{i+1}"])
            else None
        )
        normalized.extend([px, py])
    return normalized


def __calculate_bbox(coords):
    # 计算边界框 (bounding box)
    valid_coords = [
        (x, y)
        for x, y in zip(coords[::2], coords[1::2])
        if x is not None and y is not None
    ]
    if not valid_coords:
        return None
    xs, ys = zip(*valid_coords)
    return [min(xs), min(ys), max(xs), max(ys)]


def __calculate_xywh(bbox):
    # 计算中心点 (x, y) 和宽高 (w, h)
    if bbox is None:
        return [0] * 4
    x = (bbox[0] + bbox[2]) / 2
    y = (bbox[1] + bbox[3]) / 2
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return [x, y, w, h]


def __format_coords(coords, precision):
    """
    将坐标格式化为字符串 <px0> <py0> <visibility0> <px1> <py1> <visibility1> ...
    """
    out = ""
    for i in range(0, len(coords), 2):
        if coords[i] is None or coords[i + 1] is None:
            out += "0 0 0 "
        else:
            out += f"{coords[i]:.{precision}f} {coords[i+1]:.{precision}f} 1 "
    return out


def __create_yolo(row, precision, root_dir, n_datapoint, datapoint_classes):
    # 创建 YOLO 格式文件
    out = ""
    for i in range(n_datapoint):
        out += f"{datapoint_classes[i]} {row[f'{i}_x']:.{precision}f} {row[f'{i}_y']:.{precision}f} {row[f'{i}_w']:.{precision}f} {row[f'{i}_h']:.{precision}f} {row[f'data_{i}']}\n"

    # 写入 YOLO 格式的文本文件
    with open(root_dir + "/".join(row["file_name"][:-4].split("_")) + ".txt", "w") as f:
        f.write(out)


def convert(
    json_path: str,
    csv_path: str,
    root_dir: str,
    datapoint_classes: list[int],
    n_keypoint_per_datapoint: int,
    precision: int = 6,
    keypoint_column_key: str = "dlc",
) -> pd.DataFrame:
    """将 DeepLabCut 数据集转换为 YOLO 格式

    root_dir 参数是包含训练和验证图像目录的数据集根目录路径，这些图像在 JSON 文件的 file_name 列中有标注。
    例如，file_name 列中的数据 training-images_img00001.png 和 valid-images_img001.png，root_dir 应为 "./dataset/"，
    其中包含子目录 ./dataset/training-images/ 和 ./dataset/valid-images/

    keypoint_column_key 是 CSV 中关键点的列名前缀。例如，如果所有关键点列的名字都是 "dlc"，那么该参数应设为 "dlc"。

    参数:
        json_path (str): 数据集 JSON 文件的路径
        csv_path (str): 数据集 CSV 文件的路径
        root_dir (str): 数据集根目录路径，包含训练和验证图像的目录
        datapoint_classes (list[int]): 每个数据点的类别 ID 列表
        n_keypoint_per_datapoint (int): 每个数据点的关键点数量
        precision (int, 可选): 浮点数精度，默认为 6
        keypoint_column_key (str, 可选): CSV 中关键点列的前缀，默认为 "dlc"

    返回:
        pd.DataFrame: 与数据集关联的 DataFrame

    异常:
        ValueError: 关键点不能分成 x 和 y: n_keypoint_per_datapoint 必须是 2 的倍数
        ValueError: 关键点不能分成数据点：关键点的总数量必须是 n_keypoint_per_datapoint 的倍数
        ValueError: datapoint_classes 的长度必须与数据点数量匹配
        TypeError: datapoint_classes 中的项必须是整数
    """

    # 检查关键点数量是否可以分为 x 和 y
    if n_keypoint_per_datapoint % 2 != 0:
        raise ValueError(
            "关键点不能分成 x 和 y：n_keypoint_per_datapoint 必须是 2 的倍数"
        )

    # 检查 datapoint_classes 是否为整数类型
    try:
        sum(datapoint_classes)
    except TypeError:
        raise TypeError("datapoint_classes 中的项必须是整数")

    # 合并 JSON 和 CSV 数据
    df = __merge_json_csv(json_path, csv_path, keypoint_column_key)

    # 计算关键点的数量
    n_keypoint = len([col for col in df.columns if col.startswith(keypoint_column_key)])

    # 检查关键点数量是否可以整除每个数据点的关键点数量
    if n_keypoint % n_keypoint_per_datapoint != 0:
        raise ValueError(
            "关键点不能分成数据点：关键点的总数量必须是 n_keypoint_per_datapoint 的倍数"
        )

    # 计算数据点的数量
    n_datapoint = int(n_keypoint / n_keypoint_per_datapoint)

    # 检查 datapoint_classes 的长度是否匹配数据点数量
    if len(datapoint_classes) != n_datapoint:
        raise ValueError(
            "datapoint_classes 的长度必须与数据点数量匹配"
        )

    # 归一化坐标
    df["normalized_coords"] = df.apply(
        lambda row: __norm_coords(row, keypoint_column_key, n_keypoint), axis=1
    )

    # 为每个数据点计算坐标、边界框和 YOLO 格式数据
    for i in range(n_datapoint):
        df[f"{i}_coords"] = df["normalized_coords"].apply(
            lambda coords: coords[
                n_keypoint_per_datapoint * i : n_keypoint_per_datapoint * (i + 1)
            ]
        )
        df[f"data_{i}"] = df[f"{i}_coords"].apply(
            lambda x: __format_coords(x, precision)
        )
        df[f"{i}_bbox"] = df[f"{i}_coords"].apply(__calculate_bbox)
        df[[f"{i}_x", f"{i}_y", f"{i}_w", f"{i}_h"]] = df.apply(
            lambda row: __calculate_xywh(row[f"{i}_bbox"]), axis=1, result_type="expand"
        )

    # 创建 YOLO 格式的文件
    df.apply(
        lambda row: __create_yolo(
            row, precision, root_dir, n_datapoint, datapoint_classes
        ),
        axis=1,
    )

    # 删除 keypoint_column_key 前缀的列
    df = df.drop(columns=[col for col in df.columns if col.startswith(f'{keypoint_column_key}.')])

    return df