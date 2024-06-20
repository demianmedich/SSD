import datetime
import inspect


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def print(self, message):
        current_time = datetime.datetime.now().strftime("[%Y.%m.%d %H:%M:%S]")
        len_function = 30
        call = inspect.stack()[1]
        function_name = call.function
        function_name = function_name[:len_function]
        print(f"{current_time} {function_name.center(len_function)+'()'} : {message}")


def test_qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq():
    logger1 = Logger()
    logger2 = Logger()

    logger1.print("Logger 1 is logging.")
    logger2.print("Logger 2 is logging.")


if __name__ == "__main__":
    test_qqq()
