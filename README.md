# whisper-in-colab 
[![Open In Colab]([https://colab.research.google.com/assets/colab-badge.svg)]([[https://colab.research.google.com/drive/1gq0Qn-_PdKFZFr_LIxd-WWJBT3Mm1TP4?usp=sharing])
https://github.com/openai/whisper

use whisper in colab for free
在Colab部署whisper，可以免费使用。

https://colab.research.google.com/

注意，Colab是免费的，退出会丢失所有数据。默认不会创建GPU实例，需要修改“”edit》notebook settings》Hardware accelerator 》GPU“”，CPU实例也能转换，但是会很慢。



直接填下面的代码到colab中运行即可（Sound1.wav 手动上传）

!nvidia-smi
!pip3 install torch torchvision torchaudio
!pip3 install git+https://github.com/openai/whisper.git
!pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
from google.colab import drive
drive.mount('/content/gdrive')
%cd "/content/gdrive/MyDrive/Colab Notebooks"
!ls -l

!whisper /content/Sound1.wav--model large --language Chinese --initial_prompt "以下是普通话的句子。" --task translate



测试案例：
测试视频：

1691565662915.mp4

mp4直接转文字会有问题，兼容性不好，输出的结果是英文。需要把MP4转成wav格式。命令如下：

ffmpeg -i 1691565662915.mp4  -vn -acodec pcm_s16le -ar 44100 -ac 2 162.wav

解释：

-i 1691565662915.mp4：指定输入文件的路径和文件名。
-vn：禁用视频流，只提取音频。
-acodec pcm_s16le：设置音频编码器为pcm_s16le，用于转换为WAV格式。
-ar 44100：设置音频采样率为44100 Hz。
-ac 2：设置声道数为2（立体声）。
162.wav：指定输出音频文件的路径和文件名。
请确保将input.mp4替换为您要提取音频的实际文件路径和文件名，并根据需要更改输出音频的文件名。运行命令后，将生成一个包含从输入文件提取的音频的新的WAV文件。

得到的音频文件如下：

162.wav

再用whisper转成文字：

!whisper /content/162.wav --model large --language Chinese --initial_prompt "以下是普通话的句子。" --task translate


结果：

![a0a650e592d6ad61303b1d4ad23c641b](https://github.com/chow-q/whisper-in-colab/assets/73530205/470e0d45-a2cd-40a2-8d6f-76043b760885)
