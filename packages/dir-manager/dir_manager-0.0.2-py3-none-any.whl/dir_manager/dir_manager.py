import os
import logging
import shutil
from datetime import datetime
from typing import Optional

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_base_dir_path() -> str:
    # 환경 변수에서 BASE_DIR을 가져오며, 기본값을 설정
    BASE_DIR = os.getenv("BASE_DIR", "C:/work/send")
    return BASE_DIR


def create_folder(folder_path: str) -> None:
    """
    주어진 경로에 폴더를 생성합니다. 폴더가 이미 존재하면 예외 없이 진행됩니다.

    Args:
        folder_path (str): 생성할 폴더의 경로
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        logging.info(f"폴더가 생성되었거나 이미 존재합니다: {folder_path}")
    except OSError as e:
        logging.error(f"폴더 생성 중 오류가 발생했습니다: {e}")
        raise


def get_base_path(dir_name: Optional[str] = None) -> str:
    """
    현재 연도와 월을 포함하는 기본 경로를 생성하고 반환합니다.
    dir_name이 None일 경우 기본 경로는 BASE_DIR/{year}/{month} 형식이 됩니다.

    Args:
        dir_name (Optional[str]): 생성할 디렉토리 이름 (기본값: None)

    Returns:
        str: 생성된 기본 경로
    """
    current_date = datetime.now()
    current_year = current_date.year
    current_month = f"{current_date.month:02}"

    BASE_DIR = get_base_dir_path()

    # 리스트 기반으로 동적 경로 생성
    path_parts = [BASE_DIR, str(current_year), current_month]
    if dir_name:
        path_parts.append(dir_name)

    base_dir_path = os.path.join(*path_parts)

    # 디렉토리 생성
    create_folder(base_dir_path)

    return base_dir_path

def remove_folder(folder_path: str) -> None:
    """
    주어진 경로의 폴더를 삭제합니다.
    """
    try:
        os.rmdir(folder_path)
        logging.info(f"폴더가 삭제되었습니다: {folder_path}")
    except OSError as e:
        logging.error(f"폴더 삭제 중 오류가 발생했습니다: {e}")
        raise

def list_directories(base_path: str) -> list:
    """
    주어진 경로 아래의 모든 디렉토리 목록을 반환합니다.
    """
    try:
        directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        logging.info(f"디렉토리 목록을 가져왔습니다: {directories}")
        return directories
    except OSError as e:
        logging.error(f"디렉토리 목록을 가져오는 중 오류가 발생했습니다: {e}")
        return []

def move_folder(src_path: str, dest_path: str) -> None:
    """
    폴더를 src_path에서 dest_path로 이동시킵니다.
    """
    try:
        os.rename(src_path, dest_path)
        logging.info(f"폴더가 이동되었습니다: {src_path} -> {dest_path}")
    except OSError as e:
        logging.error(f"폴더 이동 중 오류가 발생했습니다: {e}")
        raise

def copy_folder(src_path: str, dest_path: str) -> None:
    """
    폴더를 src_path에서 dest_path로 복사합니다.
    """
    try:
        shutil.copytree(src_path, dest_path)
        logging.info(f"폴더가 복사되었습니다: {src_path} -> {dest_path}")
    except OSError as e:
        logging.error(f"폴더 복사 중 오류가 발생했습니다: {e}")
        raise

def delete_file(file_path: str) -> None:
    """
    파일을 삭제합니다.
    """
    try:
        os.remove(file_path)
        logging.info(f"파일이 삭제되었습니다: {file_path}")
    except OSError as e:
        logging.error(f"파일 삭제 중 오류가 발생했습니다: {e}")
        raise

def clean_directory(directory_path: str) -> None:
    """
    주어진 디렉토리 안의 모든 파일과 폴더를 삭제합니다.
    """
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 파일이나 심볼릭 링크 삭제
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 디렉토리 삭제
        logging.info(f"디렉토리 정리가 완료되었습니다: {directory_path}")
    except OSError as e:
        logging.error(f"디렉토리 정리 중 오류가 발생했습니다: {e}")
        raise

def get_directory_size(directory_path: str) -> int:
    """
    주어진 디렉토리의 총 크기(바이트 단위)를 반환합니다.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    logging.info(f"디렉토리 크기: {total_size} bytes")
    return total_size


def find_files_by_extension(directory_path: str, extension: str) -> list:
    """
    주어진 디렉토리 내에서 특정 확장자를 가진 파일 목록을 반환합니다.
    Args:
        directory_path (str): 탐색할 디렉토리 경로
        extension (str): 파일 확장자 (예: ".txt", ".csv")

    Returns:
        list: 해당 확장자의 파일 목록
    """
    matched_files = []
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:

            if filename.endswith(extension):
                matched_files.append(os.path.join(dirpath, filename))

    logging.info(f"'{extension}' 확장자를 가진 파일 {len(matched_files)}개를 찾았습니다.")
    return matched_files


def backup_directory(src_path: str, backup_path: str) -> None:
    """
    src_path의 디렉토리를 backup_path로 백업합니다.
    """
    try:
        if os.path.exists(backup_path):
            logging.error(f"백업 경로가 이미 존재합니다: {backup_path}")
            raise FileExistsError(f"백업 경로가 이미 존재합니다: {backup_path}")

        shutil.copytree(src_path, backup_path)
        logging.info(f"디렉토리가 백업되었습니다: {src_path} -> {backup_path}")
    except OSError as e:
        logging.error(f"디렉토리 백업 중 오류가 발생했습니다: {e}")
        raise


import filecmp


def compare_directories(dir1: str, dir2: str) -> dict:
    """
    두 디렉토리의 차이점을 비교합니다.

    Returns:
        dict: 서로 다른 파일 목록을 포함한 사전 (예: 'diff_files', 'only_in_dir1', 'only_in_dir2')
    """
    comparison = filecmp.dircmp(dir1, dir2)
    diff = {
        'diff_files': comparison.diff_files,
        'only_in_dir1': comparison.left_only,
        'only_in_dir2': comparison.right_only
    }

    logging.info(f"디렉토리 비교 결과: {diff}")
    return diff
