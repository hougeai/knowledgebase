> 摘要：新手小白入门AIGC开发，必须理论结合实践。本系列文章将结合Datawhale 11月份组织的《如何用免费GPU部署大模型》打卡活动，通过全身心体验，记录项目开发过程中遇到的一些问题和总结开发过程中的一些心得体会。
本文是基于项目文档来完成第4个任务：在趋动云上用免费GPU部署一个自己的AI项目。

## 项目简介
本次选择部署的一个项目是利用yolov8自动检测出图像或者视频中的行人的个数，并进行人群数量的统计。yolov8集成了检测和跟踪的功能，所以可以根据跟踪行人的id信息对视频中的行人进行去重，从而达到统计一个视频中实际有多少人的目的。

本项目已经在趋动云上公开：[项目地址](https://platform.virtaicloud.com/gemini_web/workspace/space/fbrmebdsfcjp/project/376941694915973120/code/detail/376941694815309824)
## 项目创建
根据前几个任务的练手，我们已经熟练掌握了如何在趋动云中创建一个项目。
- 在我的空间创建项目，命名为`yolov8人群监测`
- 参考文档配置好环境：这里使用6G显存就够
## 核心代码构建
首先将主处理逻辑封装在`yolo_core.py`

```python
model = YOLO('yolov8n.pt')
box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)

# 图像检测
def process_frame(frame, num_box=True, device='cpu'):
    print(device)
    results = model(frame, imgsz=640, verbose=False, show=False, device=device)[0]
    detections = sv.Detections.from_yolov8(results)
    detections = detections[detections.class_id == 0]
    labels = [f"{model.names[class_id]}{s:0.2f}" for s, class_id in zip(detections.confidence, detections.class_id)]
    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
    return frame if not num_box else (frame, str(len(detections)))

# 视频检测
def process_video(video_path, mode='track', device='cuda:0'):
    print(device)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    h, w = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_path = "out-" + video_path.split('/')[-1]
    out = cv2.VideoWriter(out_path, fourcc, fps, (int(w), int(h)))
    count = 0
    if mode == 'track':
        tids = set()
        with tqdm(total=frame_count-1) as pbar:
            for result in model.track(source=video_path, show=False, stream=True, verbose=False, device=device):
                frame = result.orig_img
                detections = sv.Detections.from_yolov8(result)
                detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
                detections = detections[detections.class_id == 0]
                if detections:
                    tracker_ids = detections.tracker_id # 多目标追踪ID
                    tids |= set(tracker_ids.tolist())
                    labels = [f'#{tracker_ids[i]}' for i in range(len(tracker_ids))]
                    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
                out.write(frame)
                pbar.update(1)
        count = len(tids)
    elif mode == 'det':
        with tqdm(total=frame_count-1) as pbar:
            while(cap.isOpened()):
                success, frame = cap.read()
                if not success:
                    break
                frame, num = process_frame(frame, num_box=True, device=device)
                count += int(num)
                out.write(frame)
                pbar.update(1)
    out.release()
    cap.release()
    return out_path, str(count)
```
通过gradio实现可视化的界面，这里采用了应对复杂场景的接口`gr.Blocks()`，核心代码如下：

```python
with gr.Blocks() as demo:
    html_title = '''
                <h1 style="text-align: center; color: #333;">yolov8人群监测</h1>
                '''
    gr.HTML(html_title)
    with gr.Tab("图像处理"):
        # Blocks默认设置所有子组件按垂直排列Column
        with gr.Row():
            image_input = gr.Image(label='输入图像')
            with gr.Column():
                image_output = gr.Image(label='检测结果')
                text_image = gr.Textbox(label='行人数量')
        image_button = gr.Button(value="提交")
    with gr.Tab("视频处理"):
        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label='输入图像')
                radio_input = gr.Radio(["det", "track"])
            with gr.Column():
                video_output = gr.Video(label='检测结果')
                text_video = gr.Textbox(label='行人数量')
        video_button = gr.Button(value="提交")
    image_button.click(process_frame, inputs=image_input, outputs=[image_output, text_image])
    video_button.click(process_video, inputs=[video_input, radio_input], outputs=[video_output, text_video])
demo.launch(share=False, server_name='0.0.0.0', server_port=7000)
```
## 项目部署
在项目右侧边栏添加端口信息`7000`，实现结果如下：

分为两个tab，分别处理图像和视频：

 - 图像处理：输入图像，输出检测结果和行人数量
 - 视频处理：输入视频，通过`radio`组件实现两种模式：`det`和`track`分别代表是否采用跟踪来判别是否为同一个行人，输出为视频跟踪可视化结果和行人数量
 
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/fb873fd90c6f42016eaf6cb8235971dd.png)

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/60d7380715591cc4a17af8819edc9c78.png)

