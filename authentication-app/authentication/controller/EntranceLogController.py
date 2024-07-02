from authentication.model.EntranceLogModel import EntranceLog

class EntranceLogController:
    def __init__(self):
        pass
    
    @staticmethod
    def getEntrancesLog():
        entrances_list = EntranceLog.get_entrances_log()
        return entrances_list

    @staticmethod
    def createEntranceLog(entrance_date, full_name, card_id, authorized):
        '''
        Receive values from a request to an endpoint.
        Implement value checking, error management, response management.
        '''
        result = EntranceLog.create_entrance(entrance_date, full_name, card_id, authorized)
        
        return result