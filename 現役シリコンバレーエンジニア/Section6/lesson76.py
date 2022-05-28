"""
パッケージのインポート順について
"""


import collections
import os
import sys
### 標準パッケージ

import termcolor
### サードパーティせいのパッケージ

import lesson_package
### チームで作ったもの

#import config
### localで作ったもの

### 標準ライブラリは　python3.8/collections など
print(collections.__file__)
### サードパーティ製は python3.8/site-package/　の中に置かれる
print(termcolor.__file__)

print(sys.path)