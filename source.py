import re
import hashlib

class Site:
    def __init__(self, url_address):
        self.url = url_address
        self.register_users = list()
        self.active_users = list()

    def show_users(self):
        pass

    def register(self, user):
        if user in self.register_users:
            raise Exception('user already registered')
        self.register_users.append(user)
        return "register successful"

    def login(self, **kwargs):
        username = kwargs.get('username', '')
        email = kwargs.get('email', '')
        password = kwargs.get('password', '')
        hashed = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        users = list()
        valid_user = None
        
        if username or email:
            for user in self.register_users:
                if user.username == username or user.email == email:
                    users.append(user)
        
        if not users:
            raise Exception('invalid login')
        
        for user in users:
            if username:
                if user.username == username:
                    if user.password == hashed:
                        valid_user = user
                        break
            if email:
                if user.email == email:
                    if user.password == hashed:
                        valid_user = user
                        break
        
        if valid_user in self.active_users:
            raise Exception('user already logged in')
        
        self.active_users.append(valid_user)
        return 'login successful'
                
            
            
    def logout(self, user):
        if user in self.active_users:
            self.active_users.remove(user)
            return 'logout successful'
        raise Exception('user is not logged in')

    def __repr__(self):
        return "Site url:%s\nregister_users:%s\nactive_users:%s" % (self.url, self.register_users, self.active_users)

    def __str__(self):
        return self.url


class Account:
    def __init__(self, username, password, user_id, phone, email):
        self.username = self.username_validation(username=username)
        self.password = self.password_validation(password=password)
        self.phone = self.phone_validation(phone=phone)
        self.email = self.email_validation(email=email)
        self.user_id = self.id_validation(id=user_id)

    def set_new_password(self, password):
        self.password = self.password_validation(password)
        
    def username_validation(self, username):
        if len(re.findall(r'^[a-zA-Z]+_[a-zA-Z]+$', username)) != 1:
            raise Exception('invalid username')
        return username

    def password_validation(self, password):
        if len(password) < 8:
            raise Exception('invalid password')

        lower = any([i.islower() for i in password])
        upper = any([i.isupper() for i in password])
        digit = any([i.isdigit() for i in password])
        status = all([lower, upper, digit])
        # print(lower, upper, digit, status)
        if not status:
            raise Exception('invalid password')
        return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()


    def id_validation(self, id):
        if len(id) != 10 or not id.isdigit():
            raise Exception('invalid code melli')

        total = 0
        for digit in reversed(range(2, 11)):
            total += int(id[:-1][len(id)-digit]) * digit
        total %= 11

        if not total < 2:
            total = 11 - total

        if int(id[-1]) != total:
            raise Exception('invalid code melli')
        return id

    def phone_validation(self, phone):
        if len(phone) != 11 and len(phone) != 13:
            raise Exception('invalid phone number')

        if not phone.startswith('+989') and not phone.startswith('09'):
            raise Exception('invalid phone number')

        if phone.startswith('+98'):
            phone = phone.replace('+98', '0')

        return phone

    def email_validation(self, email):
        first_part = email[:email.find('@')]
        second_part = email[email.find('@')+1:email.find('.')]
        third_part = email[email.find('.')+1:]
        char_list = ['_', '.', '-']

        for char in first_part:
            if char not in char_list:
                if not char.isdigit():
                    if not char.islower():
                        if not char.isupper():
                            raise Exception('invalid email')

        for char in second_part:
            if char not in char_list:
                if not char.isdigit():
                    if not char.islower():
                        if not char.isupper():
                            raise Exception('invalid email')

        if 2 <= len(third_part) <= 5:
            for char in third_part:
                if not char.islower():
                    if not char.isupper():
                        raise Exception('invalid email')
        else:
            raise Exception('invalid email')

        return email

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username


def show_welcome(func):
    def wrapper(user):
        user = str(' '.join(str(user).split('_')).title())
        if len(user) > 15:
            user = user[:15] + "..."
        return func(user)
    return wrapper


def verify_change_password(func):
    def wrapper(user, old_pass, new_pass):
        password = hashlib.sha256(bytes(old_pass, 'utf-8')).hexdigest()
        if user.password == password:
            # print(user.password)
            user.set_new_password(new_pass)
            # print(user.password)
            return func(user, old_pass, new_pass)
    return wrapper


@show_welcome
def welcome(user):
    return ("welcome to our site %s" % user)


@verify_change_password
def change_password(user, old_pass, new_pass):
    return ("your password is changed successfully.")


# a = Account('Alireza_mortezaei', '@Ali2001', '4311564961', '09369947270', 'AMCoder@gmail.com')
# print(change_password(a, '@Ali2001', '@AMCoder80'))
# print(change_password(a, '@AMCoer80', '@Ali2001'))
# b = Account('Shayan_ahmdi', '@Ali2001', '4312298531', '09359947270', 'mortezaei_alireza@yahoo.com')
# s1 = Site('am80Coder.com')
# print(s1.register(a))
# print(s1.register(b))
# print(s1.register_users)
# print(s1.login(email='mortezaei_alireza@yahoo.com',username='Shayan_ahmdi', password='@Ali2001'))
# print(s1.active_users)
# print(s1.logout(b))
# print(s1.active_users)
