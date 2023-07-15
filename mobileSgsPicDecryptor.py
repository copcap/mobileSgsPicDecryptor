import os

import threading

import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import tkinter.scrolledtext as st


# 打开文件夹
def loadFilePath():
	filename = fd.askdirectory()
	if (filename == ''):
		return
	fm_entry_text1.set(filename)

# 选择导出文件夹
def saveFilePath():
	filename = fd.askdirectory()
	if (filename == ''):
		return
	fm_entry_text2.set(filename)

# 检查路径合法性
def pathStringCheck(entry):
	if (os.path.exists(entry.get())):
		return True
	else:
		entry.delete(0, tk.END)
		return False

# 点击确定
def clickProgression():
	global inputPath, outputPath, lock
	inputPath = fm_entry1.get()
	outputPath = fm_entry2.get()
	if not os.path.isdir(inputPath):
		print(mb.showinfo(title='出错啦', message='文件输入路径不正确'))
		return
	if not os.path.isdir(outputPath):
		print(mb.showinfo(title='出错啦', message='文件输出路径不正确'))
		return
	
	if lock.locked():
		print(mb.showinfo(title='在解了在解了', message='正在解密，请不要着急……'))
		return
	
	# PV操作
	lock.acquire(blocking = False)
	fsinfo = os.listdir(inputPath)
	for fd in fsinfo:
		fullPath = os.path.join(inputPath, fd)
		if not os.path.isdir(fullPath):
			print('当前文件：' + fullPath)
			fuckGouka(fullPath,fd)
	lock.release()
	print(mb.showinfo(title='ohhhhh', message='解密完成！'))

# 对f目录下的fn文件进行解密
def fuckGouka(f,fn):
	data_read = open(f, "rb")
	out = os.path.join(outputPath, fn)
	byte = 0
	if data_read.readline().hex()[0:4]=='ffd8':
		print('未加密文件：' + f)
		data_read.close()
		return
	data_read.seek(0,0)
	data_write = open(out, "wb")
	for data in data_read:
		for dataByte in data:
			byte = byte + 1
			if byte > 1 and byte < 33+1:
				continue
			else:
				data_write.write(bytes([dataByte]))
	data_write.close()
	data_read.close()

# 提示信息
def showInfo(evt):
	fm_info['text'] = 'Made by copcap'

def hideInfo(evt):
	fm_info['text'] = 'i'


if __name__ == '__main__':
	# 创建主窗体
	window = tk.Tk()
	window.title('手杀图片解密')
	window.config(bg='#F0F0F0')
	window.resizable(width=False,
					height=False)
	# window.iconbitmap('')
	window.geometry('280x176')

	global lock
	lock = threading.Lock()

	fm = tk.Frame(window)
	
	fm_label1 = tk.Label(fm, text='加密图片文件路径')
	fm_label1.grid(row=0, column=0,
				   padx=2, pady=(8,2), sticky=tk.W)

	fm_button1 = tk.Button(fm, text='打开', width=8,
						   height=1, command=loadFilePath)
	fm_button1.grid(row=0, column=0,
					pady=(8,2), sticky=tk.E)

	fm_entry_text1 = tk.StringVar()
	fm_entry1 = tk.Entry(fm, width=38, textvariable=fm_entry_text1,
						 validate='focusout', validatecommand=lambda: pathStringCheck(fm_entry1))
	fm_entry1.grid(row=1, column=0,
				   padx=2, pady=2, sticky=tk.W)

	fm_label2 = tk.Label(fm, text='解密图片导出路径')
	fm_label2.grid(row=2, column=0,
				   padx=2, pady=5, sticky=tk.W)

	fm_button2 = tk.Button(fm, text='打开', width=8,
						   height=1, command=saveFilePath)
	fm_button2.grid(row=2, column=0,
					pady=2, sticky=tk.E)

	fm_entry_text2 = tk.StringVar()
	fm_entry2 = tk.Entry(fm, width=38, textvariable=fm_entry_text2,
						 validate='focusout', validatecommand=lambda: pathStringCheck(fm_entry2))
	fm_entry2.grid(row=3, column=0,
				   padx=2, pady=2, sticky=tk.W)

	fm_info = tk.Label(fm, text='i', width=15, anchor='e',
		    		   font=('Arial',9))
	fm_info.grid(row=4, column=0, sticky=tk.NE,
					pady=(30,0))
	fm_info.bind("<Enter>", showInfo)
	fm_info.bind("<Leave>", hideInfo)

	fm_button3 = tk.Button(fm, text='解包', width=10,
						   command=clickProgression)
	fm_button3.grid(row=4,
					pady=10)
	
	fm.pack()
	window.mainloop()