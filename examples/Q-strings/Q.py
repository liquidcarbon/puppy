import duckdb
import pandas as pd
from time import time

url = "https://raw.githubusercontent.com/liquidcarbon/chembiodata/main/isotopes.csv"
isotopes = pd.read_csv(url)
assert isotopes.shape == (354, 4)
assert duckdb.sql("SELECT * FROM isotopes").shape == isotopes.shape

class Q(str):
    """Query string that reads from templates and runs queries."""

    def __new__(cls, string, file=False, **kwargs):
        if file:
            with open(string, "r") as f:
                file_content = f.read()
            return cls(file_content, **kwargs)
        q_string = str.__new__(cls, string.format(**kwargs))
        q_string.template = string
        q_string.kwargs = kwargs
        return q_string

    def timer(func):
        def wrapper(self, *args, **kwargs):
            self.start = time()
            result = func(self, *args, **kwargs)
            self.time = round(time() - self.start, 4)
            return result
        return wrapper

    @timer
    def run(self):
        try:
            return duckdb.sql(self)
        except Exception as e:
            # log.error(e)
            return {"error": [str(e), repr(type(e))]}

    def df(self) -> pd.DataFrame:
        result = self.run()
        if isinstance(result, dict) and "error" in result:
            result_df = pd.DataFrame(result, index=["message", "type"])
        else:
            result_df = result.df()
            self.rows, self.cols = result_df.shape
            msg = f"{self.rows} rows x {self.cols} cols in {self.time} sec"
            print(msg)  # TODO: change to log.info(msg)
            result_df.q = self
        return result_df