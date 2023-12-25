import os

from mmgui import App, BrowserWindow
import pdbparse
from pdbparse.peinfo import *

app = App(headless=False)
win = None

# 根据guid的十六进制查找另一个guid的位置，再对数据进行处理。
def files(pdb_file, data):
    find_num1 = ""
    find_out = 0
    with open(pdb_file, "rb") as j:
        data_sum = j.read()
    data_hex = data.hex()
    sum_hex = data_sum.hex()
    hex = data_hex[24:56]
    if sum_hex.count(hex, 0, -1) > 1:
        if sum_hex.find(hex,0,sum_hex.find(data_hex)) != -1:
            find_out = sum_hex.find(hex,0, sum_hex.find(data_hex))
        else:
            find_out = sum_hex.find(hex,sum_hex.index(data_hex) + 32,-1)
        find_num = sum_hex[find_out - 24:find_out + 32 + 32 * 8 + 2]
        for i in find_num:
            find_num1 += chr(int(i, 16))
        return find_num.upper(), find_num1
    else:
        return "未找到第二个GUID", "未找到第二个GUID"

# 对传输的数据的间隔，换行进行处理
def sort(pdb_file, hex_num):
    file1 = ""
    file2 = ""
    for i, num in enumerate(hex_num):
        file1 += str(num)

        if (i + 1) % 2 == 0:
            file1 += "&nbsp;"
        # if (i + 1) % 16 == 0:
        #     file1 += "&nbsp;&nbsp;"
        if (i + 1) % 32 == 0:
            file1 += "<br>"
    for i, num in enumerate(pdb_file):
        if type(num) != str:
            if num < 32 or num > 255:
                file2 += "."
            else:
                file2 += chr(i)
            if (i + 1) % 16 == 0:
                file2 += "<br>"
        else:
            if (i + 1) % 16 == 0:
                file2 += "<br>"
            file2 += num
    return file1, file2

# 获取传输的文件并获取guid等基础信息，再经过 sort和files方法对数据进行处理
def open_file(msg):
    if msg == "1":
        pdb_file = win.show_file_dialog_for_file("请选择pdb文件", "*")[0]
        p = None
        try:
            p = pdbparse.parse(pdb_file, fast_load=True)
        except ValueError:
            win.webview.send_message_to_js({"msg": "error" + "Unsupported file type "})
            return

        # ValueError("Unsupported file type"):

        pdb = p.streams[pdbparse.PDB_STREAM_PDB]
        pdb.load()
        guidstr = ('%08x%04x%04x%s' % (pdb.GUID.Data1, pdb.GUID.Data2, pdb.GUID.Data3, binascii.hexlify(
            pdb.GUID.Data4).decode('ascii'))).upper()
        win.webview.send_message_to_js({"msg": [guidstr, pdb.Age, pdb.Version, str(pdb.TimeDateStamp), pdb.names]})
        file1, file2 = sort(pdb.data, pdb.data.hex().upper())

        file3_temporary, file4_temporary = files(pdb_file, pdb.data)
        file3, file4 = sort(file4_temporary, file3_temporary)
        win.webview.send_message_to_js({"msg": "file1" + file1})
        win.webview.send_message_to_js({"msg": "file2" + file2})
        win.webview.send_message_to_js({"msg": "file3" + file3})
        win.webview.send_message_to_js({"msg": "file4" + file4})

# 创建可视化界面
def on_create(ctx):
    global win

    win = BrowserWindow({
        "title": "CtlCode",
        "width": 1200,
        "height": 805,
        "dev_mode": False,
    })

    win.webview.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "index.html"))
    win.webview.bind_function("open_file", open_file)
    win.webview.bind_function("files", files)
    win.show()


def main():
    app.on("create", on_create)
    app.run()


if __name__ == "__main__":
    main()
