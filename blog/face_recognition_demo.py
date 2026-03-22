"""
顔認証デモ用のユーティリティ関数
"""
import cv2
import face_recognition
import numpy as np
from typing import Optional, Dict, List, Tuple
import base64
from io import BytesIO
from PIL import Image


def process_camera_stream(camera_url: str) -> Dict:
    """
    WEBカメラのストリームから顔を検出・認識する
    
    Args:
        camera_url: カメラのURL（例: http://192.168.1.100:8080/video）
    
    Returns:
        検出結果の辞書
    """
    try:
        # カメラに接続
        cap = cv2.VideoCapture(camera_url)
        
        if not cap.isOpened():
            return {
                'success': False,
                'error': f'カメラに接続できませんでした: {camera_url}'
            }
        
        # 1フレーム取得
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {
                'success': False,
                'error': 'フレームの取得に失敗しました'
            }
        
        # BGRからRGBに変換（face_recognitionはRGBを期待）
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 顔の位置を検出
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if not face_locations:
            return {
                'success': True,
                'faces_detected': 0,
                'message': '顔が検出されませんでした',
                'image': frame_to_base64(frame)
            }
        
        # 顔の特徴を抽出
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # 検出された顔に枠を描画
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, 'Face Detected', (left, top - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return {
            'success': True,
            'faces_detected': len(face_locations),
            'face_locations': face_locations,
            'face_encodings_count': len(face_encodings),
            'message': f'{len(face_locations)}個の顔を検出しました',
            'image': frame_to_base64(frame)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'エラーが発生しました: {str(e)}'
        }


def frame_to_base64(frame: np.ndarray) -> str:
    """
    OpenCVのフレームをBase64エンコードされた文字列に変換
    
    Args:
        frame: OpenCVのフレーム（BGR形式）
    
    Returns:
        Base64エンコードされた画像文字列
    """
    # BGRからRGBに変換
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # PIL Imageに変換
    pil_image = Image.fromarray(rgb_frame)
    
    # BytesIOに保存
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG')
    
    # Base64エンコード
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_str


def validate_camera_url(url: str) -> bool:
    """
    カメラURLの形式を検証
    
    Args:
        url: カメラのURL
    
    Returns:
        有効なURLかどうか
    """
    if not url:
        return False
    
    # ローカルカメラ（0-9の数字のみ）
    if url.isdigit():
        return True
    
    # HTTP/HTTPS URL
    if url.startswith('http://') or url.startswith('https://'):
        return True
    
    # RTSP URL
    if url.startswith('rtsp://'):
        return True
    
    return False
