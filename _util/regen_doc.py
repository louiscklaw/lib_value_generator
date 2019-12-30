#!/usr/bin/env python

import os,sys

TRAVIS_COMMIT_MESSAGE = os.environ['TRAVIS_COMMIT_MESSAGE']
print("regen_doc start")

print(f'TRAVIS_COMMIT_MESSAGE "{TRAVIS_COMMIT_MESSAGE}"')

print("regen_doc done")