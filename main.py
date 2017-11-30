#!/usr/bin/env python3

class Credentials:
    # keyring = __import__('keyring')
    import keyring
    serviceName = 'PW-login'  # __name__
    usernameMocked = 'username is also a secret'  # we store it in password field because it is kinda of secret too
    separator = '|'

    def getCredentials(self):
        credentials = self.keyring.get_password(self.serviceName, self.usernameMocked)
        if credentials == None:
            raise FileNotFoundError
        else:
            separatorPos = credentials.find(self.separator)
            username = credentials[:separatorPos]
            password = credentials[separatorPos + 1:]
            return username, password

    def saveCredentials(self, user, passw):
        return self.keyring.set_password(self.serviceName, self.usernameMocked, self.separator.join([user, passw]))


def login(username, password):
    # lets fake some SSL cert. PW login website uses a expired one. LAME.
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    import http.client
    conn = http.client.HTTPSConnection("1.1.1.1", timeout=2.5)
    payloadAlt = '&'.join(['buttonClicked=4',
                           'username=' + username,
                           'password=' + password])
    headers = {
        'connection': "keep-alive",
        'cookie': "gsScrollPos=",
        'host': "1.1.1.1",
        'origin': "http://1.1.1.1",
        'referer': "http://1.1.1.1/login.html",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "a2b860e4-11b3-ed90-bbf2-88ca925019c5"
    }
    from socket import timeout
    try:
        conn.request("POST", "/login.html", payloadAlt, headers)
        res = conn.getresponse()
        data = res.read()

        # print(data.decode("utf-8"))
        print('wysłanie żądania poprawne')
        print('czy internet ?')
        exit(0)
    except ssl.SSLError:
        print('politechnika ma gówno w sieci. nie umieją zrobić certyfikatu')
    except TimeoutError:
        raise
    except timeout:
        from sys import stderr
        print('najprawdopodobniej nie jesteś w sieci pwwifi-students. timeout łączenia ze stroną bajdiego ' + headers[
            'host'], file=stderr)
        exit(1)


def main():
    passy = Credentials()
    try:
        username, password = passy.getCredentials()
    except FileNotFoundError:
        from getpass import getpass
        username = input('zaloguj się:')
        password = input('haslo:')
        passy.saveCredentials(username, password)

    print('loguję się..')
    try:
        login(username, password)
    except Exception as e:
        raise
        print('jakiś problem. złe dane ?')


if __name__ == '__main__':
    main()
