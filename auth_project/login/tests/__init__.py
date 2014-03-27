import unittest


def suite():
    return unittest.TestLoader().discover("login.tests", pattern="*.py")
