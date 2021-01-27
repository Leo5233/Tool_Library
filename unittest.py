# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:02:59 2020

@author: user
"""

import unittest
import sys

class T(unittest.TestCase):
    # testFixture建立
    def setUp(self):
        self.a = "qwe"
    
    def test1(self):
        # 各類檢測
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertNotEqual('foo'.upper(), 'OO')
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
        self.assertIsNone(None, msg=None)
        self.assertIsNotNone('', msg=None)
        self.assertIn('t', 'teu', msg=None)
        self.assertNotIn('p', 'dgs', msg=None)
        self.assertIsInstance(3, int, msg=None)
        self.assertNotIsInstance(4, str, msg=None)
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'],"you are an idiot")
        # 檢測應該要出該類錯 沒出錯反而會報錯
        with self.assertRaises(TypeError,msg='msg'):
            s.split(2)
            
        self.assertGreater(6, 5)
        self.assertGreaterEqual(5, 5)# >=
        self.assertLess(5, 6)
        self.assertLessEqual(5, 5)
        self.assertRegex('abcdefg', '.*c')
        self.assertNotRegex('abcdefg','3' )
        self.assertCountEqual('112233345', '423152133')# 是否每個字元的重複次數一樣(只是順序不同)
    
    # 無論如何都會被跳過，skip類的可以在括號內加入訊息，如果不用裝飾器可用一般的def內放入self.skipTest(msg)
    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    # 有skipIf和skipUnless
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass
    
    # 用with self.subTest(i=迴圈個別項)，使迴圈內的項目會全部測完，不會一遇到錯誤就停止。
    def sub_test(self):
        for x in range(10):
            with self.subTest(i=x):
                self.assertEqual(x%2, 0)
    
    # testFixture建立
    def tearDown(self):
        del self.a

# 用來自訂蒐集各Testcase內的測試method來組合  
def suite():
    suite = unittest.TestSuite()
    suite.addTest(T('test1'))
    suite.addTest(T('test_nothing'))
    return suite
        
if __name__ == '__main__':
    # unittest.main() 跑testcase全部
    # 跑suite要用testRunner
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
    