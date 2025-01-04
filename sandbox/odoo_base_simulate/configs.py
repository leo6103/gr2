# configs.py

import configparser
import os

def read_config(file_path):
    """Đọc file cấu hình odoo.conf và trả về dictionary các giá trị."""
    config = configparser.ConfigParser()
    config.read(file_path)

    if 'options' not in config:
        raise ValueError("Missing [options] section in config file.")

    return dict(config['options'])

def get_addons_path(config):
    """Lấy giá trị addons_path từ config."""
    addons_path = config.get('addons_path')
    if not addons_path:
        raise ValueError("addons_path is not set in config.")
    return addons_path
