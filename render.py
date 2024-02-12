import gradio as gr
import os
import sys
import bpy

def render(blend_path):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(current_directory, 'output')

    # outputディレクトリが存在しない場合にのみ作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # CUDAを使用するように設定
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = "OPTIX"

    cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
    cycles_prefs.refresh_devices()

    # 利用するデバイスをすべてOFFに初期設定
    for device in cycles_prefs.devices:
        device.use = False

    i = 0
    for device in cycles_prefs.devices:
        if device.type == 'OPTIX':
            device.use = True
            i = i+1
            
    bpy.ops.wm.open_mainfile(blend_path)
    # レンダリング設定を変更します
    bpy.context.scene.cycles.device = "GPU"             #   <-ここをファイル開いてからにすると成功
    bpy.context.scene.render.engine = 'CYCLES'          #   <-ここをファイル開いてからにすると成功

    bpy.context.scene.render.image_settings.file_format = 'PNG'  # 画像フォーマットを設定（PNG、JPEG、等）
    bpy.context.scene.render.filepath = output_directory + "img"  # ファイル名を設定
    # フレーム範囲を設定
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 1
    # レンダリングを実行
    bpy.ops.render.render(animation=True)
    # Blenderを終了
    bpy.ops.wm.quit_blender()

def upload_file(blend_file):
    render(blend_file)
    return os.path.basename(blend_file)

bl_webui = gr.Interface(
    title = "Blender Rendering Web UI",
    fn=upload_file,  # アップロードされたファイルを処理する関数
    inputs="file",   # アップロードボタンを表示する
    outputs="text"   # 結果を表示する
)

if __name__ == "__main__":
    bl_webui.launch(show_api=False, server_name="0.0.0.0")
