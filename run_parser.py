import time
from config import UPDATE_PARSER_SLLEP_TIME
from parse.tasks import update_parser

if __name__ == '__main__':
    while True:
        try:
            update_parser()
        except Exception as e:
            print(e)
        finally:
            time.sleep(UPDATE_PARSER_SLLEP_TIME * 60)
