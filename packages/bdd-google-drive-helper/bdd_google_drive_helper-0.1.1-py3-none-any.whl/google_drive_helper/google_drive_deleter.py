# google_drive_helper/google_drive_deleter.py
from google_drive_helper.src.auth import AuthManager
from google_drive_helper.src.drive_manager import DriveManager
from google_drive_helper.src.file_deleter import FileDeleter


class GoogleDriveDeleter(AuthManager, DriveManager, FileDeleter):
    def __init__(
        self, credentials_json="credentials.json", credentials_pickle="token.pickle"
    ):
        # 初始化 AuthManager 並取得認證
        AuthManager.__init__(self, credentials_json, credentials_pickle)
        # 初始化 DriveManager 並創建 Drive 服務
        DriveManager.__init__(self, self.creds)
        # 初始化 FileDeleter 並準備好刪除服務
        FileDeleter.__init__(self, self.drive_service)

    def delete_files_by_date(self, drive_name, folder_path, target_date):
        """整合方法：列出共用雲端硬碟、找到目標資料夾並刪除指定日期的檔案"""
        drive_id = self.list_shared_drives(drive_name)
        if drive_id:
            target_folder_id = self.find_folder_by_path(drive_id, folder_path)
            print(f"Target folder ID: {target_folder_id}")
            if target_folder_id:
                self.delete_files_by_date_in_folder(target_folder_id, target_date)
            else:
                print("Target folder not found or inaccessible.")
        else:
            print("Shared drive not found.")
