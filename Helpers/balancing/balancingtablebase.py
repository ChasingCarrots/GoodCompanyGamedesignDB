import json

class ColumnBase(object):
    def GetHeader(self):
        return "undefined"

    def IsEditable(self):
        return False

    def GetRowStrings(self, query):
        return []

    def SetValue(self, objID, value):
        pass

class BalancingTableBase(object):
    BalancingTableIdentifier = "base"

    def __init__(self, query):
        self.query = query
        self.columns = []

    def AddColumn(self, column):
        self.columns.append(column)

    def GetJson(self):
        data = {
            "columns": [{
                "header": "Object",
                "editable": False
            }],
            "rows": []
        }
        for obj in self.query.all():
            data["rows"].append({
                "id": obj.id,
                "columns": [str(obj)]
            })
        for column in self.columns:
            data["columns"].append({
                "header": column.GetHeader(),
                "editable": column.IsEditable()
            })
            rowIndex = 0
            for columnRow in column.GetRowStrings(self.query):
                data["rows"][rowIndex]["columns"].append(columnRow)
                rowIndex += 1

        return json.dumps(data)

    def SetValueReceived(self, columnIndex, objID, value):
        self.columns[columnIndex].SetValue(objID, value)

