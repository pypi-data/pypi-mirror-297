import json
import os

class SettingsManager:
    """
    커맨드라인 명령어를 통해 세팅파일을 저장하는 기본 클래스
    """
    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self.settings_dict = self.load_settings()

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError as e:
                print(f"설정 파일을 읽는 중 오류 발생: {e}")
                return {}
        else:
            return {}

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as file:
                json.dump(self.settings_dict, file, indent=4)
        except IOError as e:
            print(f"설정 파일을 저장하는 중 오류 발생: {e}")
