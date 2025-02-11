from api import IdealistaClient, USER, PASSWORD

ic = IdealistaClient()
s = ic.start()
e = ic.exists(USER)
if e:
    l = ic.login(USER, PASSWORD)
    print(l)
