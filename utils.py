import datetime, json
from models import *
from enum import IntEnum
class OPER(IntEnum):
    ADD = 1
    MODIFY = 2
    DELETE = 3
    
class OBJ(IntEnum):
    ITEM = 1
    VARIANT = 2   

def add_update(op, data, user, objtype):
    now_time = datetime.datetime.now()
    old_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
    updates = Data_Update.query.filter_by(updater=user).filter(Data_Update.update_time>old_time, Data_Update.update_time<now_time)
    if(updates.count() == 0):
        new_data = [{"op":op, "data":data, "type":objtype}]
        text = json.dumps(new_data)
        data_update = Data_Update(text)
        db.session.add(data_update)
        user.updates.append(data_update)
        db.session.commit()
    else:
        update = updates.first()
        text = update.update
        curr_data = json.loads(text)
        new_data = {"op":op, "data":data, "type":objtype}
        curr_data.append(new_data)
        update.update = json.dumps(curr_data)
        update.update_time = datetime.datetime.now()
        db.session.commit()