import datetime
import hashlib
from cryptography.hazmat.primitives import hashes, hmac
import os
from cryptography.hazmat.backends import default_backend

#Initialize MAC generation and verification functions
def gen_mac(m, k):
    hash = hmac.HMAC(k, hashes.SHA256(), backend=default_backend())
    hash.update(m.encode())
    mac = hash.finalize()
    return mac

def ver_mac(m, k, mac):
    mac2 = gen_mac(m, k)
    return mac2 == mac

#Initialize timestamp verifying function
def ver_time(t):
    cur_t = datetime.datetime.now()
    if cur_t - t <= datetime.timedelta(minutes = 5):
        return True
    else:
        return False


#Initialize message and message timestamp
message = "The company website has not limited the number of transactions a single user or device can perform in a given period of time. The transactions/time should be above the actual business requirement, but low enough to deter automated attacks."
m_datetime = datetime.datetime.now()
m_w_timestamp = "{} {}".format(message, m_datetime)

#Initialize key
random_key = os.urandom(32)

#Generate mac
m_mac = gen_mac(m_w_timestamp, random_key)

#Verifying mac and timestamp
print("Verifying mac: ", ver_mac(m_w_timestamp, random_key, m_mac))

m_datetime2 = ' '.join(m_w_timestamp.split()[-2:])
m_datetime2 = datetime.datetime.strptime(m_datetime2, "%Y-%m-%d %H:%M:%S.%f")
print("Verifying timestamp: ", ver_time(m_datetime2))