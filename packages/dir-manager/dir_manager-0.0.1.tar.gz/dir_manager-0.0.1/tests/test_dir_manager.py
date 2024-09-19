import shutil
import unittest
import os
from unittest import mock
from datetime import datetime
from dir_manager.dir_manager import get_base_path, create_folder, remove_folder, list_directories, move_folder, \
    copy_folder, delete_file, clean_directory, get_directory_size, find_files_by_extension, backup_directory, \
    compare_directories


class TestDirectoryFunctions(unittest.TestCase):
    def setUp(self):
        """각 테스트마다 실행되는 설정 함수. 임시 폴더 생성."""
        self.test_dir = "/tmp/test_directory"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """각 테스트가 끝난 후 실행되는 정리 함수. 임시 폴더 삭제."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @mock.patch.dict(os.environ, {"BASE_DIR": "/Temp"})
    def test_get_base_path_without_dir_name(self):
        # dir_name이 None일 경우
        base_path = get_base_path()
        current_date = datetime.now()
        expected_path = os.path.join("/Temp", str(current_date.year), f"{current_date.month:02}")

        self.assertEqual(base_path, expected_path)
        self.assertTrue(os.path.exists(base_path))

    @mock.patch.dict(os.environ, {"BASE_DIR": "/Temp"})
    def test_get_base_path_with_custom_dir(self):
        # dir_name이 있을 경우
        base_path = get_base_path("custom_dir")
        current_date = datetime.now()
        expected_path = os.path.join("/Temp", str(current_date.year), f"{current_date.month:02}", "custom_dir")

        self.assertEqual(base_path, expected_path)
        self.assertTrue(os.path.exists(base_path))

    @mock.patch.dict(os.environ, {"BASE_DIR": "/Temp"})
    def test_create_folder_existing_directory(self):
        # 이미 존재하는 디렉토리일 경우
        test_dir = "/Temp"
        os.makedirs(test_dir, exist_ok=True)
        create_folder(test_dir)  # 예외 발생 없이 진행됨

        self.assertTrue(os.path.exists(test_dir))

    def test_remove_folder(self):
        # 테스트용 임시 폴더 생성
        test_folder = "/tmp/test_remove_folder"
        os.makedirs(test_folder, exist_ok=True)

        # 폴더가 정상적으로 생성되었는지 확인
        self.assertTrue(os.path.exists(test_folder))

        # 폴더 삭제
        remove_folder(test_folder)

        # 폴더가 삭제되었는지 확인
        self.assertFalse(os.path.exists(test_folder))

    def test_list_directories(self):
        # 테스트용 디렉토리와 하위 디렉토리 생성
        base_folder = "/tmp/test_list_directories"
        sub_folder_1 = os.path.join(base_folder, "subdir1")
        sub_folder_2 = os.path.join(base_folder, "subdir2")

        os.makedirs(sub_folder_1, exist_ok=True)
        os.makedirs(sub_folder_2, exist_ok=True)

        # 디렉토리 목록 가져오기
        directories = list_directories(base_folder)

        # 디렉토리 목록에 하위 디렉토리가 포함되어 있는지 확인
        self.assertIn("subdir1", directories)
        self.assertIn("subdir2", directories)

    def test_move_folder(self):
        # 테스트용 임시 폴더 생성
        src_folder = "/tmp/test_move_folder"
        dest_folder = "/tmp/test_moved_folder"
        os.makedirs(src_folder, exist_ok=True)

        # 폴더가 정상적으로 생성되었는지 확인
        self.assertTrue(os.path.exists(src_folder))

        # 폴더 이동
        move_folder(src_folder, dest_folder)

        # 폴더가 이동되었는지 확인
        self.assertFalse(os.path.exists(src_folder))
        self.assertTrue(os.path.exists(dest_folder))

    def test_copy_folder(self):
        # 테스트용 임시 폴더 및 하위 파일 생성
        src_folder = "/tmp/test_copy_folder"
        dest_folder = "/tmp/test_copied_folder"
        os.makedirs(src_folder, exist_ok=True)

        with open(os.path.join(src_folder, "testfile.txt"), "w") as f:
            f.write("This is a test file.")

        # 폴더 복사
        copy_folder(src_folder, dest_folder)

        # 원본 폴더와 복사된 폴더가 모두 존재하는지 확인
        self.assertTrue(os.path.exists(src_folder))
        self.assertTrue(os.path.exists(dest_folder))
        self.assertTrue(os.path.exists(os.path.join(dest_folder, "testfile.txt")))

    def test_delete_file(self):
        # 테스트용 임시 파일 생성
        test_file = "/tmp/test_delete_file.txt"
        with open(test_file, "w") as f:
            f.write("This file will be deleted.")

        # 파일이 생성되었는지 확인
        self.assertTrue(os.path.exists(test_file))

        # 파일 삭제
        delete_file(test_file)

        # 파일이 삭제되었는지 확인
        self.assertFalse(os.path.exists(test_file))

    def test_clean_directory(self):
        """clean_directory 함수 테스트."""
        # 임시 파일 생성
        file_path = os.path.join(self.test_dir, "temp_file.txt")
        with open(file_path, "w") as f:
            f.write("Temporary file content")

        # 디렉토리 내 파일 확인
        self.assertTrue(os.path.exists(file_path))

        # 디렉토리 정리
        clean_directory(self.test_dir)

        # 디렉토리가 비워졌는지 확인
        self.assertEqual(len(os.listdir(self.test_dir)), 0)

    def test_get_directory_size(self):
        """get_directory_size 함수 테스트."""
        # 임시 파일 생성
        file_path = os.path.join(self.test_dir, "temp_file.txt")
        with open(file_path, "w") as f:
            f.write("Temporary file content")

        # 파일 크기 확인
        expected_size = os.path.getsize(file_path)
        dir_size = get_directory_size(self.test_dir)

        self.assertEqual(dir_size, expected_size)

    def test_find_files_by_extension(self):
        """find_files_by_extension 함수 테스트."""
        # 임시 파일 생성
        file1 = os.path.join(self.test_dir, "file1.txt")
        file2 = os.path.join(self.test_dir, "file2.csv")
        file3 = os.path.join(self.test_dir, "file3.txt")

        with open(file1, "w") as f1, open(file2, "w") as f2, open(file3, "w") as f3:
            f1.write("File 1 content")
            f2.write("File 2 content")
            f3.write("File 3 content")

        # .txt 파일 목록 확인
        txt_files = find_files_by_extension(self.test_dir, ".txt")

        self.assertEqual(len(txt_files), 2)
        self.assertIn(file1, txt_files)
        self.assertIn(file3, txt_files)

    def test_backup_directory(self):
        """backup_directory 함수 테스트."""
        # 임시 파일 생성
        backup_dir = "/tmp/backup_directory"
        file_path = os.path.join(self.test_dir, "temp_file.txt")
        with open(file_path, "w") as f:
            f.write("Temporary file content")

        # 디렉토리 백업
        backup_directory(self.test_dir, backup_dir)

        # 백업 디렉토리가 존재하는지 확인
        self.assertTrue(os.path.exists(backup_dir))
        self.assertTrue(os.path.exists(os.path.join(backup_dir, "temp_file.txt")))

        # 백업 완료 후 정리
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)

    def test_compare_directories(self):
        """compare_directories 함수 테스트."""
        # 첫 번째 디렉토리 생성
        dir1 = os.path.join(self.test_dir, "dir1")
        dir2 = os.path.join(self.test_dir, "dir2")
        os.makedirs(dir1, exist_ok=True)
        os.makedirs(dir2, exist_ok=True)

        # 각각 다른 파일 생성
        with open(os.path.join(dir1, "file1.txt"), "w") as f1, open(os.path.join(dir2, "file2.txt"), "w") as f2:
            f1.write("Content of file 1")
            f2.write("Content of file 2")

        # 두 디렉토리 비교
        diff = compare_directories(dir1, dir2)

        self.assertIn("file1.txt", diff['only_in_dir1'])
        self.assertIn("file2.txt", diff['only_in_dir2'])

if __name__ == "__main__":
    unittest.main()
