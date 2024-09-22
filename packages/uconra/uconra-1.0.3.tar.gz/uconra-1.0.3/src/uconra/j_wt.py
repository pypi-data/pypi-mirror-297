import jwt
import datetime


class JWT:
    """
    The Following is a basic JWT token creation Object.
    It only uses an email, key, and an expiration date of a day.
    The expiration date has been set to 1 day.
    It can be changed and modified as desired

    The Object is used to encrypt sesetive data with Jason Web Token (JWT)


    """
    def __init__(self):
        pass

    def generate_jwt_token(self, email=None, key=None):
        self.email = email
        self.key = key
        payload_data = {
            'email': f'{self.email}',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(
            payload=payload_data,
            key=self.key,

        )
        self.token = token
        return self.token

    def decode_jwt_token(self, encoded_token):
        self.encoded_token = encoded_token

        decode_payload_data = jwt.decode(
            jwt=self.encoded_token,
            options={"verify_signature": True},
            key=self.key,
            algorithms=["HS256"],
        )
        self.decoded_payload_data = decode_payload_data
        return self.decoded_payload_data

if __name__ == '__main__':

    token = JWT()

    login_token = token.generate_jwt_token('cody@gmail.com', key='3uihjdskdpeisjdjfl')

    print(f"encoded jwt token : {login_token}")

    decode_login_token = token.decode_jwt_token(login_token)

    print(decode_login_token['email'])

    print(f"decoded jwt token : {decode_login_token}")
