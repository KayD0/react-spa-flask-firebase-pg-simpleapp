"""
ロギングモジュール
"""
import os
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, g


class CustomJSONFormatter(logging.Formatter):
    """JSON形式のログフォーマッター"""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        ログレコードをJSON形式にフォーマットする
        
        Args:
            record: ログレコード
            
        Returns:
            JSON形式のログ文字列
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # 例外情報があれば追加
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        # リクエスト情報があれば追加
        if hasattr(g, 'request_id'):
            log_data['request_id'] = g.request_id
        
        # 追加のコンテキスト情報があれば追加
        if hasattr(record, 'context'):
            log_data.update(record.context)
        
        return json.dumps(log_data)


def setup_logger(app: Flask) -> None:
    """
    アプリケーションにロガーを設定する
    
    Args:
        app: Flaskアプリケーションインスタンス
    """
    # ログレベルの設定
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    # ルートロガーの設定
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # 既存のハンドラをクリア
    for handler in logger.handlers:
        logger.removeHandler(handler)
    
    # コンソールハンドラの追加
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    
    # 開発環境では通常のフォーマット、それ以外ではJSON形式を使用
    if app.debug:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        formatter = CustomJSONFormatter()
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイルハンドラの追加（オプション）
    log_file = os.getenv('LOG_FILE')
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Flaskのロガーも同じ設定を使用
    app.logger.handlers = logger.handlers
    app.logger.setLevel(numeric_level)
    
    # リクエスト開始時にリクエストIDを生成
    @app.before_request
    def before_request():
        g.request_id = os.urandom(16).hex()
        app.logger.info(
            f"Request started: {request.method} {request.path}",
            extra={
                'context': {
                    'method': request.method,
                    'path': request.path,
                    'ip': request.remote_addr,
                    'user_agent': request.user_agent.string
                }
            }
        )
    
    # リクエスト終了時にログを記録
    @app.after_request
    def after_request(response):
        app.logger.info(
            f"Request completed: {request.method} {request.path} {response.status_code}",
            extra={
                'context': {
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'response_time_ms': (
                        (datetime.utcnow() - g.get('request_start_time', datetime.utcnow())).total_seconds() * 1000
                        if hasattr(g, 'request_start_time') else None
                    )
                }
            }
        )
        return response


def get_logger(name: str) -> logging.Logger:
    """
    名前付きロガーを取得する
    
    Args:
        name: ロガー名
        
    Returns:
        設定済みのロガーインスタンス
    """
    return logging.getLogger(name)
