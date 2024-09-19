#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib
import re
import shutil
from time import strftime

from pypkg.config import config as setting


class PKG:

    def __init__(self):
        self.dirname = pathlib.Path(".").absolute().name
        self.app_name = self.dirname.lower()
        self.APP_NAME = self.app_name.upper()
        self.AppName = self.app_name.title()


    @staticmethod
    def copy_template_to_apps():
        os.system(f"cp -r {setting.TPL_PATH}/* .")
        os.system(f"cp {setting.TPL_PATH}/.gitignore-tpl  .")
        os.system(f"cp {setting.TPL_PATH}/.env-tpl  .")

    def dirs(self):
        for root, _dirs, files in os.walk("."):
            for dir in _dirs:
                if "${app_name}" in dir:
                    new_dir = re.sub(
                        r"\${app_name}", self.app_name, dir
                    )
                    os.system(f"cp -r {root}/{dir} {root}/{new_dir}")

    def file(self):
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith("-tpl"):

                    if "${app_name}" in file:
                        new_file = re.sub(
                            r"\${app_name}", self.app_name, file
                        )
                        shutil.move(f"{root}/{file}", f"{root}/{new_file}")
                        file = new_file

                    if not file.endswith((".py-tpl", ".csv-tpl", ".md-tpl")):
                        continue

                    with open(f"{root}/{file}", "r") as f:
                        codes = f.readlines()
                    new_codes = []
                    for code in codes:
                        if "${APP_NAME}" in code:
                            code = re.sub(r"\${APP_NAME}", self.APP_NAME, code)
                        if "${app_name}" in code:
                            code = re.sub(r"\${app_name}", self.app_name, code)
                        if "${AppName}" in code:
                            code = re.sub(r"\${AppName}", self.AppName.replace("_", "").replace("-", ""), code)
                        if "${USER}" in code:
                            code = re.sub(r"\${USER}", setting.USERNAME, code)
                        if "${DATE}" in code:
                            code = re.sub(r"\${DATE}", strftime("%Y/%m/%d"), code)
                        if "${TIME}" in code:
                            code = re.sub(r"\${TIME}", strftime("%H:%M:%S"), code)
                        if "${FIXEDCSVTITLE}" in code:
                            code = re.sub(
                                r"\${FIXEDCSVTITLE}",
                                ",".join([i.value for i in setting.FixedCsvTitle]),
                                code,
                            )
                        new_codes.append(code)
                    with open(f"{root}/{file}", "w") as f:
                        f.writelines([i for i in new_codes])

                    shutil.move(f"{root}/{file}", f"{root}/{file[:-4]}")

if __name__ == '__main__':
    PKG().dirs()