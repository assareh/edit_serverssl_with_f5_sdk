''' Example of how to edit Server SSL Profiles with the F5 Python SDK '''

from f5.bigip import ManagementRoot

# Connect to the BigIP
MGMT = ManagementRoot("10.1.1.138", "admin", "admin")

CIPHER_EDIT_STRING = "!DHE"


# create a bunch of serverssl profiles
for i in range(0, 100):
    profile_name = "andy-" + str(i) + "-serverssl"
    try:
        profile = MGMT.tm.ltm.profile.server_ssls.server_ssl.create(\
        name=profile_name, \
        partition='Common', \
        ciphers='!SSLv2:!EXPORT:ECDHE+AES-GCM:ECDHE+AES:RSA+AES-GCM:RSA+AES:ECDHE+3DES:RSA+3DES:-MD5:-SSLv3:-RC4')
    except Exception as exception:
        print "Error '{0}' occured. Arguments {1}.".format(exception.message, exception.args)


# get all of the serverssl profiles
print "\nAll serverssl profiles on the BIG-IP:\
       \n-------------------------------------"

# instantiate
SERVERSSL_COLLECTION = MGMT.tm.ltm.profile.server_ssls.get_collection()
SERVERSSL_PROFILES = MGMT.tm.ltm.profile.server_ssls

for profile in SERVERSSL_COLLECTION:
    print profile.name, profile.ciphers


# edit the cipher string
print "\nNow attempting to patch all serverssl profiles on the BIG-IP:\
       \n-------------------------------------------------------------"

for profile in SERVERSSL_COLLECTION:

    # verify it needs patching
    if profile.ciphers.find(CIPHER_EDIT_STRING) < 0:
        profile.ciphers = profile.ciphers + ":" + CIPHER_EDIT_STRING
        try:
            profile.update()
            print profile.name, profile.ciphers
        except Exception as exception:
            print "Error '{0}' occured. Arguments {1}.".format(exception.message, exception.args)

    else:
        print profile.name, "skipped"
