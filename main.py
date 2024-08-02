import os
import re
import requests
import shutil
from PIL import Image

base_url = 'https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/'


# 生成所需README.md文件
def generate_readme(dir_path='docs'):
    dirs = os.listdir(dir_path)
    total_num = 0
    for dir in dirs:
        # 跳过非目录文件
        if not os.path.isdir(os.path.join(dir_path, dir)):
            continue
        readme_path = os.path.join(dir_path, dir, 'README.md')
        files = os.listdir(os.path.join(dir_path, dir))
        # 遍历目录下所有文件
        file_list = [file for file in files if os.path.isfile(os.path.join(dir_path, dir, file)) and file.endswith('.md') and file!= 'README.md']
        # 生成README.md文件
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('# {}\n\n'.format(dir))
            for file in file_list:
                rel_path = f'{dir_path}/{dir}/{file}'.replace(' ', '%20')
                # rel_path = file.replace(' ', '%20')
                f.write('- [{}]({})\n'.format(file.replace('.md', ''), rel_path))
            num = len(file_list)
            total_num += num
            f.write('\n\n<u>*本系列共更新**{}**篇文章*</u>。\n'.format(num))
    # 生成../README.md文件
    readme_path = os.path.join(dir_path, '..', 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'<u>.*?</u>', f'<u>*截至今日，知识库累计更新原创文章**{total_num}**篇*</u>', content)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    # 生成../_sidebar.md文件
    sidebar_path = os.path.join(dir_path, '..', '_sidebar.md')
    with open(sidebar_path, 'w', encoding='utf-8') as f:
        f.write('## 目录\n\n')
        for dir in dirs:
            if not os.path.isdir(os.path.join(dir_path, dir)):
                continue
            rel_path = f'{dir_path}/{dir}/README.md'.replace(' ', '%20')
            f.write('- [{}]({})\n'.format(dir, rel_path))
            readme_path = os.path.join(dir_path, dir, 'README.md')
            file_list = open(readme_path, 'r', encoding='utf-8').readlines()[2:]
            file_list = [file.strip() for file in file_list if file.strip() and file.startswith('-')]
            for file in file_list:
                f.write(f'  {file}\n')

# 定义下载图片的函数
def download_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    url = url.split(' ')[0]
    if url.startswith('https://mmbiz'):
        file_name = os.path.join(folder, f"{url.split('/')[-2]}.jpg")
    elif "#pic_center" in url:
        file_name = os.path.join(folder, url.split('#')[0].split('/')[-1])
    elif '?source' in url:
        file_name = os.path.join(folder, url.split('?')[0].split('/')[-1])
    else:
        file_name = os.path.join(folder, url.split('/')[-1])
    if os.path.exists(file_name):
        return
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as img_file:
            img_file.write(response.content)
        print(f'Downloaded: {file_name}')
    else:
        print(f'Failed to download: {url}')

# 下载所有md中的图片并保存到子目录assets文件夹中，并替换md中的链接
def replace_images(dir_path='docs'):
    # 遍历所有子目录
    urls = []
    dirs = os.listdir(dir_path)
    for dir in dirs:
        # 跳过非目录文件
        if not os.path.isdir(os.path.join(dir_path, dir)):
            continue
        files = os.listdir(os.path.join(dir_path, dir))
        # 遍历目录下所有文件
        file_list = [file for file in files if os.path.isfile(os.path.join(dir_path, dir, file)) and file.endswith('.md') and file!= 'README.md']
        for file in file_list:
            # 读取文件内容
            with open(os.path.join(dir_path, dir, file), 'r', encoding='utf-8') as f:
                content = f.read()
            # 下载图片并保存到assets文件夹中
            # img_list = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
            # img_urls = [url for _, url in img_list if url.startswith('https://') and not url.startswith('https://gitee')]
            # if img_urls:
            #     for url in img_urls:
            #         download_image(url, os.path.join(dir_path, dir, 'assets'))
            # 替换md中的链接 https-assets
            # contents = content.split('\n')
            # for i, line in enumerate(contents):
            #     if re.match(r'!\[(.*?)\]\((.*?)\)', line):
            #         url = re.findall(r'!\[(.*?)\]\((.*?)\)', line)[0][1]
            #         if url.startswith('https://mmbiz'):
            #             file_name = os.path.join('assets', f"{url.split('/')[-2]}.jpg")
            #         elif "#pic_center" in url:
            #             file_name = os.path.join('assets', url.split('#')[0].split('/')[-1])
            #         elif '?source' in url:
            #             file_name = os.path.join('assets', url.split('?')[0].split('/')[-1])
            #         else:
            #             file_name = os.path.join('assets', url.split('/')[-1])
            #         line = line.replace(url, file_name)
            #         contents[i] = line
            # content = '\n'.join(contents)
            # print(f'Processed: {os.path.join(dir_path, dir, file)}')
            
            # 替换md中的链接 assets-oracle
            contents = content.split('\n')
            for i, line in enumerate(contents):
                if re.match(r'!\[(.*?)\]\((.*?)\)', line):
                    url = re.findall(r'!\[(.*?)\]\((.*?)\)', line)[0][1]
                    new = f'{base_url}{os.path.basename(url)}'
                    contents[i] = line.replace(url, new)
            content = '\n'.join(contents)
            print(f'Processed: {os.path.join(dir_path, dir, file)}')
            
            # 写入文件
            with open(os.path.join(dir_path, dir, file), 'w', encoding='utf-8') as f:
                f.write(content)

# 压缩图像画质
def compress_images(dir_path='docs', quality=70):
    dirs = os.listdir(dir_path)
    for dir in dirs:
        assets_path = os.path.join(dir_path, dir, 'assets')
        files = os.listdir(assets_path)
        for file in files:
            file_path = os.path.join(assets_path, file)
            if os.path.getsize(file_path) > 1 * 1024 * 1024:  # 大于 1MB
                with Image.open(file_path) as img:
                    # 压缩图像并覆盖原文件
                    if img.format != 'JPEG':
                        img = img.convert('RGB')
                        # 获取新文件路径
                        # new_file_path = os.path.splitext(file_path)[0] + '.jpg'
                        # 压缩图像并保存
                        img.save(file_path, format='JPEG', quality=quality, optimize=True)
                        print(f'Compressed: {file_path}, jpg')
                    else:
                        img.save(file_path, quality=quality, optimize=True)
                        print(f'Compressed: {file_path}')

def find(dir_path='docs'):
    # 遍历所有子目录
    dirs = os.listdir(dir_path)
    for dir in dirs:
        # 跳过非目录文件
        if not os.path.isdir(os.path.join(dir_path, dir)):
            continue
        files = os.listdir(os.path.join(dir_path, dir))
        # 遍历目录下所有文件
        file_list = [file for file in files if os.path.isfile(os.path.join(dir_path, dir, file)) and file.endswith('.md') and file!= 'README.md']
        for file in file_list:
            # 读取文件内容
            with open(os.path.join(dir_path, dir, file), 'r', encoding='utf-8') as f:
                content = f.read()
            # 替换md中的链接
            contents = content.split('\n')
            for i, line in enumerate(contents):
                if re.match(r'!\[(.*?)\]\((.*?)\)', line):
                    url = re.findall(r'!\[(.*?)\]\((.*?)\)', line)[0][1]
                    if not os.path.exists(os.path.join(dir_path, dir, url)):
                        print(dir, file, url)

def resize_image():
    img = Image.open('media/1.png')
    img.thumbnail((122, 94)) # 缩放图片
    img.save('media/logo_thumbnail.png') # 保存缩放后的图片

if __name__ == '__main__':
    # generate_readme()
    # replace_images()
    # compress_images()
    # find()
    resize_image()