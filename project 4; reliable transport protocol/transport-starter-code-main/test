#!/usr/bin/env python3

import os
import subprocess
import sys
import re

SENDER_EXECUTABLE_NAME = "3700send"
RECEIVER_EXECUTABLE_NAME = "3700recv"
RUN_SCRIPT_NAME = "run"
CONFIG_DIR = "configs"

def die(message):
  print("ERROR: %s" % message)
  sys.exit(-1)

def get_files():
  if not os.path.exists(SENDER_EXECUTABLE_NAME):
    die("Could not find sender program '%s'" % SENDER_EXECUTABLE_NAME)

  if not os.access(SENDER_EXECUTABLE_NAME, os.X_OK):
    die("Could not execute sender program '%s'" % SENDER_EXECUTABLE_NAME)

  if not os.path.exists(RECEIVER_EXECUTABLE_NAME):
    die("Could not find receiver program '%s'" % RECEIVER_EXECUTABLE_NAME)

  if not os.access(RECEIVER_EXECUTABLE_NAME, os.X_OK):
    die("Could not execute receiver program '%s'" % RECEIVER_EXECUTABLE_NAME)

  if not os.path.exists(RUN_SCRIPT_NAME):
    die("Could not find simulator '%s'" % RUN_SCRIPT_NAME)

  if not os.access(RUN_SCRIPT_NAME, os.X_OK):
    die("Could not execute simulator '%s'" % RUN_SCRIPT_NAME)


get_files()

def runTest(config):
  print("%s" % ("Test: %s" % (config)).ljust(60, ' '), end='', flush=True)

  result = subprocess.check_output([os.path.join(os.getcwd(), RUN_SCRIPT_NAME), os.path.join(CONFIG_DIR, config)]).decode('utf-8')
  pattern = re.compile(r'Success!  Data was transmitted correctly', re.DOTALL)
  m = re.search(pattern, result)
  if m:
    print("[PASS]")
  else:
    print("[FAIL]")
    print(result)

runTest("1-1-basic.conf")
runTest("1-2-normal.conf")
runTest("2-1-duplicates.conf")
runTest("3-1-jitter.conf")
runTest("3-2-more-jitter.conf")
runTest("4-1-drops.conf")
runTest("4-2-more-drops.conf")
runTest("5-1-mangle.conf")
runTest("5-2-more-mangle.conf")
runTest("6-1-low-latency.conf")
runTest("6-2-medium-latency.conf")
runTest("6-3-high-latency.conf")
runTest("7-1-low-bandwidth.conf")
runTest("7-2-medium-bandwidth.conf")
runTest("7-3-high-bandwidth.conf")
runTest("8-1-intermediate-1.conf")
runTest("8-2-intermediate-2.conf")
runTest("8-3-advanced.conf")
