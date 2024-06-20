import datetime
import inspect
import os


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            root_folder = cls.find_git_root()
            log_folder = os.path.join(root_folder, "log")
            os.makedirs(log_folder, exist_ok=True)
        return cls._instance

    @staticmethod
    def find_git_root():
        current_dir = os.getcwd()
        while not os.path.exists(os.path.join(current_dir, ".git")):
            current_dir = os.path.dirname(current_dir)
            if current_dir == os.path.dirname(current_dir):
                raise RuntimeError("Git root not found.")
        return current_dir

    def create_latest_logfile(self, log_file_path):
        try:
            with open(log_file_path, "w") as f:
                f.write("Initial content if needed")
            print(f"Created log file: {log_file_path}")
        except IOError as e:
            print(f"Failed to create log file: {e}")

    def check_latest_log_size(self, log_file_path):
        if not os.path.exists(log_file_path):
            self.create_latest_logfile(log_file_path)
        log_file_size = os.path.getsize(log_file_path)
        log_file_size_kb = log_file_size / 1024
        if log_file_size_kb > 10:
            return True
        return False

    def check_until_log_file_existence(self, log_folder):
        if not os.path.exists(log_folder):
            raise FileNotFoundError(f"Log folder '{log_folder}' not found.")
        files = os.listdir(log_folder)
        for file in files:
            if file.startswith("until") and file.endswith(".log"):
                return os.path.join(log_folder, file)
        return None

    def rename_latest_log(self, log_file_path):
        dir_name, old_file_name = os.path.split(log_file_path)
        current_time = datetime.datetime.now()
        new_file_name = f"until_{current_time.strftime('%Y%m%d_%Hh_%Mm_%Ss')}.log"
        new_file_path = os.path.join(dir_name, new_file_name)
        os.rename(log_file_path, new_file_path)
        return new_file_path

    def change_extension_to_zip(self, log_file_path):
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"File '{log_file_path}' not found.")
        dir_name, old_file_name = os.path.split(log_file_path)
        file_name, extension = os.path.splitext(old_file_name)
        new_file_path = os.path.join(dir_name, file_name + ".zip")
        os.rename(log_file_path, new_file_path)
        return new_file_path

    def save_log(self, log):
        root_folder = self.find_git_root()
        log_folder = os.path.join(root_folder, "log")
        log_file_path = os.path.join(log_folder, "latest.log")
        if self.check_latest_log_size(log_file_path):
            until_file_path = self.check_until_log_file_existence(log_folder)
            if until_file_path:
                self.change_extension_to_zip(until_file_path)
            self.rename_latest_log(log_file_path)
            print("OVER")

        with open(log_file_path, "a") as file:
            file.write(log + "\n")
            print(log)

    def print(self, message):
        current_time = datetime.datetime.now().strftime("[%Y.%m.%d %H:%M:%S]")
        len_function = 30
        call = inspect.stack()[1]
        function_name = call.function
        function_name = function_name[:len_function] + "()"
        log = f"{current_time} {function_name.center(len_function)} : {message}"
        self.save_log(log)


def qqq_q():
    logger1 = Logger()
    logger2 = Logger()

    logger1.print("Logger 1 is logging.")
    logger2.print("Logger 2 is logging.")


if __name__ == "__main__":
    qqq_q()
    qqq_q()
