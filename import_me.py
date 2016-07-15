from sshaolin.client import SSHClient

a = SSHClient("10.66.78.25", 22, "nath4854", look_for_keys=True, compress=False)
print(a.execute_command("ls /"))
