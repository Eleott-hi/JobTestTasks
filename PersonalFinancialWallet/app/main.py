# from app.wallet import Wallet
# import json


# from pydantic import BaseModel
from app.application import Application

# from datetime import date


# class Table(BaseModel):
#     Data: date = date.today()


if __name__ == "__main__":

    Application().run()
    # table = Table()
    # with open("data.json", "w") as f:
    #     f.write(table.model_dump_json())
