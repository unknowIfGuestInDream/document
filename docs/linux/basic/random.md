
## 生成64字节的二进制文件
```shell
dd if=/dev/random of=./dummy.bin bs=1 count=64
```

## 查看二进制文件内容
```shell
hexdump dummy.bin
hexdump -C dummy.bin
```