import requests
import re
import hashlib
import base64


def login(baseurl, username, password):
    s = requests.Session()
    r = s.get(baseurl + "html/index.html")
    csrf_tokens = grep_csrf(r.text)

    s.headers.update({
        '__RequestVerificationToken': csrf_tokens[1],
    })

    # test token on statistics api
    # r = s.get(baseurl + "api/monitoring/statistic-server")

    data = login_data(username, password, csrf_tokens[1])
    print("api/user/login")
    r = s.post(baseurl + "api/user/login", data=data)
    print(r.text)

    s.headers.update({
        '__RequestVerificationToken': r.headers["__RequestVerificationTokenone"]
    })

    return s


def enable_data(baseurl, session):
    print("api/dialup/mobile-dataswitch")
    s.post(baseurl + "api/dialup/mobile-dataswitch",
           data='<?xml version:"1.0" encoding="UTF-8"?><request><dataswitch>1</dataswitch></request>')


# 2100MHz (B1) FDD (0000000000000001) – Telstra (a handful of sites), Optus (Darwin, Tasmania)
# 1800MHz (B3) FDD (0000000000000004) – Telstra, Optus, Vodafone
# 850MHz (B5) FDD (0000000000000010) – Vodafone
# 2600MHz (B7) FDD (0000000000000040) – Optus, Telstra. (TPG have a license but have not announced plans for it.)
# 900MHz (B8) FDD (0000000000000080) – Telstra (a handful of sites, utilises spectrum previously used by 2G)
# 700MHz (B28) FDD (0000000008000000) – Telstra, Optus (switched on early in a couple of cities, will be widespread in
# 2015)
# 2300MHz (B40) TDD (0000008000000000) – Optus (Vivid wireless spectrum), NBN
# 3500MHz (B42) TDD (0000020000000000) – Optus, NBN (trials at this stage)

def change_mode(baseurl, session):
    print("api/net/net-mode")
    default_mode_data = '<?xml version="1.0" encoding="UTF-8"?><request><NetworkMode>00</NetworkMode><NetworkBand>3FFFFFFF</NetworkBand><LTEBand>8008000044</LTEBand></request>'
    test_mode_data = '<?xml version="1.0" encoding="UTF-8"?><request><NetworkMode>03</NetworkMode><NetworkBand>3FFFFFFF</NetworkBand><LTEBand>8000000000</LTEBand></request>'
    s_response = s.post(baseurl + "api/net/net-mode", data=test_mode_data)
    print(s_response.text)


def grep_csrf(html):
    pat = re.compile(r".*meta name=\"csrf_token\" content=\"(.*)\"", re.I)
    matches = (pat.match(line) for line in html.splitlines())
    return [m.group(1) for m in matches if m]


def login_data(username, password, csrf_token):
    def encrypt(text):
        m = hashlib.sha256()
        m.update(text)
        return base64.b64encode(m.hexdigest())

    password_hash = encrypt(username + encrypt(password) + csrf_token)
    return '<?xml version:"1.0" encoding="UTF-8"?><request><Username>admin</Username><Password>' + password_hash + '</Password><password_type>4</password_type></request>'


WEB = "http://192.168.8.1/"
USERNAME = "admin"
PASSWORD = "admin"

s = login(WEB, USERNAME, PASSWORD)
change_mode(WEB, s)
