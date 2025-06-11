"""
pytestを使用したテスト実行スクリプト
"""
import sys
import pytest

def run_tests():
    """pytestを使用してすべてのテストを実行する"""
    # コマンドライン引数をpytestに渡す
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 統合テストを除外するデフォルト設定（-mオプションが指定されていない場合）
    if not any(arg.startswith('-m') for arg in args):
        args.append('-m')
        args.append('not integration')
    
    # pytestを実行
    return pytest.main(args)

if __name__ == '__main__':
    sys.exit(run_tests())
