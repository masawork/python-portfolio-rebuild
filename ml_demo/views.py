from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pickle
import numpy as np
from pathlib import Path

# MLモデルのパス
MODEL_PATH = Path(__file__).resolve().parent.parent / 'ml' / 'models' / 'sample_model.pkl'


def load_model():
    """MLモデルを読み込む"""
    if MODEL_PATH.exists():
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None


@api_view(['POST'])
def predict(request):
    """
    機械学習推論API
    例: 簡単な回帰モデル（入力値から予測値を返す）
    """
    try:
        data = request.data
        # 入力値の取得（例: 数値のリスト）
        input_values = data.get('input', [])
        
        if not input_values:
            return Response(
                {'error': 'inputパラメータが必要です'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # モデルの読み込み
        model = load_model()
        
        if model is None:
            # モデルがない場合は簡単な計算を返す（デモ用）
            result = sum(input_values) * 2.5
            prediction = {
                'input': input_values,
                'prediction': result,
                'model_used': 'demo_calculation'
            }
        else:
            # モデルで推論
            input_array = np.array(input_values).reshape(1, -1)
            prediction_value = model.predict(input_array)[0]
            prediction = {
                'input': input_values,
                'prediction': float(prediction_value),
                'model_used': 'trained_model'
            }
        
        return Response(prediction, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def ml_demo(request):
    """MLデモ画面"""
    return render(request, 'ml_demo/ml_demo.html')

