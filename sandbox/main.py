import os
import ast
from typing import List, Dict, Tuple
from odoo_base_simulate.configs import read_config, get_addons_path


def get_abs_addons_path(addons_path: str) -> str:
    """
    Chuyển đổi đường dẫn addons thành đường dẫn tuyệt đối và kiểm tra hợp lệ.
    :param addons_path: Đường dẫn tương đối hoặc tuyệt đối tới thư mục addons.
    :return: Đường dẫn tuyệt đối tới addons.
    :raises ValueError: Nếu addons_path không tồn tại hoặc không phải thư mục.
    """
    abs_addons_path = os.path.abspath(addons_path)
    if not os.path.isdir(abs_addons_path):
        raise ValueError(f"Addons path '{abs_addons_path}' is not a valid directory.")
    return abs_addons_path


def read_manifest(addon_path: str) -> Dict:
    """
    Đọc và phân tích nội dung file __manifest__.py.
    :param addon_path: Đường dẫn tuyệt đối tới module.
    :return: Dictionary chứa nội dung manifest nếu hợp lệ.
    :raises: ValueError nếu file manifest không tồn tại hoặc không hợp lệ.
    """
    manifest_path = os.path.join(addon_path, '__manifest__.py')
    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(f"Manifest file not found in module: {addon_path}")

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
            manifest_dict = ast.literal_eval(manifest_content)  # An toàn hơn so với exec
            if not isinstance(manifest_dict, dict):
                raise ValueError(f"Manifest file in {addon_path} is not a valid dictionary.")
            return manifest_dict
    except Exception as e:
        raise ValueError(f"Error reading manifest file in {addon_path}: {e}")


def find_addons_with_manifest(abs_addons_path: str) -> List[Tuple[str, Dict]]:
    """
    Duyệt qua các thư mục trong addons_path, đọc file __manifest__.py và kiểm tra nội dung.
    :param abs_addons_path: Đường dẫn tuyệt đối tới thư mục addons.
    :return: Danh sách tuple chứa tên addon và manifest dictionary.
    """
    addons = []
    for addon_name in os.listdir(abs_addons_path):
        addon_path = os.path.join(abs_addons_path, addon_name)

        if os.path.isdir(addon_path):
            try:
                # Đọc manifest file
                manifest_dict = read_manifest(addon_path)

                # Kiểm tra các trường cần thiết
                required_keys = {'name', 'version'}
                if required_keys.issubset(manifest_dict):
                    addons.append((addon_name, manifest_dict))
                else:
                    print(f"Addon '{addon_name}' is missing required keys: {required_keys - manifest_dict.keys()}")
            except Exception as e:
                print(f"Error processing addon '{addon_name}': {e}")
    return addons


def print_addons_with_manifest(addons: List[Tuple[str, Dict]]) -> None:
    """
    In danh sách các add-ons hợp lệ cùng nội dung manifest.
    :param addons: Danh sách tuple chứa tên addon và manifest dictionary.
    :return: None
    """
    if addons:
        print("\nValid addons and their manifests:")
        for addon_name, manifest in addons:
            print(f"\nAddon: {addon_name}")
            print(f"Manifest Content: {manifest}")
    else:
        print("No valid addons with manifests found.")


def main() -> None:
    """
    Hàm chính để khởi động chương trình:
    - Đọc file cấu hình.
    - Lấy đường dẫn addons_path.
    - Nạp nội dung các manifest và kiểm tra tính hợp lệ.
    - In danh sách add-ons hợp lệ và nội dung manifest.
    :return: None
    """
    config_file = 'odoo.conf'

    # Đọc file config
    try:
        config = read_config(config_file)
    except Exception as e:
        print(f"Error reading config file: {e}")
        return

    # Lấy addons_path từ config
    try:
        addons_path = get_addons_path(config)
        print(f"Addons path: {addons_path}")
    except Exception as e:
        print(f"Error retrieving addons path: {e}")
        return

    # Kiểm tra đường dẫn tuyệt đối và nạp add-ons
    try:
        abs_addons_path = get_abs_addons_path(addons_path)
        addons = find_addons_with_manifest(abs_addons_path)
        print_addons_with_manifest(addons)
    except Exception as e:
        print(f"Error processing addons: {e}")


if __name__ == "__main__":
    main()
