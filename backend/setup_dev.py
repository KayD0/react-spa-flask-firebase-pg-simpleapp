"""
開発環境セットアップスクリプト
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Pythonバージョンをチェックする"""
    required_version = (3, 7)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"エラー: Python {required_version[0]}.{required_version[1]} 以上が必要です")
        print(f"現在のバージョン: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        sys.exit(1)
    
    print(f"Python {current_version[0]}.{current_version[1]}.{current_version[2]} を使用しています")

def create_virtual_env(venv_path):
    """仮想環境を作成する"""
    if os.path.exists(venv_path):
        print(f"仮想環境が既に存在します: {venv_path}")
        return
    
    print("仮想環境を作成しています...")
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print(f"仮想環境が作成されました: {venv_path}")
    except subprocess.CalledProcessError as e:
        print(f"仮想環境の作成中にエラーが発生しました: {e}")
        sys.exit(1)

def install_dependencies(venv_path):
    """依存関係をインストールする"""
    # 仮想環境内のpipを取得
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, 'Scripts', 'pip')
    else:  # macOS/Linux
        pip_path = os.path.join(venv_path, 'bin', 'pip')
    
    print("依存関係をインストールしています...")
    try:
        # pipをアップグレード
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # requirements.txtから依存関係をインストール
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        
        print("依存関係のインストールが完了しました")
    except subprocess.CalledProcessError as e:
        print(f"依存関係のインストール中にエラーが発生しました: {e}")
        sys.exit(1)

def create_env_file():
    """環境変数ファイルを作成する"""
    env_example_path = '.env.example'
    env_path = '.env'
    
    if os.path.exists(env_path):
        print(f"環境変数ファイルが既に存在します: {env_path}")
        return
    
    if not os.path.exists(env_example_path):
        print(f"警告: {env_example_path} が見つかりません")
        return
    
    print(f"環境変数ファイルを作成しています: {env_path}")
    try:
        with open(env_example_path, 'r') as example_file:
            with open(env_path, 'w') as env_file:
                env_file.write(example_file.read())
        print(f"環境変数ファイルが作成されました: {env_path}")
        print(f"注意: {env_path} を編集して、実際の環境変数を設定してください")
    except IOError as e:
        print(f"環境変数ファイルの作成中にエラーが発生しました: {e}")

def setup_dev_environment(args):
    """開発環境をセットアップする"""
    # 現在のディレクトリをスクリプトのディレクトリに変更
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Pythonバージョンをチェック
    check_python_version()
    
    # 仮想環境のパス
    venv_path = args.venv_path
    
    # 仮想環境を作成
    create_virtual_env(venv_path)
    
    # 依存関係をインストール
    install_dependencies(venv_path)
    
    # 環境変数ファイルを作成
    create_env_file()
    
    print("\n開発環境のセットアップが完了しました！")
    
    # 仮想環境のアクティベート方法を表示
    if os.name == 'nt':  # Windows
        activate_cmd = f"{venv_path}\\Scripts\\activate"
    else:  # macOS/Linux
        activate_cmd = f"source {venv_path}/bin/activate"
    
    print("\n仮想環境をアクティベートするには、次のコマンドを実行してください:")
    print(f"  {activate_cmd}")
    
    print("\nアプリケーションを実行するには、次のコマンドを実行してください:")
    print("  python app.py")
    
    print("\nテストを実行するには、次のコマンドを実行してください:")
    print("  python run_tests.py")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='開発環境をセットアップする')
    parser.add_argument('--venv-path', default='venv', help='仮想環境のパス (デフォルト: venv)')
    args = parser.parse_args()
    
    setup_dev_environment(args)
