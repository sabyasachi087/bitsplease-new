import stomp
import random
import predictor.curator as crt
import predictor.classifier as clf


class TestDataMessageListener(stomp.ConnectionListener):

    def __init__(self, name):
        self.ensembler = clf.init()
        self.name = name
        self.queue = 'gest.recg.test.queue'
        self._init_conn()        
    
    def _init_conn(self):
        self.conn = stomp.Connection()               
        self.conn.connect('admin', 'admin', wait=True)
        self.conn.subscribe(destination=self.queue, id=random.randint(1, 100), ack='auto')
        self.conn.set_listener(self.name, self)
        self.conn.start()
        
    def stop(self):
        self.conn.disconnect()

    def on_error(self, _, message):
        print('received an error "%s"' % message)

    def on_message(self, _, message):
        try:
            datas = self.transform(message)
            df = crt.toDataFrame(datas)
            self.speech(self.ensembler.predict([df]))
        except Exception as e:
            print(e)
            self.stop()
    
    def transform(self, message):
        str_data = [b.replace("\r", "").replace("\n", "").replace("'", "").split(",")\
                     for b in message.split("__")]
        return str_data
    
    def speech(self, pred):
        text = " ".join((pred[0][0]).split("_"))
        if text.strip() != 'NA':
            print('********************************************')
            print('*                %s                  *' % text)
            print('********************************************')
