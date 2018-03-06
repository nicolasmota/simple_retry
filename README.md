# Simple retry

[![Build Status](https://travis-ci.org/nicolasmota/simple_retry.svg?branch=master)](https://travis-ci.org/nicolasmota/simple_retry)
[![codecov](https://codecov.io/gh/nicolasmota/simple_retry/branch/master/graph/badge.svg)](https://codecov.io/gh/nicolasmota/simple_retry)

Simple retry is a lib that allows you to re-execute functions based on throwing exceptions

## Installing
```
pip install simple-retry
```

## Simple usage

To use the lib you just import the decorator and add on top of the function that you want to retry
```
import requests

from simple_retry.decorators import retry

@retry(Except=requests.RequestException, retries=5, delay=1)
def func():
    response = requests.get('http://fooo.bar')
    response.raise_for_status()
```

## Parameters

```
  Except: Exception that will be raised for retry (required)
  retries: Number of retries to be executed (default: 5)
  delay: Waiting time between each execution (default: 0)
  logger: Logger object that will be used to log (optional, default: None)
  level: Log level to log in, example: info, warning, error, exception, critical (default: info)
```
