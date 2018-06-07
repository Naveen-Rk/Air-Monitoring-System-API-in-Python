from ams import db
import datetime






def dbinsert():
    new_ex = dbcon('', 'rknaveen22@gmail.com', 'Naveenrk22', '830065', 'Naveen', 'rk pvt ltd', 'Erode', '1', datetime.datetime.now(), datetime.datetime.now())

    db.session.add(new_ex)

    db.session.commit()

    example = dbcon.query.first()

    print(example.mobile)

    return 'hello'
