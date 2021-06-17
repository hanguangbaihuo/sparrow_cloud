import jwt
import os
import time
import unittest

JWT_SECRET = "hard_to_guess_string"
USER_ID = 'abcedfg1234567'

# 有效的对称加密token
class MockRequest(object):
    def __init__(self):
        self.META = {"HTTP_AUTHORIZATION": self.get_token()}

    def get_token(self):
        payload = {"uid": USER_ID, 
                "app_id": "app_0000",
                "exp": int(time.time()+60*60), 
                "iat": int(time.time()), 
                "iss": "test"
            }
        return b'Tokentest '+jwt.encode(payload, JWT_SECRET, algorithm='HS256')

# 过期无效的对称加密token
class MockInvalidRequest(object):
    def __init__(self):
        self.META = {"HTTP_AUTHORIZATION": self.get_token()}

    def get_token(self):
        payload = { "uid": USER_ID, 
                "app_id": "app_0000",
                "exp": int(time.time()-100),
                "iat": int(time.time()-500),
                "iss": "test"
            }
        return b'Tokentest '+jwt.encode(payload, JWT_SECRET, algorithm='HS256')

# 有效的非对称加密token
class MockAsyRequest(object):
    def __init__(self):
        self.META = {"HTTP_AUTHORIZATION": self.get_token()}

    def get_token(self):
        payload = { "uid": USER_ID, 
                "app_id": "app_0000",
                "exp": int(time.time()+60*60), 
                "iat": int(time.time()), 
                "iss": "test"
            }
        private_key = open(os.getenv("PRIVATE_KEY_PATH")).read()
        return b'Tokentest '+jwt.encode(payload, private_key, algorithm='RS256')

# 过期无效的非对称加密token
class MockInvalidAsyRequest(object):
    def __init__(self):
        self.META = {"HTTP_AUTHORIZATION": self.get_token()}

    def get_token(self):
        payload = { "uid": USER_ID, 
                "app_id": "app_0000",
                "exp": int(time.time()-100),
                "iat": int(time.time()-500),
                "iss": "test"
            }
        private_key = open(os.getenv("PRIVATE_KEY_PATH")).read()
        return b'Tokentest '+jwt.encode(payload, private_key, algorithm='RS256')

class TestJWTMiddleware(unittest.TestCase):

    def setUp(self):
        os.environ.setdefault("JWT_SECRET", JWT_SECRET)
        os.environ.setdefault("PRIVATE_KEY_PATH", "./tests/rsa_private.pem")
        os.environ.setdefault("SC_JWT_PUBLIC_KEY_PATH", "./tests/rsa_public.pem")

    def test_normal_token(self):
        '''
        测试对称加密token
        '''
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        request = MockRequest()
        JWTMiddleware().process_request(request)
        self.assertIn("REMOTE_USER", request.META)
        self.assertIn("payload", request.META)
        self.assertIn("X-Jwt-Payload", request.META)
        self.assertEqual(USER_ID, request.META.get("REMOTE_USER"))
        self.assertIsNotNone(request.META.get("payload"))

    def test_invaid_nornal_token(self):
        '''
        测试对称加密token过期无效
        '''
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        request = MockInvalidRequest()
        JWTMiddleware().process_request(request)
        self.assertIn("REMOTE_USER", request.META)
        self.assertIn("payload", request.META)
        self.assertNotIn("X-Jwt-Payload", request.META)
        self.assertIsNone(request.META.get("REMOTE_USER"))
        self.assertIsNone(request.META.get("payload"))

    def test_asy_token(self):
        '''
        测试非对称加密
        '''
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        request = MockAsyRequest()
        JWTMiddleware().process_request(request)
        self.assertIn("REMOTE_USER", request.META)
        self.assertIn("payload", request.META)
        self.assertIn("X-Jwt-Payload", request.META)
        self.assertEqual(USER_ID, request.META.get("REMOTE_USER"))
        self.assertIsNotNone(request.META.get("payload"))

    def test_invalid_asy_token(self):
        '''
        测试过期无效的非对称加密
        '''
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        request = MockInvalidAsyRequest()
        JWTMiddleware().process_request(request)
        self.assertIn("REMOTE_USER", request.META)
        self.assertIn("payload", request.META)
        self.assertNotIn("X-Jwt-Payload", request.META)
        self.assertIsNone(request.META.get("REMOTE_USER"))
        self.assertIsNone(request.META.get("payload"))

if __name__ == '__main__':
    unittest.main()
