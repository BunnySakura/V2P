# V2P

*视频转图片 | Video to picture*

![主界面](doc/img.png "主界面")

## 打包

```shell
python -m nuitka --standalone --enable-plugin=tk-inter --onefile --windows-disable-console --windows-icon-from-ico=icon.ico -o V2P mian.py
```
