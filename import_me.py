from sshaolin.client import SSHClient

a = SSHClient("192.168.0.69", 6789, "root", look_for_keys=True)
print a.execute_command("ls")