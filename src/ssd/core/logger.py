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

    def save_log(self, log):
        root_folder = self.find_git_root()
        log_folder = os.path.join(root_folder, "log")
        log_file_path = os.path.join(log_folder, "latest.log")
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


def test_qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq():
    logger1 = Logger()
    logger2 = Logger()

    logger1.print("Logger 1 is logging.")
    logger2.print("Logger 2 is logging.")


if __name__ == "__main__":
    test_qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq()
