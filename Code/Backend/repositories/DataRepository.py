from os import stat
from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # Reading data

    # cocktails

    @staticmethod
    def get_total_cocktails():
        sql = "select count(cocktailId) as count FROM cocktail;"
        return Database.get_one_row(sql)

    @staticmethod
    def read_all_cocktails():
        sql = "select * from cocktail"
        return Database.get_rows(sql)

    @staticmethod
    def get_cocktail_by_id(id):
        sql = "select * from cocktail where cocktailId = %s"
        params = [id]
        return Database.get_one_row(sql,params)

    @staticmethod
    def get_all_recipes():
        sql = "select * from mix"
        return Database.get_rows(sql)

    @staticmethod
    def get_recipe_by_cocktail_id(id):
        sql = "select beverageId,volume from mix where cocktailid = %s"
        params = [id]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_recipe_by_beverage_id(id):
        sql = "select beverageId,volume from mix where beverageid = %s"
        params = [id]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_all_beverages():
        sql = "select * from beverage"
        return Database.get_rows(sql)

    @staticmethod
    def get_beverage_by_id(id):
        sql = "select * from beverage where beverageId = %s"
        params = [id]
        return Database.get_one_row(sql,params)

    @staticmethod 
    def get_cocktail_history():
        sql = "select * from cocktailhistory"
        return Database.get_rows(sql)

    @staticmethod 
    def get_cocktail_history_by_cocktail_id(id):
        sql = "select * from cocktailhistory where cocktailId = %s"
        params = [id]
        return Database.get_rows(sql,params)
    
    # devices

    @staticmethod
    def get_all_devices():
        sql = "select * from device"
        return Database.get_rows(sql)

    @staticmethod
    def get_device_by_id(id):
        sql = "select * from device where deviceId = %s"
        params = [id]
        return Database.get_one_row(sql,params)

    @staticmethod
    def get_all_actions():
        sql = "select * from action"
        return Database.get_rows(sql)

    @staticmethod
    def get_device_by_id(id):
        sql = "select * from action where actionid = %s"
        params = [id]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_device_history():
        sql = "select * from devicehistory"
        return Database.get_rows(sql)

    @staticmethod
    def get_device_history_by_device_id(id):
        sql = "select * from devicehistory where deviceId = %s"
        params = [id]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_device_history_by_action_id(id):
        sql = "select * from devicehistory where actionid = %s"
        params = [id]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_latest_rows_device_history(limit):
        sql = "select h.deviceId,d.name,h.value,d.description,d.type FROM devicehistory h join device d on h.deviceid = d.deviceid order by date desc limit %s"
        params = [limit]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_latest_rows_sensor_history(limit):
        sql = 'select h.deviceId,d.name,h.value,d.description,d.type FROM devicehistory h join device d on h.deviceid = d.deviceid where d.type = "sensor" order by date desc limit %s'
        params = [limit]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_latest_rows_actuator_history(limit):
        sql = 'select h.deviceId,d.name,h.value,d.description,d.type FROM devicehistory h join device d on h.deviceid = d.deviceid where d.type = "actuator" order by date desc limit %s'
        params = [limit]
        return Database.get_rows(sql,params)


    # Putting data

    # cocktails

    @staticmethod
    def put_cocktail_history(id, comment=None):
        sql = "insert into cocktailhistory(cocktailId,comments) values(%s,%s)"
        params = [id, comment]
        return Database.execute_sql(sql, params)

    @staticmethod
    def put_device_history(device_id,action_id=None,value=None,comment=None):
        sql = "insert into devicehistory(deviceid,actionid,value,comments) values(%s,%s,%s,%s)"
        params = [device_id,action_id,value,comment]
        return Database.execute_sql(sql, params)

    
    # updating 

    @staticmethod
    def update_volume_beverage_by_id(id,current_volume):
        sql = "update beverage set currentVolume = %s where id = %s"
        params = [id,current_volume]
        return Database.execute_sql(sql, params)