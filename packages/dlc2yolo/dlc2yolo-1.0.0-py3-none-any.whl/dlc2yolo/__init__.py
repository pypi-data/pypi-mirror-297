# Copyright 2024 Hakureirm <wbj010101@gmail.com>

"""
Convert DeepLabCut dataset to YOLO format

Quick Start:
- dlc2yolo.convert(json_path, csv_path, root_dir, datapoint_classes=[0, 1], n_keypoint_per_datapoint=30)
- dlc2yolo.convert(json_path, csv_path, root_dir, datapoint_classes=[0, 0], n_keypoint_per_datapoint=30)

============

Copyright (C) 2024 Hakureirm <wbj010101@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .__about__ import *
from .dlc2yolo import (
    convert,
)
