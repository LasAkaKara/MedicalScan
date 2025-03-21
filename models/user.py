class User:
    def __init__(self, email, password=None, is_verified=False, is_active=True):
        self.email = email
        self.password = password
        self.is_verified = is_verified
        self.is_active = is_active
        self.verification_code = None
        self.code_expiry = None
        self.last_login = None
        self.full_name = None
        self.phone = None

    @staticmethod
    def from_db_row(row):
        if not row:
            return None
        user = User(row[1])  # email
        user.is_verified = bool(row[3])
        user.is_active = bool(row[4])
        user.verification_code = row[5]
        user.code_expiry = row[6]
        user.last_login = row[8]
        user.full_name = row[9]
        user.phone = row[10]
        return user 