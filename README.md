

# AutoBooter-Linux

A tiny Linux tool that automatically detects the **MediaTek Preloader** USB port and sends the correct boot command (FASTBOOT / METAMETA / FACTFACT, etc.) without needing to manually pick the serial port.

Perfect for MTK devices that keep connecting/disconnecting as "`MT65xx Preloader`".

---

## 🚀 Usage

Run:

```bash
python mtk-auto-boot FASTBOOT
```



The tool will:

1. Wait for the MTK preloader VID/PID → `0e8d:2000`
2. Auto-detect `/dev/ttyACM*`
3. Send the boot sequence until the device confirms it

Then it exits.

---

## 📦 Install

Requirements:

```bash
sudo apt install python3-serial
```

Make it executable:

```bash
chmod +x mtk_auto_boot.py
```

(If you installed the packaged version, it’s already available as `mtk-auto-boot`.)

---

## 🔧 Permissions

If you get:

```
Permission denied: '/dev/ttyACM0'
```

Add your user to the `dialout` group:

```bash
sudo usermod -aG dialout $USER
```

Log out & back in.

---

## 🧩 Why?

MediaTek preloaders flash on/off constantly.
This script removes the guesswork and automates the boot-sequence handshake so you can quickly enter FASTBOOT or META mode.



If you want a cleaner or fancier version later (badge style, logo, screenshots), I can bump it up.
