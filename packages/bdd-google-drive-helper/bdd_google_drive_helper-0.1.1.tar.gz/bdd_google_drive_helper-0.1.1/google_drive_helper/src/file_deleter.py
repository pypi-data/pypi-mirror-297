from datetime import datetime


class FileDeleter:
    def __init__(self, drive_service):
        self.drive_service = drive_service

    def delete_files_by_date_in_folder(self, folder_id, target_date):
        """刪除指定資料夾中指定日期的檔案"""
        query = f"'{folder_id}' in parents"
        try:
            results = (
                self.drive_service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, createdTime)",
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                )
                .execute()
            )
            print(f"Query results: {results}") 
        except Exception as e:
            print(f"Error retrieving files: {e}")
            return

        files = results.get("files", [])
        if not files:
            print("No files found in the folder.")
            return

        target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        print(f"Target date: {target_date_obj}")

        for file in files:
            created_time = file["createdTime"]
            try:
                created_date_obj = datetime.strptime(
                    created_time, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).date()
            except ValueError:
                created_date_obj = datetime.strptime(
                    created_time, "%Y-%m-%dT%H:%M:%S.%f%z"
                ).date()
            print(
                f"File: {file['name']}, Created Time: {created_time}, Created Date: {created_date_obj}"
            )
            if created_date_obj == target_date_obj:
                print(f"Moving file '{file['name']}' to trash with ID: {file['id']}")
                try:
                    self.drive_service.files().update(
                        fileId=file["id"],
                        body={"trashed": True},
                        supportsAllDrives=True
                    ).execute()
                    print(f"File '{file['name']}' moved to trash successfully.")
                except Exception as e:
                    print(f"Error moving file '{file['name']}' to trash: {e}")
