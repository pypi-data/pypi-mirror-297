## description
功能：将音视频数据转换成rtp包

## usage examples
```python
from RTPSender.RTPSender import RTPSenderNewProcess
from pydub import AudioSegment
import cv2
from time import sleep, time

if __name__ == '__main__':
    ip_address = "127.0.0.1"
    port = 7777
    image_file = "images/frame_0.png"
    image_files = ["images/frame_%d.png" % i for i in range(5)]
    audio_file = "audios/bgroup.wav"
    audio_16k_file = "audios/bgroup16k.wav"

    frame_size = (1080, 1920) # (width, height)

    audio = AudioSegment.from_file(audio_16k_file, format="wav")
    audio_data = audio.raw_data
    imgs = [cv2.imread(image_file) for image_file in image_files]

    log_dir = "./logs/"

    logger.remove() # 移除默认的日志记录器：控制台打印
    logger.add(
        log_dir + "rtp_sender.{time:YYYY-MM-DD_HH}.log", 
        rotation="1 hour",  # 每小时创建一个新日志文件
        retention=timedelta(days=7),  # 保留最近days天的日志，默认为7天
        compression=None,  # 不压缩日志文件
        format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {message}"
    )
    # 为了统一日志，需传入第四个参数logger
    rtpSenderNewProcess = RTPSenderNewProcess(ip_address, port, frame_size, logger, hard_encode=True, open_log=True, days=7, stdout=False)

    rtpSenderNewProcess.enque_event("init", None) # 初始化时，发送事件名称"init"即可，data传None，内部会初始化RTPSender

    loop_cnt = 1

    i = 0
    cnt = 0
    t1 = time()

    try:
        while loop_cnt > 0:
            for img in imgs:
                if i >= len(audio_data) - 640:
                    i = 0
                for j in range(25):
                    rtpSenderNewProcess.enque_event("video", img) # 发送视频帧，事件名称"video"，data为img，表示一帧图像
                    data1 = audio_data[i:i+640]
                    i += 640
                    data2 = audio_data[i:i+640]
                    rtpSenderNewProcess.enque_event("audio", (data1, data2)) # 发送音频帧，事件名称"audio"，data为(data1, data2),表示两帧音频

                    cnt += 1
                    i += 640
                    t2 = time()
                    t = t1 + cnt*0.04 - t2
                    if t > 0:
                        sleep(t)
            loop_cnt -= 1
    finally:
        rtpSenderNewProcess.stop_process() # 发送完成之后，必须停止进程，和该进程相关的所有资源都会被释放，包括rtpSender以及其中的线程
```

## Releases
| Release Version | Release Date | Updates                   |
|-----------------|--------------|---------------------------|
| v3.9.1          | 2024-09-19   | 引入多进程并统一日志|
| v3.8.8          | 2024-09-14   | 在v3.8.6的基础上，增加平均耗时日志|
| v3.8.6          | 2024-09-14   | 增加编码和发送耗时日志|
| v3.8.4          | 2024-09-13   | 在v3.8.3的基础上，增加时间日志|
| v3.8.3          | 2024-09-11   | 在v3.8.0的基础上，暴露gop参数|
| v3.8.2          | 2024-09-06   | 删除测试代码              |
| v3.8.1          | 2024-09-06   | 引入多进程  |
| v3.8.0          | 2024-09-04   | 设置码率为600k  |
| v3.7.9          | 2024-08-29   | 添加控制台日志开关                 |
| v3.7.8          | 2024-08-29   | 使用loguru记录日志                 |
| v3.7.7          | 2024-08-29   | Bug fixes            |
| v3.7.5          | 2024-08-29   | 添加滚动日志，保存日志到文件                 |