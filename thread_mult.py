import logging
import threading
import time

def is_lucky_number(ticket_number: str):
    if len(ticket_number) != 6 or not ticket_number.isdigit():
        return "invalid ticket number"

    left = sum(map(int, ticket_number[:3]))
    right = sum(map(int, ticket_number[3:]))

    if left == right:
        print(f"{ticket_number} is lucky number")
    else:
        print(f"{ticket_number} is common number")



if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

logging.info("Main : before creating thread")
x = threading.Thread(target=is_lucky_number, args=("123042",))
logging.info("Main : after running thread")
x.start()
x.join()
logging.info("Main : all done")