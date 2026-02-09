import datetime
import logging
from multiprocessing import Process, Manager




def is_lucky_number(start_range, end_range, result_list):
   cnt = 0
   for i in range(start_range, end_range):
       ticket = f"{i:06d}"
       if sum(map(int, ticket[:3])) == sum(map(int, ticket[3:])):
           cnt = cnt + 1
   result_list.append(cnt)

if __name__ == "__main__":
    manager = Manager()
    results = manager.list()

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main : before creating Process")
    x1 = Process(target=is_lucky_number, args=(0, 250000, results))
    x2 = Process(target=is_lucky_number, args=(250000, 500000, results))
    x3 = Process(target=is_lucky_number, args=(500000, 750000, results))
    x4 = Process(target=is_lucky_number, args=(750000, 1000000, results))
    logging.info("Main : after running thread")
    t1 = datetime.datetime.now()

    for p in (x1, x2, x3, x4):
        p.start()

    logging.info("Main : wait for the thread to finish")
    for p in (x1, x2, x3, x4):
        p.join()

    t2 = datetime.datetime.now()
    logging.info("Main : all done")
    logging.info(f"total time spent: {t2 - t1}")

    print("TOTAL:", sum(results))
