import datetime

class dbcon(db.Model):
    __tablename__  = 'user'
    user_no = db.Column('USER_NO', db.INTEGER, primary_key=True, nullable=False)
    email = db.Column('USER_EMAIL_ID', db.String(50), nullable=False)
    password = db.Column('USER_PASSWORD', db.String(32), nullable=False)
    mobile = db.Column('USER_MOBILE', db.INTEGER, nullable=False)
    username = db.Column('USER_NAME', db.String(30), nullable=False)
    user_company_name = db.Column('USER_COMPANY_NAME', db.String(30), nullable=False)
    user_company_address = db.Column('USER_COMPANY_ADDRESS', db.String(50), nullable=False)
    user_active = db.Column('USER_ACTIVE', db.INTEGER, nullable=False)
    user_create_ts = db.Column('USER_CREATE_TS', db.DATETIME, nullable=False, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    user_update_ts = db.Column('USER_UPDATE_TS', db.DATETIME, default=datetime.datetime.now, nullable=False)

    def __init__(self, user_no, email, password, mobile, username, user_company_name, user_company_address, user_active, user_create_ts, user_update_ts):
        self.user_no = user_no
        self.email = email
        self.password = password
        self.mobile = mobile
        self.username = username
        self.user_company_name = user_company_name
        self.user_company_address = user_company_address
        self.user_active = user_active
        self.user_create_ts = user_create_ts
        self.user_update_ts = user_update_ts
