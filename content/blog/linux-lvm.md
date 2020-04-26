---
title: linux-LVM
date: 2010-12-27
author: admin
category: linux
tags: ['linux']
slug: linux-lvm
---

# 什么是 lvm？

lvm 即 logical volume
management（逻辑卷管理），是一种灵活组织磁盘和分区的方式，最大的优势在于可以打破磁盘和分区的界限随意的拓展逻辑卷的大小。原先如果分区不够用了只能备份数据重新分区再还原数据，而使用 lvm 可以动态的放大一个卷甚至也不需要 umount 下来直接在线拓展分区大小，这对于服务器来说是很不错的功能。

# lvm 是如何工作的？

首先了解几个概念： \*
pv（物理卷）用于创建 vg（逻辑卷组）的卷，需要将普通分区的类型改成 8e。 \*
vg（逻辑卷组）由多个物理卷组成一个大的卷，可以把他想象成一个磁盘，只是这个磁盘时逻辑上的跨越了物理磁盘和分区。 \* lv（逻辑卷）在 vg 上创建的逻辑卷，可以想象成 vg 的分区。
然后，lv 大小的更改是通过增减 pe 实现的，pe 是 vg 和 lv 的基本单位，vg 通过在添加的 pv 上创建 pe 来增加自身大小，然后通过增减分配给 lv 的 pe 数来控制 lv 的大小，基本原理图如下：

[![lvm](/wp-content/uploads/2010/12/lvm.jpg 'lvm')](/wp-content/uploads/2010/12/lvm.jpg)

# 相关命令有哪些？

- 物理分区相关：fdisk pv 相关：pvcreate，pvscan，pvdispaly，pvremove
- vg 相关：vgcreate，vgscan，vgdisplay，vgextend，vgreduce，vgchange，vgremove
- lv 相关：lvcreate，lvscan，lvdisplay，lvextend，lvreduce，lvremove，lvresize

# 如何创建逻辑卷以及调整逻辑卷大小？

下面是一个全程实例演示了如何创建，扩大和缩小 lv

## 分区并更改分区类型

    [root@localhost ~]# fdisk /dev/hda

    The number of cylinders for this disk is set to 19929.
    There is nothing wrong with that, but this is larger than 1024,
    and could in certain setups cause problems with:
    1) software that runs at boot time (e.g., old versions of LILO)
    2) booting and partitioning software from other OSs
    (e.g., DOS FDISK, OS/2 FDISK)
    Command (m for help): m
    Command action
    a toggle a bootable flag
    b edit bsd disklabel
    c toggle the dos compatibility flag
    d delete a partition
    l list known partition types
    m print this menu
    n add a new partition
    o create a new empty DOS partition table
    p print the partition table
    q quit without saving changes
    s create a new empty Sun disklabel
    t change a partition’s system id
    u change display/entry units
    v verify the partition table
    w write table to disk and exit
    x extra functionality (experts only)
    Command (m for help): p
    Disk /dev/hda: 163.9 GB, 163928604672 bytes
    255 heads, 63 sectors/track, 19929 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Device Boot Start End Blocks Id System
    /dev/hda1 * 1 2432 19535008+ 83 Linux
    /dev/hda2 2433 4864 19535040 83 Linux
    /dev/hda3 4865 19696 119138040 83 Linux
    /dev/hda4 19697 19929 1871572+ 82 Linux swap / Solaris
    Command (m for help): d
    Partition number (1-5): 3
    Command (m for help): p
    Disk /dev/hda: 163.9 GB, 163928604672 bytes
    255 heads, 63 sectors/track, 19929 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Device Boot Start End Blocks Id System
    /dev/hda1 * 1 2432 19535008+ 83 Linux
    /dev/hda2 2433 4864 19535040 83 Linux
    /dev/hda4 19697 19929 1871572+ 82 Linux swap / Solaris
    Command (m for help): n
    Command action
    e extended
    p primary partition (1-4)
    e
    Selected partition 3
    First cylinder (4865-19929, default 4865):
    Using default value 4865
    Last cylinder or +size or +sizeM or +sizeK (4865-19696, default 19696):
    Using default value 19696
    Command (m for help): p
    Disk /dev/hda: 163.9 GB, 163928604672 bytes
    255 heads, 63 sectors/track, 19929 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Device Boot Start End Blocks Id System
    /dev/hda1 * 1 2432 19535008+ 83 Linux
    /dev/hda2 2433 4864 19535040 83 Linux
    /dev/hda3 4865 19696 119138040 5 Extended
    /dev/hda4 19697 19929 1871572+ 82 Linux swap / Solaris
    Command (m for help): n
    First cylinder (4865-19696, default 4865):
    Using default value 4865
    Last cylinder or +size or +sizeM or +sizeK (4865-19696, default 19696): +20000M
    Command (m for help): p
    Disk /dev/hda: 163.9 GB, 163928604672 bytes
    255 heads, 63 sectors/track, 19929 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Device Boot Start End Blocks Id System
    /dev/hda1 * 1 2432 19535008+ 83 Linux
    /dev/hda2 2433 4864 19535040 83 Linux
    /dev/hda3 4865 19696 119138040 5 Extended
    /dev/hda4 19697 19929 1871572+ 82 Linux swap / Solaris
    /dev/hda5 4865 7297 19543041 83 Linux
    Command (m for help): n
    First cylinder (7298-19696, default 7298):
    Using default value 7298
    Last cylinder or +size or +sizeM or +sizeK (7298-19696, default 19696): +20000M
    Command (m for help): t
    Partition number (1-6): 5
    Hex code (type L to list codes): L
    0 Empty 1e Hidden W95 FAT1 80 Old Minix bf Solaris
    1 FAT12 24 NEC DOS 81 Minix / old Lin c1 DRDOS/sec (FAT-
    2 XENIX root 39 Plan 9 82 Linux swap / So c4 DRDOS/sec (FAT-
    3 XENIX usr 3c PartitionMagic 83 Linux c6 DRDOS/sec (FAT-
    4 FAT16 5 Extended 41 PPC PReP Boot 85 Linux extended da Non-FS data
    6 FAT16 42 SFS 86 NTFS volume set db CP/M / CTOS / .
    7 HPFS/NTFS 4d QNX4.x 87 NTFS volume set de Dell Utility
    8 AIX 4e QNX4.x 2nd part 88 Linux plaintext df BootIt
    9 AIX bootable 4f QNX4.x 3rd part 8e Linux LVM e1 DOS access
    a OS/2 Boot Manag 50 OnTrack DM 93 Amoeba e3 DOS R/O
    b W95 FAT32 51 OnTrack DM6 Aux 94 Amoeba BBT e4 SpeedStor
    c W95 FAT32 (LBA) 52 CP/M 9f BSD/OS eb BeOS fs
    e W95 FAT16 (LBA) 53 OnTrack DM6 Aux a0 IBM Thinkpad hi ee EFI GPT
    f W95 Ext’d (LBA) 54 OnTrackDM6 a5 FreeBSD ef EFI (FAT-12/16/
    10 OPUS 55 EZ-Drive a6 OpenBSD f0 Linux/PA-RISC b
    11 Hidden FAT12 56 Golden Bow a7 NeXTSTEP f1 SpeedStor
    12 Compaq diagnost 5c Priam Edisk a8 Darwin UFS f4 SpeedStor
    14 Hidden FAT16 16 Hidden FAT16 63 GNU HURD or Sys ab Darwin boot fb VMware VMFS
    17 Hidden HPFS/NTF 64 Novell Netware b7 BSDI fs fc VMware VMKCORE
    18 AST SmartSleep 65 Novell Netware b8 BSDI swap fd Linux raid auto
    1b Hidden W95 FAT3 70 DiskSecure Mult bb Boot Wizard hid fe LANstep
    1c Hidden W95 FAT3 75 PC/IX be Solaris boot ff BBT
    Hex code (type L to list codes): 8e *将文件系统类型改为LVM*
    Changed system type of partition 5 to 8e (Linux LVM)
    Command (m for help): t
    Partition number (1-6): 6
    Hex code (type L to list codes): 8e
    Changed system type of partition 6 to 8e (Linux LVM)
    Command (m for help): w
    The partition table has been altered!
    Calling ioctl() to re-read partition table.
    WARNING: Re-reading the partition table failed with error 16: Device or
    resource busy.
    The kernel still uses the old table.
    The new table will be used at the next reboot.
    Syncing disks.

## 更新磁盘分区表

    [root@localhost ~]# partprobe
    Warning: Unable to open /dev/fd0 read-write (Read-only file system). /dev/fd0
    has been opened read-only.
    [root@localhost ~]# fdisk -l
    Disk /dev/hda: 163.9 GB, 163928604672 bytes
    255 heads, 63 sectors/track, 19929 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Device Boot Start End Blocks Id System
    /dev/hda1 * 1 2432 19535008+ 83 Linux
    /dev/hda2 2433 4864 19535040 83 Linux
    /dev/hda3 4865 19696 119138040 5 Extended
    /dev/hda4 19697 19929 1871572+ 82 Linux swap / Solaris
    /dev/hda5 4865 7297 19543041 8e Linux LVM
    /dev/hda6 7298 9730 19543041 8e Linux LVM

## 创建物理卷

    [root@localhost ~]# pvcreate /dev/hda{5,6}
    Physical volume “/dev/hda5″ successfully created
    Physical volume “/dev/hda6″ successfully created
    [root@localhost ~]# pvscan
    PV /dev/hda5 lvm2 [18.64 GB]
    PV /dev/hda6 lvm2 [18.64 GB]
    Total: 2 [37.28 GB] / in use: 0 [0 ] / in no VG: 2 [37.28 GB]
    [root@localhost ~]# pvdisplay
    “/dev/hda5″ is a new physical volume of “18.64 GB”
    — NEW Physical volume —
    PV Name /dev/hda5
    VG Name
    PV Size 18.64 GB
    Allocatable NO
    PE Size (KByte) 0
    Total PE 0
    Free PE 0
    Allocated PE 0
    PV UUID J7pxmO-KO3K-CzpG-LIwW-loFF-0FV9-eSGlDD
    “/dev/hda6″ is a new physical volume of “18.64 GB”
    — NEW Physical volume —
    PV Name /dev/hda6
    VG Name
    PV Size 18.64 GB
    Allocatable NO
    PE Size (KByte) 0
    Total PE 0 还没有划分PE
    Free PE 0
    Allocated PE 0
    PV UUID sx2xgb-i6OW-G1OS-7VHu-yUc7-K18e-mHXfo6

## 创建 vg

    [root@localhost ~]# vgcreate -s 16M ftpvg /dev/hda{5,6}
    Volume group “ftpvg” successfully created
    [root@localhost ~]# vgscan
    Reading all physical volumes. This may take a while…
    Found volume group “ftpvg” using metadata type lvm2
    [root@localhost ~]# pvscan
    PV /dev/hda5 VG ftpvg lvm2 [18.62 GB / 18.62 GB free]
    PV /dev/hda6 VG ftpvg lvm2 [18.62 GB / 18.62 GB free]
    Total: 2 [37.25 GB] / in use: 2 [37.25 GB] / in no VG: 0 [0 ]

## 查看 vg 信息

    [root@localhost ~]# vgdisplay
    — Volume group —
    VG Name ftpvg
    System ID
    Format lvm2
    Metadata Areas 2
    Metadata Sequence No 1
    VG Access read/write
    VG Status resizable
    MAX LV 0
    Cur LV 0
    Open LV 0
    Max PV 0
    Cur PV 2
    Act PV 2
    VG Size 37.25 GB
    PE Size 16.00 MB
    Total PE 2384 已经划分了PE
    Alloc PE / Size 0 / 0
    Free PE / Size 2384 / 37.25 GB
    VG UUID OznWAr-uGaq-pLPy-OvkQ-MiS1-NDvk-bVAg1J

## 创建 lv

    [root@localhost ~]# lvcreate -L 30G -n ftplv ftpvg
    Logical volume “ftplv” created
    [root@localhost ~]# vgdisplay
    — Volume group —
    VG Name ftpvg
    System ID
    Format lvm2
    Metadata Areas 2
    Metadata Sequence No 2
    VG Access read/write
    VG Status resizable
    MAX LV 0
    Cur LV 1
    Open LV 0
    Max PV 0
    Cur PV 2
    Act PV 2
    VG Size 37.25 GB
    PE Size 16.00 MB
    Total PE 2384
    Alloc PE / Size 1920 / 30.00 GB
    Free PE / Size 464 / 7.25 GB
    VG UUID OznWAr-uGaq-pLPy-OvkQ-MiS1-NDvk-bVAg1J

## 在 lv 上创建文件系统

    [root@localhost ~]# mkfs -t ext3 /dev/ftpvg/ftplv
    mke2fs 1.39 (29-May-2006)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    3932160 inodes, 7864320 blocks
    393216 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=0
    240 block groups
    32768 blocks per group, 32768 fragments per group
    16384 inodes per group
    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
    4096000
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done
    This filesystem will be automatically checked every 36 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.

## 挂载文件系统写入文件

    [root@localhost ~]# mount /dev/ftpvg/ftplv /var/ftp/
    [root@localhost ~]# ls
    anaconda-ks.cfg Desktop ftp install.log install.log.syslog www.tgz
    [root@localhost ~]# cp www.tgz /var/ftp/
    [root@localhost ~]# df -h
    Filesystem Size Used Avail Use% Mounted on
    /dev/hda1 19G 7.0G 11G 41% /
    /dev/hda2 19G 2.0G 16G 12% /usr
    tmpfs 252M 0 252M 0% /dev/shm
    /dev/mapper/ftpvg-ftplv
    30G 528M 28G 2% /var/ftp

## 调整 lv 大小（按 pe 数扩大）

    [root@localhost ~]# lvresize -l +464 /dev/ftpvg/ftplv
    Extending logical volume ftplv to 37.25 GB
    Logical volume ftplv successfully resized
    [root@localhost ~]# vgdisplay
    — Volume group —
    VG Name ftpvg
    System ID
    Format lvm2
    Metadata Areas 2
    Metadata Sequence No 3
    VG Access read/write
    VG Status resizable
    MAX LV 0
    Cur LV 1
    Open LV 1
    Max PV 0
    Cur PV 2
    Act PV 2
    VG Size 37.25 GB
    PE Size 16.00 MB
    Total PE 2384
    Alloc PE / Size 2384 / 37.25 GB
    Free PE / Size 0 / 0 这里空闲的pe已经被使用
    VG UUID OznWAr-uGaq-pLPy-OvkQ-MiS1-NDvk-bVAg1J
    [root@localhost ~]# lvdisplay
    — Logical volume —
    LV Name /dev/ftpvg/ftplv
    VG Name ftpvg
    LV UUID HwZweC-La3M-8kUw-DXRB-7O62-DW7X-hIMRbM
    LV Write Access read/write
    LV Status available
    # open 1
    LV Size 37.25 GB
    Current LE 2384
    Segments 2
    Allocation inherit
    Read ahead sectors auto
    - currently set to 256
    Block device 253:0
    [root@localhost ~]# df -h
    Filesystem Size Used Avail Use% Mounted on
    /dev/hda1 19G 7.0G 11G 41% /
    /dev/hda2 19G 2.0G 16G 12% /usr
    tmpfs 252M 0 252M 0% /dev/shm
    /dev/mapper/ftpvg-ftplv
    30G 528M 28G 2% /var/ftp

## 调整文件系统大小

    [root@localhost ~]# resize2fs /dev/ftpvg/ftplv
    resize2fs 1.39 (29-May-2006)
    Filesystem at /dev/ftpvg/ftplv is mounted on /var/ftp; on-line resizing
    required
    Performing an on-line resize of /dev/ftpvg/ftplv to 9764864 (4k) blocks.
    The filesystem on /dev/ftpvg/ftplv is now 9764864 blocks long.
    [root@localhost ~]# df -h
    Filesystem Size Used Avail Use% Mounted on
    /dev/hda1 19G 7.0G 11G 41% /
    /dev/hda2 19G 2.0G 16G 12% /usr
    tmpfs 252M 0 252M 0% /dev/shm
    /dev/mapper/ftpvg-ftplv
    37G 532M 35G 2% /var/ftp

所有工作都是在没有 umount 文件系统前提下在线完成的，这也是 lvm 的强大之处

## 卸载逻辑卷

    [root@localhost ~]# umount /var/ftp/ 放大lv可以在线进行，而缩小lv则要umount后进行
    [root@localhost ~]# pvscan
    PV /dev/hda5 VG ftpvg lvm2 [18.62 GB / 0 free]
    PV /dev/hda6 VG ftpvg lvm2 [18.62 GB / 0 free]
    Total: 2 [37.25 GB] / in use: 2 [37.25 GB] / in no VG: 0 [0 ]
    You have new mail in /var/spool/mail/root

## 扫描 lv

    [root@localhost ~]# e2fsck -f /dev/ftpvg/ftplv
    e2fsck 1.39 (29-May-2006)
    Pass 1: Checking inodes, blocks, and sizes
    Pass 2: Checking directory structure
    Pass 3: Checking directory connectivity
    Pass 4: Checking reference counts
    Pass 5: Checking group summary information
    /dev/ftpvg/ftplv: 12/4882432 files (8.3% non-contiguous), 289173/9764864 blocks
    [root@localhost ~]# resize2fs /dev/ftpvg/ftplv 30000M 缩小文件系统大小
    resize2fs 1.39 (29-May-2006)
    Resizing the filesystem on /dev/ftpvg/ftplv to 7680000 (4k) blocks.
    The filesystem on /dev/ftpvg/ftplv is now 7680000 blocks long.
    [root@localhost ~]# df -h
    Filesystem Size Used Avail Use% Mounted on
    /dev/hda1 19G 7.0G 11G 41% /
    /dev/hda2 19G 2.0G 16G 12% /usr
    tmpfs 252M 0 252M 0% /dev/shm
    [root@localhost ~]# mount /dev/ftpvg/ftplv /var/ftp/ 再挂在上看到确实缩小了，但是lv还没有缩小
    [root@localhost ~]# df -h
    Filesystem Size Used Avail Use% Mounted on
    /dev/hda1 19G 7.0G 11G 41% /
    /dev/hda2 19G 2.0G 16G 12% /usr
    tmpfs 252M 0 252M 0% /dev/shm
    /dev/mapper/ftpvg-ftplv
    29G 528M 28G 2% /var/ftp
    [root@localhost ~]# ls /var/ftp/
    lost+found www.tgz
    [root@localhost ~]# vgdisplay
    — Volume group —
    VG Name ftpvg
    System ID
    Format lvm2
    Metadata Areas 2
    Metadata Sequence No 3
    VG Access read/write
    VG Status resizable
    MAX LV 0
    Cur LV 1
    Open LV 1
    Max PV 0
    Cur PV 2
    Act PV 2
    VG Size 37.25 GB
    PE Size 16.00 MB
    Total PE 2384
    Alloc PE / Size 2384 / 37.25 GB
    Free PE / Size 0 / 0 由于lv没有缩小，这里的pe还是被全部使用
    VG UUID OznWAr-uGaq-pLPy-OvkQ-MiS1-NDvk-bVAg1J
    [root@localhost ~]# lvdisplay
    — Logical volume —
    LV Name /dev/ftpvg/ftplv
    VG Name ftpvg
    LV UUID HwZweC-La3M-8kUw-DXRB-7O62-DW7X-hIMRbM
    LV Write Access read/write
    LV Status available
    # open 1
    LV Size 37.25 GB 可以看到lv没有缩小
    Current LE 2384
    Segments 2
    Allocation inherit
    Read ahead sectors auto
    - currently set to 256
    Block device 253:0

## 缩小 lv

    [root@localhost ~]# lvresize -l -464 /dev/ftpvg/ftplv
    WARNING: Reducing active and open logical volume to 30.00 GB
    THIS MAY DESTROY YOUR DATA (filesystem etc.)
    Do you really want to reduce ftplv? [y/n]: y
    Reducing logical volume ftplv to 30.00 GB
    Logical volume ftplv successfully resized
    [root@localhost ~]# lvdisplay
    — Logical volume —
    LV Name /dev/ftpvg/ftplv
    VG Name ftpvg
    LV UUID HwZweC-La3M-8kUw-DXRB-7O62-DW7X-hIMRbM
    LV Write Access read/write
    LV Status available
    # open 1
    LV Size 30.00 GB
    Current LE 1920
    Segments 2
    Allocation inherit
    Read ahead sectors auto
    - currently set to 256
    Block device 253:0
    [root@localhost ~]# vgdisplay
    — Volume group —
    VG Name ftpvg
    System ID
    Format lvm2
    Metadata Areas 2
    Metadata Sequence No 4
    VG Access read/write
    VG Status resizable
    MAX LV 0
    Cur LV 1
    Open LV 1
    Max PV 0
    Cur PV 2
    Act PV 2
    VG Size 37.25 GB
    PE Size 16.00 MB
    Total PE 2384
    Alloc PE / Size 1920 / 30.00 GB
    Free PE / Size 464 / 7.25 GB 由于lv的缩小，vg里也有了剩余的pe
    VG UUID OznWAr-uGaq-pLPy-OvkQ-MiS1-NDvk-bVAg1J
    [root@localhost ~]# pvdisplay
    — Physical volume —
    PV Name /dev/hda5
    VG Name ftpvg
    PV Size 18.64 GB / not usable 13.00 MB
    Allocatable yes (but full)
    PE Size (KByte) 16384
    Total PE 1192
    Free PE 0
    Allocated PE 1192
    PV UUID J7pxmO-KO3K-CzpG-LIwW-loFF-0FV9-eSGlDD
    — Physical volume —
    PV Name /dev/hda6
    VG Name ftpvg
    PV Size 18.64 GB / not usable 13.00 MB
    Allocatable yes
    PE Size (KByte) 16384
    Total PE 1192
    Free PE 464 这是vg中没有使用的pe对应的pv中没有使用的pe
    Allocated PE 728
    PV UUID sx2xgb-i6OW-G1OS-7VHu-yUc7-K18e-mHXfo6

## 新建一个 lv,过程一样

    [root@localhost ~]# lvcreate -l 464 -n wwwlv ftpvg
    Logical volume “wwwlv” created
    [root@localhost ~]# vgdisplay
    — Volume group —
    VG Name ftpvg
    System ID
    Format lvm2
    Metadata Areas 2
    Metadata Sequence No 5
    VG Access read/write
    VG Status resizable
    MAX LV 0
    Cur LV 2
    Open LV 1
    Max PV 0
    Cur PV 2
    Act PV 2
    VG Size 37.25 GB
    PE Size 16.00 MB
    Total PE 2384
    Alloc PE / Size 2384 / 37.25 GB
    Free PE / Size 0 / 0
    VG UUID OznWAr-uGaq-pLPy-OvkQ-MiS1-NDvk-bVAg1J
    [root@localhost ~]# lvdisplay
    — Logical volume —
    LV Name /dev/ftpvg/ftplv
    VG Name ftpvg
    LV UUID HwZweC-La3M-8kUw-DXRB-7O62-DW7X-hIMRbM
    LV Write Access read/write
    LV Status available
    # open 1
    LV Size 30.00 GB
    Current LE 1920
    Segments 2
    Allocation inherit
    Read ahead sectors auto
    - currently set to 256
    Block device 253:0
    — Logical volume —
    LV Name /dev/ftpvg/wwwlv
    VG Name ftpvg
    LV UUID P5RH8f-Apyo-Bi36-gXkG-kvv0-ErQp-0YlxLu
    LV Write Access read/write
    LV Status available
    # open 0
    LV Size 7.25 GB
    Current LE 464
    Segments 1
    Allocation inherit
    Read ahead sectors auto
    - currently set to 256
    Block device 253:1
    [root@localhost ~]# mkfs -t ext3 /dev/ftpvg/wwwlv
    mke2fs 1.39 (29-May-2006)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    950272 inodes, 1900544 blocks
    95027 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=1946157056
    58 block groups
    32768 blocks per group, 32768 fragments per group
    16384 inodes per group
    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done
    This filesystem will be automatically checked every 33 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.
    [root@localhost ~]# mkdir /var/www
    [root@localhost ~]# mount /dev/ftpvg/wwwlv /var/www/
    [root@localhost ~]# ls /var/www/
    lost+found
    [root@localhost ~]# df -h
    Filesystem Size Used Avail Use% Mounted on
    /dev/hda1 19G 7.0G 11G 41% /
    /dev/hda2 19G 2.0G 16G 12% /usr
    tmpfs 252M 0 252M 0% /dev/shm
    /dev/mapper/ftpvg-ftplv
    29G 528M 28G 2% /var/ftp
    /dev/mapper/ftpvg-wwwlv
    7.2G 145M 6.7G 3% /var/www

至此实例演示完成，没有演示到的是用 vgextend 和 vgreduce 命令增减 pv。
