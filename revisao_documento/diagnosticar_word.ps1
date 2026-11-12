param([int]$WordProcessId)
Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Text;
public class WordWindowReader {
    public delegate bool EnumProc(IntPtr hwnd, IntPtr value);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc callback, IntPtr value);
    [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr hwnd, EnumProc callback, IntPtr value);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hwnd, out uint id);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hwnd, StringBuilder text, int count);
    public static void Read(int process) {
        EnumWindows((hwnd, value) => {
            uint id; GetWindowThreadProcessId(hwnd, out id);
            if (id == process) {
                var title = new StringBuilder(2048); GetWindowText(hwnd,title,2048);
                Console.WriteLine(hwnd.ToString()+": "+title);
                EnumChildWindows(hwnd,(child, arg) => {
                    var t=new StringBuilder(2048); GetWindowText(child,t,2048);
                    if(t.Length>0) Console.WriteLine("  "+child.ToString()+": "+t);
                    return true;
                },IntPtr.Zero);
            }
            return true;
        },IntPtr.Zero);
    }
}
'@
[WordWindowReader]::Read($WordProcessId)
