import time
from worker.tasks import update_parser

if __name__ == '__main__':
    while True:
        try:
            update_parser()
        except Exception as e:
            print(e)
        finally:
            time.sleep(5 * 60)