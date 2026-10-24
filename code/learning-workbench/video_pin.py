"""User-operated window picker for pinning a separately authenticated lecture."""
import ctypes,tkinter as tk
from ctypes import wintypes
from tkinter import ttk
user32=ctypes.WinDLL('user32',use_last_error=True)
user32.SetWindowPos.argtypes=[wintypes.HWND,wintypes.HWND,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,wintypes.UINT]
user32.SetWindowPos.restype=wintypes.BOOL
user32.GetWindowTextLengthW.argtypes=[wintypes.HWND]
user32.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int]
user32.IsWindowVisible.argtypes=[wintypes.HWND]
user32.GetWindowLongPtrW.argtypes=[wintypes.HWND,ctypes.c_int];user32.GetWindowLongPtrW.restype=ctypes.c_ssize_t
Callback=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
user32.EnumWindows.argtypes=[Callback,wintypes.LPARAM]
root=tk.Tk();root.title('讲座视频 · 置顶窗口');root.geometry('680x270')
items=[];pinned=set()
ttk.Label(root,text='先从Moodle打开录播，再把视频标签拖成独立浏览器窗口。',wraplength=630).pack(padx=20,pady=(20,8),anchor='w')
ttk.Label(root,text='选择下面的窗口置顶；切换PPT、知识库或编辑器时它仍会留在上面。',wraplength=630).pack(padx=20,anchor='w')
combo=ttk.Combobox(root,state='readonly',width=85);combo.pack(padx=20,pady=15)
status=ttk.Label(root,text='只改变你选中的窗口。');status.pack(padx=20,anchor='w')
def refresh():
 items.clear()
 @Callback
 def visit(hwnd,unused):
  if user32.IsWindowVisible(hwnd):
   size=user32.GetWindowTextLengthW(hwnd);buf=ctypes.create_unicode_buffer(size+1);user32.GetWindowTextW(hwnd,buf,size+1)
   title=buf.value
   if any(x in title.lower() for x in ['comp902','echovideo','echo360','lecture recordings']) and hwnd!=root.winfo_id():items.append((hwnd,title))
  return True
 user32.EnumWindows(visit,0);combo['values']=[title for _,title in items]
 if items:combo.current(0)
 status.config(text=f'找到{len(items)}个课程窗口；没有视频窗口时，先打开视频，再点刷新。')
def change(pin):
 i=combo.current()
 if i<0:return
 hwnd,title=items[i]
 was_topmost=bool(user32.GetWindowLongPtrW(hwnd,-20)&8)
 if not user32.SetWindowPos(hwnd,ctypes.c_void_p(-1 if pin else -2),0,0,0,0,0x0001|0x0002|0x0010):status.config(text='窗口已关闭或不可访问，请刷新后重选。');return
 if pin:
  if not was_topmost:pinned.add(hwnd)
 else:pinned.discard(hwnd)
 status.config(text=('已置顶：' if pin else '已取消置顶：')+title)
buttons=ttk.Frame(root);buttons.pack(pady=15)
for label,command in [('刷新窗口',refresh),('置顶所选视频',lambda:change(True)),('取消置顶',lambda:change(False))]:ttk.Button(buttons,text=label,command=command).pack(side='left',padx=8)
def close():
 for hwnd in pinned:user32.SetWindowPos(hwnd,ctypes.c_void_p(-2),0,0,0,0,0x0001|0x0002|0x0010)
 root.destroy()
root.protocol('WM_DELETE_WINDOW',close)
if __name__=='__main__':
 import sys
 if '--self-test' in sys.argv:
  root.title('COMP9024 video pin self test');root.update();refresh()
  target=next(i for i,(_,title) in enumerate(items) if title=='COMP9024 video pin self test')
  combo.current(target);hwnd=items[target][0]
  user32.GetWindowLongPtrW.argtypes=[wintypes.HWND,ctypes.c_int];user32.GetWindowLongPtrW.restype=ctypes.c_ssize_t
  change(True);assert user32.GetWindowLongPtrW(hwnd,-20)&8
  change(False);assert not user32.GetWindowLongPtrW(hwnd,-20)&8
  close();print('Own test window: pin and unpin passed')
 else:refresh();root.mainloop()
