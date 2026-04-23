#!/usr/bin/env python3
"""
Modbus HTTP网关启动器
启动HTTP服务器并显示二维码，手机扫码即可打开控制页面
"""

import sys
import os
import socket
import threading
import logging
from pathlib import Path

# 添加当前目录到Python路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import font as tkfont

# ── 导入Flask应用 ──
from app import app, init_app, get_local_ip, logger

# ── 配置 ──
HTTP_PORT = 5000

class QRCodeWindow:
    """二维码显示窗口"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("机器人无线网关")
        self.root.geometry("520x680")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # 居中显示
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 520) // 2
        y = (self.root.winfo_screenheight() - 680) // 2
        self.root.geometry(f"+{x}+{y}")

        # 获取本地IP
        self.local_ip = self._get_ip()

        # 构建界面
        self._build_ui()

        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _get_ip(self):
        """获取本地IP地址"""
        try:
            return get_local_ip()
        except:
            return "127.0.0.1"

    def _build_ui(self):
        """构建界面"""
        # ── 标题 ──
        title_font = tkfont.Font(size=22, weight="bold")
        tk.Label(
            self.root, text="伯朗特移动端控制平台",
            font=title_font, bg="white", fg="#2c3e50"
        ).pack(pady=(30, 5))

        sub_font = tkfont.Font(size=12)
        tk.Label(
            self.root, text="手机扫码即可控制设备",
            font=sub_font, bg="white", fg="#7f8c8d"
        ).pack(pady=(0, 25))

        # ── 二维码 ──
        url = f"http://{self.local_ip}:{HTTP_PORT}"
        qr_img = self._generate_qr(url, size=280)

        qr_label = tk.Label(self.root, image=qr_img, bg="white")
        qr_label.image = qr_img  # 保持引用
        qr_label.pack(pady=10)

        # ── URL文字（备用） ──
        url_font = tkfont.Font(size=16, weight="bold")
        tk.Label(
            self.root, text=url,
            font=url_font, bg="white", fg="#3498db"
        ).pack(pady=(5, 5))

        tk.Label(
            self.root, text="↑ 用微信 / 相机扫描上方二维码",
            font=sub_font, bg="white", fg="#95a5a6"
        ).pack(pady=(0, 20))

        # ── 分隔线 ──
        sep = tk.Frame(self.root, height=1, bg="#ecf0f1")
        sep.pack(fill="x", padx=40, pady=5)

        # ── 服务器状态 ──
        status_frame = tk.Frame(self.root, bg="white")
        status_frame.pack(pady=(15, 5))

        self.status_dot = tk.Canvas(status_frame, width=14, height=14,
                                     bg="white", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 8))
        self._draw_dot("#95a5a6")  # 灰色 = 启动中

        self.status_label = tk.Label(
            status_frame, text="服务器启动中...",
            font=sub_font, bg="white", fg="#7f8c8d"
        )
        self.status_label.pack(side="left")

        # ── 信息行 ──
        info_font = tkfont.Font(size=10)
        info_text = (
            f"IP: {self.local_ip}   |   端口: {HTTP_PORT}\n"
            f"配置文件: config.json   |   确保手机和PC在同一网络"
        )
        tk.Label(
            self.root, text=info_text,
            font=info_font, bg="white", fg="#bdc3c7",
            justify="center"
        ).pack(pady=(5, 15))

        # ── 停止按钮 ──
        btn_font = tkfont.Font(size=13)
        self.stop_btn = tk.Button(
            self.root, text="  停止服务器  ",
            font=btn_font, bg="#e74c3c", fg="white",
            activebackground="#c0392b", activeforeground="white",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._on_close
        )
        self.stop_btn.pack(pady=10)

        # 启动后延迟更新状态
        self.root.after(2000, self._update_status)

    def _generate_qr(self, data, size=280):
        """生成二维码图片"""
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        pil_img = qr.make_image(fill_color="#2c3e50", back_color="white")
        pil_img = pil_img.resize((size, size), Image.NEAREST)
        return ImageTk.PhotoImage(pil_img)

    def _draw_dot(self, color):
        """绘制状态指示灯"""
        self.status_dot.delete("all")
        self.status_dot.create_oval(1, 1, 13, 13, fill=color, outline="")

    def _update_status(self):
        """更新服务器状态"""
        self._draw_dot("#2ecc71")  # 绿色 = 运行中
        self.status_label.config(text="服务器运行中 ✓", fg="#2ecc71")

    def _on_close(self):
        """关闭窗口时停止服务器"""
        self.root.destroy()
        os._exit(0)

    def run(self):
        """运行窗口"""
        self.root.mainloop()


def start_flask_server():
    """在后台线程中启动Flask服务器"""
    # 初始化应用（加载配置、连接Modbus）
    init_app()

    logger.info(f"HTTP服务器启动: 0.0.0.0:{HTTP_PORT}")
    logger.info(f"手机端访问: http://{get_local_ip()}:{HTTP_PORT}")

    # 启动Flask（生产环境使用非debug模式）
    app.run(
        host="0.0.0.0",
        port=HTTP_PORT,
        debug=False,
        use_reloader=False
    )


def main():
    """主函数"""
    # 启动Flask服务器线程
    server_thread = threading.Thread(target=start_flask_server, daemon=True)
    server_thread.start()

    # 显示二维码窗口
    QRCodeWindow().run()


if __name__ == "__main__":
    main()
