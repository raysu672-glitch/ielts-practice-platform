import os, sys, hashlib, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import paramiko
for line in open(".env.deploy", encoding="utf-8", errors="replace"):
    line=line.strip()
    if line.startswith("IELTS_") and "=" in line:
        k,v=line.split("=",1); os.environ[k.strip()]=v.strip()
host=os.environ["IELTS_DEPLOY_HOST"]; user=os.environ["IELTS_DEPLOY_USER"]
port=int(os.environ.get("IELTS_DEPLOY_PORT") or 22); root=(os.environ.get("IELTS_DEPLOY_DIR") or "/var/www/ielts").rstrip("/")
cli=paramiko.SSHClient(); cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
kw=dict(hostname=host,username=user,port=port,timeout=25)
if os.environ.get("IELTS_DEPLOY_KEY"): kw["key_filename"]=os.environ["IELTS_DEPLOY_KEY"]
if os.environ.get("IELTS_DEPLOY_PASSWORD"): kw["password"]=os.environ["IELTS_DEPLOY_PASSWORD"]
cli.connect(**kw); sftp=cli.open_sftp()

rel="sources/tinglidanciceshi/listening_basic.html"
local=rel.replace("/", os.sep); remote=f"{root}/{rel}"
lh=hashlib.md5(open(local,"rb").read()).hexdigest()
print("本地 md5 :", lh, "| 大小", os.path.getsize(local))

ts=time.strftime("%Y%m%d_%H%M%S")
bak=f"/tmp/listening_basic_bak_{ts}.html"
try:
    sftp.stat(remote)
    cli.exec_command(f"cp -p {remote} {bak}")[1].channel.recv_exit_status()
    print("线上原文件已备份 ->", bak)
    print("线上原 md5 :", hashlib.md5(sftp.open(remote,"rb").read()).hexdigest())
except IOError:
    print("线上不存在该文件，将新建")

sftp.put(local, remote)
print("已上传 ->", remote)
print("上传后 md5 :", hashlib.md5(sftp.open(remote,"rb").read()).hexdigest(), "(应与本地一致)")

# 属主/权限对齐（静态文件，确保 web 可读）
cli.exec_command(f"chmod 644 {remote}; chown www-data:www-data {remote}")[1].channel.recv_exit_status()
stdin,stdout,stderr=cli.exec_command(f"ls -l {remote}")
print(stdout.read().decode("utf-8","replace").strip())
cli.close()
