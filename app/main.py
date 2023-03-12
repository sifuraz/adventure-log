from db.setup import session
from db.models.user import User

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# TODO uvicorn setup


def print_hi():
    user: User = session.query(User).filter_by(username="test").first()
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {user.email}")  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
