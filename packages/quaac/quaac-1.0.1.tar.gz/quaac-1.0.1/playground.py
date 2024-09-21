import datetime
from pathlib import Path

from peewee import SqliteDatabase, prefetch

from quaac import DataPoint, Equipment, User, Attachment, Document
from quaac import peewee_models as pw

# db = SqliteDatabase('test.sqlite')
u = User(name='John Doe', email='j@j.com')
# up = u._to_peewee(db)
# db.bind([pw.User, pw.Equipment, pw.DataPoint, pw.AncillaryEquipment])
# d = pw.DataPoint(
#     name='Temperature',
#     perform_datetime=datetime.datetime.now(),
#     measurement_value='1.0',
#     measurement_unit='Celsius',
#     reference_value='0.0',
#     performer=pw.User(name='John Doe', email='j@j.com').get_or_create()[0],
#     primary_equipment=pw.Equipment(name='Linear Accelerator', type='linac', serial_number='12345', manufacturer='Varian', model='TrueBeam').get_or_create()[0],
# )
# d.save()
db_path = 'test.sqlite'
db_path = Path(db_path)
sqlite_db = SqliteDatabase(database=db_path)
sqlite_db.bind(pw.ALL_MODELS)
dps = pw.DataPoint.select().where(pw.DataPoint.id == 1)
users = pw.User.select()
user_dp = prefetch(users, dps)
u = pw.User.select()

e = Equipment(name='Linear Accelerator', type='linac', serial_number='12345', manufacturer='Varian', model='TrueBeam')
anc = Equipment(name='Ancillary Equipment', type='anc', serial_number='54321', manufacturer='Catphanlabs', model='CAtphan504')
f = Attachment.from_file('requirements.txt')
d = DataPoint(name='Temperature', perform_datetime=datetime.datetime.now(), measurement_value=1.0, measurement_unit='Celsius', reference_value=2, performer=u, primary_equipment=e, attachments=[f], ancillary_equipment=[anc])
doc = Document(version='1.0', datapoints=[d])
doc.to_sqlite('test.sqlite')
# dj = doc.model_dump(mode='json')
ttt = 1
