# 🤝 Contribution guidelines

First off, thank you for considering contributing to Scitizen 🔬.

It is people like you that make Scitizen such a great project 🚀.

## 📘 Getting familiar with the project architecture

In order to get familiar with the architecture behind Scitizen, please read our [ARCHITECTURE](ARCHITECTURE.md) guide.

## 👨‍💻 Developing on a local device

The best way to extensively test the behavior of Scitizen is to test it directly on a physical device (like a Raspberry Pi).

In order to develop on a local device, follow these steps 👇

### 1️⃣ Setup your repository

[Fork](https://help.github.com/articles/fork-a-repo/) this repository to your own GitHub account and then [clone](https://help.github.com/articles/cloning-a-repository/) it to your local device.

### 2️⃣ Install `balena-cli`

You can find the installation instructions [here](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md).

### 3️⃣ List all device types that are supported

Run the command

```bash
balena devices supported
```

Example of output

```bash
SLUG                                   ALIASES                ARCH    NAME
asus-tinker-board                                             armv7hf Asus Tinker Board
asus-tinker-board-s                                           armv7hf Asus Tinker Board S
asus-tinker-edge-t                                            aarch64 ASUS Tinker Edge T
bananapi-m1-plus                                              armv7hf BananaPi-M1+
etcher-pro                                                    aarch64 Etcher Pro
fincm3                                                        armv7hf Balena Fin (CM3)
generic                                                       amd64   Generic
generic-aarch64                                               aarch64 Generic AARCH64
genericx86-64-ext                                             amd64   Generic x86_64
intel-edison                           edison                 i386    Intel Edison
intel-nuc                              nuc                    amd64   Intel NUC
jetson-nano                                                   aarch64 Nvidia Jetson Nano SD-CARD
jetson-nano-2gb-devkit                                        aarch64 Nvidia Jetson Nano 2GB Devkit SD
jetson-nano-emmc                                              aarch64 Nvidia Jetson Nano eMMC
jetson-tx1                                                    aarch64 Nvidia Jetson TX1
jetson-tx2                                                    aarch64 Nvidia Jetson TX2
jetson-tx2-nx-devkit                                          aarch64 Nvidia Jetson TX2 NX (with Xavier NX Devkit)
jetson-xavier                                                 aarch64 Nvidia Jetson Xavier
jetson-xavier-nx-devkit                                       aarch64 Nvidia Jetson Xavier NX Devkit SD-CARD
jetson-xavier-nx-devkit-emmc                                  aarch64 Nvidia Jetson Xavier NX Devkit eMMC
jetson-xavier-nx-devkit-seeed-2mic-hat                        aarch64 Nvidia Jetson Xavier NX Devkit SD Seeed ReSpeaker-2Mic
jn30b-nano                                                    aarch64 Auvidea JN30B Nano
odroid-c1                                                     armv7hf ODROID-C1+
odroid-xu4                             odroid-ux3, odroid-u3+ armv7hf ODROID-XU4
orange-pi-one                                                 armv7hf Orange Pi One
orange-pi-zero                                                armv7hf Orange Pi Zero
orangepi-plus2                                                armv7hf Orange Pi Plus2
raspberry-pi                           raspberrypi            rpi     Raspberry Pi (v1 / Zero / Zero W)
raspberry-pi2                          raspberrypi2           armv7hf Raspberry Pi 2
raspberrypi3                                                  armv7hf Raspberry Pi 3
raspberrypi3-64                                               aarch64 Raspberry Pi 3 (using 64bit OS)
raspberrypi4-64                                               aarch64 Raspberry Pi 4 (using 64bit OS)
raspberrypi400-64                                             aarch64 Raspberry Pi 400
raspberrypicm4-ioboard                                        aarch64 Raspberry Pi CM4 IO Board
surface-go                                                    amd64   Microsoft Surface Go
surface-pro-6                                                 amd64   Microsoft Surface 6
```

Then, find the SLUG matching your device (in our example, we'll take `raspberrypi4-64`).

### 4️⃣ Find the latest development version (.dev) available for your device

Run the command

```bash
balena os versions raspberrypi4-64
```

Example of output

```bash
v2.80.5+rev1.prod (recommended)
v2.80.5+rev1.dev
v2.80.3+rev1.prod
v2.80.3+rev1.dev
v2.75.0+rev1.prod
v2.75.0+rev1.dev
v2.73.1+rev1.prod
v2.73.1+rev1.dev
v2.71.5+rev1.prod
v2.71.5+rev1.dev
v2.71.3+rev1.prod
v2.71.3+rev1.dev
```

Then, find the latest development version (.dev) version (in our example, we'll take `v2.80.5+rev1.dev`).

### 5️⃣ Download the latest development version (.dev) available for your device

Run the command

```bash
balena os download raspberrypi4-64 --output scitizen-os-dev.img --version v2.80.5+rev1.dev
```

Example of output

```bash
Getting device operating system for raspberrypi4-64
Downloading Device OS 2.80.5+rev1.dev [========================] 100% eta 0s  
The image was downloaded successfully
```

### 6️⃣ Configure the image

Run the command

```bash
sudo balena local configure scitizen-os-dev.img
```

Example of output

```bash
? Network SSID My_Wifi_Ssid
? Network Key super_secret_wifi_password
? Do you want to set advanced settings? Yes
? Device Hostname scitizen
? Do you want to enable persistent logging? No
Done!
```

In `Device Hostname`, fill in `scitizen`.
If you need Wi-Fi, you can also set it up here.

### 7️⃣ Plug-in your micro-SD card and find the drive

Run the command

```bash
balena util available-drives
```

Example of output

```bash
DEVICE     SIZE    DESCRIPTION
/dev/disk2 31.9 GB Generic STORAGE DEVICE Media
```

In our example, the drive is `/dev/disk2`.

### 8️⃣ Flash the image

Run the command

```bash
sudo balena local flash scitizen-os-dev.img --drive /dev/disk2
```

Example of output

```bash
? This will erase the selected drive. Are you sure? Yes
Flashing [========================] 100% eta 0s
Validating [========================] 100% eta 0s
```

### 9️⃣ Plug-it in your device and power-it up

![Power it up tutorial](docs/assets/power-it-up.gif)

### 🔟 Scan your network for your device

Run the command

```bash
sudo balena scan
```

Example of output

```bash
Scanning for local balenaOS devices... Reporting scan results
- 
  host:          scitizen.local
  address:       192.168.0.25
  osVariant:     development
  dockerInfo: 
    Containers:        1
    ContainersRunning: 1
    ContainersPaused:  0
    ContainersStopped: 0
    Images:            2
    Driver:            overlay2
    SystemTime:        2021-08-25T11:57:56.229479306Z
    KernelVersion:     5.4.83-v8
    OperatingSystem:   balenaOS 2.80.5+rev1
    Architecture:      aarch64
  dockerVersion: 
    Version:    19.03.18
    ApiVersion: 1.40
```

In our example, the device hostname is `scitizen.local`.

### 1️⃣1️⃣ Push Scitizen on your device and start a live session

Run the command

```bash
balena push scitizen.local
```

Example of output

```bash
[Info]    Starting build on device 192.168.0.25
[Build]   [agent]    [==================================================>]  100.0MB/100.0MB
[Build]   [api]      [==================================================>]  100.0MB/100.0MB
[Build]   [app]      [==================================================>]  100.0MB/100.0MB
[Build]   [wifi]     [==================================================>]  100.0MB/100.0MB
[Build]   [worker]   [==================================================>]  100.0MB/100.0MB
[Info]    Streaming device logs...
[Live]    Watching for file changes...
[Live]    Waiting for device state to settle...
[Live]    Device state settled
[Logs]    [1/1/2021, 12:00:00] [app] Hello World!
...
[Logs]    [1/1/2021, 14:00:00] [app] Goodbye World!
```

Congratulations 🎉! You now have a live session where every changes you apply on the code will be build and pushed to your device.

### Optional: connect to your device via SSH

To connect to the Host OS, run the command

```bash
balena ssh scitizen.local
```

To connect to a specific service, run the command

```bash
balena ssh scitizen.local <service>
```

Example: `balena ssh scitizen.local app`

## 👨‍💻 Developing without a local device

It is also possible to contribute to Scitizen even if you do not have access to a physical device like a Raspberry Pi.

We will use a container image to emulate the Host OS.

In order to develop without a local device, follow these steps 👇

### 1️⃣ Setup your repository

[Fork](https://help.github.com/articles/fork-a-repo/) this repository to your own GitHub account and then [clone](https://help.github.com/articles/cloning-a-repository/) it to your local device.

### 2️⃣ Install `balena-cli`

You can find the installation instructions [here](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md).

### 3️⃣ Emulate Scitizen Host OS

Run the command

```bash
docker run \
--name scitizen_os \
--detach \
--interactive \
--tty \
--privileged \
--network host \
--restart always \
--tmpfs /run,/run/lock,/tmp,/var/lib/journal,/sys/fs/cgroup/systemd \
--volume /lib/modules:/lib/modules:ro \
ghcr.io/pcorbel/scitizen/development-os:latest
```

### 4️⃣ Scan your network for your device

Run the command

```bash
balena scan
```

Example of output

```bash
Scanning for local balenaOS devices... Reporting scan results
- 
  host:          f88f3cb.local
  address:       10.128.0.3
  osVariant:     development
  dockerInfo: 
    Containers:        1
    ContainersRunning: 1
    ContainersPaused:  0
    ContainersStopped: 0
    Images:            2
    Driver:            overlay2
    SystemTime:        2021-09-15T12:42:14.121444495Z
    KernelVersion:     4.19.0-17-cloud-amd64
    OperatingSystem:   balenaOS 2.83.18+rev1 (containerized)
    Architecture:      x86_64
  dockerVersion: 
    Version:    19.03.24
    ApiVersion: 1.40
```

In our example, the device address is `10.128.0.3`.

### 1️⃣1️⃣ Push Scitizen on your device and start a live session

Run the command

```bash
balena push 10.128.0.3
```

Example of output

```bash
[Info]    Starting build on device 10.128.0.3
[Build]   [agent]    [==================================================>]  100.0MB/100.0MB
[Build]   [api]      [==================================================>]  100.0MB/100.0MB
[Build]   [app]      [==================================================>]  100.0MB/100.0MB
[Build]   [wifi]     [==================================================>]  100.0MB/100.0MB
[Build]   [worker]   [==================================================>]  100.0MB/100.0MB
[Info]    Streaming device logs...
[Live]    Watching for file changes...
[Live]    Waiting for device state to settle...
[Live]    Device state settled
[Logs]    [1/1/2021, 12:00:00] [app] Hello World!
...
[Logs]    [1/1/2021, 14:00:00] [app] Goodbye World!
```

Congratulations 🎉! You now have a live session where every changes you apply on the code will be build and pushed to your device.

## 🙏 Open a pull request

When you're done making changes and you'd like to propose them for review, open your PR (pull request).

## 🕵️‍♂️ Submit your PR and get it reviewed

Once you submit your PR, others from the Scitizen community will review it with you.
After that, we may have questions, check back on your PR to keep up with the conversation.
Did you have an issue, like a merge conflict? Check out a [git tutorial](https://lab.github.com/githubtraining/managing-merge-conflicts) on how to resolve merge conflicts and other issues.

## 💪 Your PR is merged

Congratulations! The whole Scitizen community thanks you 🙏!

Once your PR is merged, you will be proudly listed as a contributor in the [contributor chart](https://github.com/pcorbel/scitizen/graphs/contributors) 🏅.
