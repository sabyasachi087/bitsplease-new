from messaging.mq_listener import TestDataMessageListener 


def main():
    tdml = TestDataMessageListener('Test_Listener')
    input('Listener Started ........ , press enter to quit')
    tdml.stop()


if __name__ == "__main__": 
    from logger.app_logger import setup_logging
    setup_logging()
    main()