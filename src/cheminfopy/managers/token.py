# -*- coding: utf-8 -*-
# # vigenere cipher
# # https://stackoverflow.com/a/2490718/1675586


# def encode(key, string):
#     encoded_chars = []
#     for i in range(len(string)):
#         key_c = key[i % len(key)]
#         encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
#         encoded_chars.append(encoded_c)
#     encoded_string = "".join(encoded_chars)
#     return encoded_string


# def decode(key, string):
#     encoded_chars = []
#     for i in range(len(string)):
#         key_c = key[i % len(key)]
#         encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
#         encoded_chars.append(encoded_c)
#     encoded_string = "".join(encoded_chars)
#     return encoded_string


# def _should_pickle(k):
#     if "password" in k:
#         return False
#     return True


# class TokenManager:
#     def __init__(self, instance: str, username: str, password: str):
#         self.instance = instance
#         self._username = username
#         self._password = encode(password)

#     def __getstate__(self):
#         """To avoid that some user can pickle the object with the password"""
#         return dict((k, v) for (k, v) in self.__dict__.iteritems() if _should_pickle(k))

#     def get_user_token(self, rights=["read"]):
#         ...

#     def get_sample_token(self, rights=["read"]):
#         ...
