import gradio as gr
import os
import subprocess

# ファイルを受け取り、Blenderを開始
def start_blender(file):
    global subprocess_running
    subprocess_running = True

    # Pythonファイルのディレクトリを取得
    script_dir = os.path.dirname(os.path.realpath(__file))

    # Blenderコマンドを実行するためのコマンドリスト
    command = [
        os.path.join(script_dir, 'blender', 'blender'),  # Blender実行可能ファイルのパス
        '-b',  # バッチモード
        '-noaudio',  # オーディオを無効にする
        '-P', os.path.join(script_dir, 'render.py')  # Pythonスクリプトのパス
    ]

    # サブプロセスを起動
    subprocess.Popen(command)

# Gradioのインターフェースを設定
iface = gr.Interface(
    fn=start_blender,  # ファイルアップロード時に呼び出される関数
    inputs="file",     # ファイルのアップロードを許可
    outputs="text",    # テキストの出力を設定
    live=True,           # リアルタイムでアップロード可能にする
    share=True
)

# インターフェースを開始
iface.launch()
