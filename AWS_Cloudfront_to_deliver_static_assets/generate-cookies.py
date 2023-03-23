import functools
import requests
import rsa
import datetime
from botocore.signers import CloudFrontSigner

#openssl genrsa -out private_key.pem 2048
#openssl rsa -pubout -in private_key.pem -out public_key.pem

CLOUDFRONT_RESOURCE = "<cf distrubution url>"
CLOUDFRONT_PUBLIC_KEY_ID = "<cf public key>"
CLOUDFRONT_PRIVATE_KEY = open('D:/VSCode/GitRepos/PythonHacks/AWS_Cloudfront_to_deliver_static_assets/private_key.pem','rb').read()
EXPIRES_AT = datetime.datetime.now() + datetime.timedelta(hours=1)

# load the private key
key = rsa.PrivateKey.load_pkcs1(CLOUDFRONT_PRIVATE_KEY)

# create a signer function that can sign message with the private key
rsa_signer = functools.partial(rsa.sign, priv_key=key, hash_method="SHA-1")


signer = CloudFrontSigner(CLOUDFRONT_PUBLIC_KEY_ID, rsa_signer)

policy = signer.build_policy(CLOUDFRONT_RESOURCE, EXPIRES_AT).encode("utf8")
CLOUDFRONT_POLICY = signer._url_b64encode(policy).decode("utf8")
print("CLOUDFRONT_POLICY", CLOUDFRONT_POLICY)

signature = rsa_signer(policy)
CLOUDFRONT_SIGNATURE = signer._url_b64encode(signature).decode("utf8")
print("CLOUDFRONT_SIGNATURE", CLOUDFRONT_SIGNATURE)

COOKIES = {
    "CloudFront-Policy": CLOUDFRONT_POLICY,
    "CloudFront-Signature": CLOUDFRONT_SIGNATURE,
    "CloudFront-Key-Pair-Id": CLOUDFRONT_PUBLIC_KEY_ID,
}

response = requests.get('<cf distrubution url>', cookies=COOKIES)

print(response)