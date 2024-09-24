import requests
import json
import base64
from cryptography.fernet import Fernet
from typing import Optional, Tuple, Union, Dict, Any, List
from altcolor.altcolor import colored_text
import os

data_loaded: bool = False

class GitHubDatabase:
    def __init__(self, token: str, repo_owner: str, repo_name: str, branch: str = 'main') -> None:
        self.token: str = token
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.branch: str = branch
        self.headers: Dict[str, str] = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _get_file_url(self, path: str) -> str:
        return f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{path}"

    def _get_file_content(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        url: str = self._get_file_url(path)
        response: requests.Response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            file_data: Dict[str, Union[str, bytes]] = response.json()
            sha: str = file_data['sha']
            content: str = base64.b64decode(file_data['content']).decode('utf-8')
            return content, sha
        return None, None

    def read_data(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        content, sha = self._get_file_content(path)
        return content, sha

    def write_data(self, path: str, data: str, message: str = "Updated data") -> int:
        try:
            url: str = self._get_file_url(path)
            content, sha = self._get_file_content(path)
            encoded_data: str = base64.b64encode(data.encode('utf-8')).decode('utf-8')

            payload: Dict[str, Union[str, None]] = {
                "message": message,
                "content": encoded_data,
                "branch": self.branch
            }

            if sha:
                payload["sha"] = sha

            response: requests.Response = requests.put(url, headers=self.headers, json=payload)
            return response.status_code
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            return 500

    def delete_data(self, path: str, message: str = "Deleted data") -> int:
        try:
            url: str = self._get_file_url(path)
            _, sha = self._get_file_content(path)

            if sha:
                payload: Dict[str, str] = {
                    "message": message,
                    "sha": sha,
                    "branch": self.branch
                }
                response: requests.Response = requests.delete(url, headers=self.headers, json=payload)
                return response.status_code
            else:
                return 404
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            return 500

    @staticmethod
    def generate_example() -> None:
        example_code: str = """from gitbase.gitbase import GitHubDatabase, PlayerDataSystem, DataSystem
from cryptography.fernet import Fernet

# Generate an example of how to use gitbase [NOT NEEDED IF YOU ARE READING THIS]
GitHubDatabase.generate_example()

# Initialize GitHub database and encryption key
token = "your_github_token"
repo_owner = "your_repo_owner"
repo_name = "your_repo_name"
key = Fernet.generate_key()

db = GitHubDatabase(token, repo_owner, repo_name)
player_data_system = PlayerDataSystem(db, key)
data_system = DataSystem(db, key)

# Player instance with some attributes
class Player:
    def __init__(self, username, score):
        self.username = username
        self.score = score

player = Player("john_doe", 100)

# Save specific attributes of the player instance
player_data_system.save_player_data("john_doe", player, attributes=["username", "score"])

# Load player data
player_data_system.load_player_data("john_doe", player)

# Save a piece of data using a key and value pair
data_system.save_data(key="key_name", value=69)

# Load the value of a specific key by its name
key_1 = data_system.load_data(key="key_name")

# Print the value
print(key_1)

# Delete data | data_system.delete_data(key="key_name")
# Delete account | player_data_system.delete_account(username="john_doe")
"""
        with open("example_code.py", "wb") as file:
            file.write(bytes(example_code, 'UTF-8'))

class PlayerDataSystem:
    def __init__(self, db: GitHubDatabase, encryption_key: bytes) -> None:
        self.db: GitHubDatabase = db
        self.encryption_key: bytes = encryption_key
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_player_data(self, username: str, player_instance: Any, attributes: Optional[List[str]] = None) -> None:
        try:
            player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in (attributes or player_instance.__dict__.keys()) if hasattr(player_instance, var)}
            encrypted_data: bytes = self.encrypt_data(json.dumps(player_data))
            path: str = f"players/{username}.json"
            self.db.write_data(path, encrypted_data.decode('utf-8'), message=f"Saved data for {username}")
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            print(colored_text("GREEN", "Attempting to save to offline backup version."))
            self.save_offline_data(username, player_instance, attributes)

    def save_offline_data(self, username: str, player_instance: Any, attributes: Optional[List[str]] = None) -> None:
        os.makedirs("gitbase/data/players", exist_ok=True)
        
        player_data: Dict[str, Union[str, int, float]] = {var: getattr(player_instance, var) for var in (attributes or player_instance.__dict__.keys()) if hasattr(player_instance, var)}
        encrypted_data: bytes = self.encrypt_data(json.dumps(player_data))
        
        name: str = player_instance.username if player_instance.username else "example_username"
        path: str = os.path.join("gitbase/data/players", f"{name}.gitbase")
        
        try:
            with open(path, "wb") as file:
                file.write(encrypted_data)
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))

    def load_player_data(self, username: str, player_instance: Any) -> None:
        try:
            path: str = f"players/{username}.json"
            encrypted_data, _ = self.db.read_data(path)

            if encrypted_data:
                decrypted_data: str = self.decrypt_data(encrypted_data.encode('utf-8'))
                player_data: Dict[str, Union[str, int, float]] = json.loads(decrypted_data)

                for var, value in player_data.items():
                    setattr(player_instance, var, value)

                print(colored_text("GREEN", f"Data loaded and assigned for {username}"))
            else:
                print(colored_text("RED", f"No data found for {username}"))
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            print(colored_text("GREEN", "Attempting to load offline backup version."))
            self.load_offline_data(username, player_instance)

    def load_offline_data(self, username: str, player_instance: Any) -> None:
        path: str = f"gitbase/data/players/{username}.gitbase"
        
        if os.path.exists(path):
            with open(path, "rb") as file:
                encrypted_data: bytes = file.read()

            if encrypted_data:
                decrypted_data: str = self.decrypt_data(encrypted_data)
                player_data: Dict[str, Union[str, int, float]] = json.loads(decrypted_data)

                for var, value in player_data.items():
                    setattr(player_instance, var, value)

                print(colored_text("GREEN", f"Data loaded and assigned for {username}"))
            else:
                print(colored_text("RED", f"No data found for {username}"))
        else:
            print(colored_text("RED", f"Offline backup not found for {username}"))

    def delete_account(self, username: str) -> int:
        try:
            path: str = f"players/{username}.json"
            return self.db.delete_data(path, message=f"Deleted account '{username}'")
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            print(colored_text("GREEN", "Attempting to delete offline backup version."))
            self.delete_offline_data(username)

    def delete_offline_data(self, username: str) -> None:
        path: str = f"gitbase/data/players/{username}.gitbase"
        
        if os.path.exists(path):
            os.remove(path)

class DataSystem:
    def __init__(self, db: GitHubDatabase, encryption_key: bytes) -> None:
        self.db: GitHubDatabase = db
        self.encryption_key: bytes = encryption_key
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_data(self, key: str, value: Any) -> None:
        try:
            encrypted_data: bytes = self.encrypt_data(json.dumps(value))
            path: str = f"{key}.json"
            self.db.write_data(path, encrypted_data.decode('utf-8'), message=f"Saved {key}")
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))

    def load_data(self, key: str) -> Optional[Any]:
        try:
            path: str = f"{key}.json"
            encrypted_data, _ = self.db.read_data(path)

            if encrypted_data:
                decrypted_data: str = self.decrypt_data(encrypted_data.encode('utf-8'))
                return json.loads(decrypted_data)
            else:
                return None
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))

    def delete_data(self, key: str) -> int:
        try:
            path: str = f"{key}.json"
            return self.db.delete_data(path, message=f"Deleted {key}")
        except Exception as e:
            print(colored_text("RED", f"Error: {e}"))
            return 500