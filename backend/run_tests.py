"""
テスト実行スクリプト
"""
import unittest
import sys
import os

# テストディレクトリをインポートパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """すべてのテストを実行する"""
    # テストディレクトリからすべてのテストを検出
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    # テストを実行
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # 結果に基づいて終了コードを設定
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
