import whisper
import time
import requests
import os
from urllib.parse import urlparse
import subprocess
import shlex
from datetime import datetime

#model = whisper.load_model("medium")
model = whisper.load_model("large")

def extract_audio(video_path, output_path, timeout=300):
    if video_path is None:
        return None  # Handle case when video_path is None
    try:
        # Use FFmpeg to extract audio from video

        command = f'ffmpeg -loglevel quiet -i "{video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{temp_wav}"'
        subprocess.run(shlex.split(command), timeout=timeout, check=True)
        print("音频提取完成")
        #去除音频中的静音 //去除所有超过0.8秒的静音(低于30分贝)部分。（过长的静音会导致whisper产生幻觉，重复输出）
        command2 = f'ffmpeg -loglevel quiet -i "{temp_wav}" -af silenceremove=stop_periods=-1:stop_duration=0.8:stop_threshold=-30dB "{output_path}"'
        subprocess.run(shlex.split(command2), timeout=timeout, check=True)
        print("音频去除静音完成")
        return output_path  # Return the output path after successful extraction
    except subprocess.TimeoutExpired:
        print("音频提取超时")
        return None  # Return None if extraction times out
    except Exception as e:
        print("提取音频时出错:", e)
        return None  # Return None if there's an error
def get_txt(audio_path):
    if not os.path.isfile(audio_path):
        return None
    result = model.transcribe(audio_path, language="Chinese", initial_prompt=prompt)
    print(result["text"])
    return result["text"]


def get_video_filename(url):
    # 解析视频下载地址获取文件名
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename

def download_video(url, save_directory):
    try:
        # 发送 HTTP GET 请求获取视频下载地址
        print("start time:", datetime.now())
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if not response.content:
            print("Error: No data returned for the video.")
            return None
        # 获取视频下载地址
        data = response.json()
        video_url = data.get("parseContent")
        video_id = data.get("id")

        # 获取视频文件名
        filename = get_video_filename(video_url)
        print(filename,video_url)
        save_path = os.path.join(save_directory, filename)

        # 下载视频文件
        video_response = requests.get(video_url, stream=True)
        video_response.raise_for_status()  # 检查请求是否成功

        with open(save_path, 'wb') as f:
            for chunk in video_response.iter_content(1024):
                f.write(chunk)
        print("视频下载完成，保存路径为:", save_path)
        return save_path,video_id
    except requests.exceptions.RequestException as e:
        print("请求错误:", e)
        return None  # Return None if there's an error

def process_video(url, save_directory):
    try:
        download_result = download_video(url, save_directory)
        if not download_result:
            return
        video_path, video_id = download_result
        print("Processing video:", video_path)

        audio_path = extract_audio(video_path, output_path)
        #if not audio_path:
        #    print("Audio extraction failed. Skipping.")
        #    return
        result_text = get_txt(audio_path)
        delete_file(video_path)
        delete_file(audio_path)
        delete_file(temp_wav)
        if not result_text:
            print("not get result_text. Skipping.")
            return
        post_data(video_id, result_text)
        print("end time:", datetime.now())
    except Exception as e:
        print("An error occurred during video processing:", e)
def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            # 删除视频文件
            os.remove(file_path)
            print("视频文件已成功删除:", file_path)
        else:
            print("视频文件不存在:", file_path)
    except OSError as e:
        print("删除视频文件时出错:", e)

def post_data(id,text):
    # 入参
    payload = {
        "id": id,
        "content": text
    }
    try:
        # 发送POST请求
        response = requests.post(post_url, json=payload)
        # 如果响应状态码不是200，则抛出异常
        response.raise_for_status()
        # 打印响应内容
        print(id," 上传文本成功，",response.text)
    except requests.exceptions.RequestException as e:
        # 捕获请求异常并打印错误信息
        print("请求异常:", e)

if __name__ == "__main__":
    # 请求地址
    #test
    get_url = "http://{}/api/getdata"
    set_url = "http://{}/api/setdata"
    environments = [
        {"host": "10.108.62.16:18004"}
    ]
    #environments = [
    #    {"host": "10.108.62.16:18004"}
    #]
    #如果想要让转出来的文字有标点符号的话，prompt的最后必须加上句号结尾。（prompt只是学习你的风格，不会执行命令）
    prompt = 批批网，速干，舒美绸，无肩带，大码，小码，中码，均码，服装批发，一件起批，工装库，裙子，连衣裙，工装，速干裤，剪标，1加，4加。"
    # 保存视频的目录
    save_directory = f"D:\\"
    output_path = f"D:\\output.wav"
    temp_wav = f"D:\\temp.wav"
    while True:
        try:
            for environment in environments:
                host = environment["host"]
                request_url = get_url.format(host)
                post_url = set_url.format(host)
                print(host)
                process_video(request_url, save_directory)
        except KeyboardInterrupt:
            print("Process interrupted by the user.")
            break
        except Exception as e:
            print("An error occurred in the main loop:", e)
        time.sleep(5)
