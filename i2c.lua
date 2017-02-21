id  = 0
sda = 2
scl = 1

-- initialize i2c, set pin1 as sda, set pin2 as scl
i2c.setup(id, sda, scl, i2c.SLOW)

-- user defined function: read from reg_addr content of dev_addr
function read_reg(dev_addr, reg_addr)
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.TRANSMITTER)
    i2c.write(id, reg_addr)
    i2c.stop(id)
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.RECEIVER)
    c = i2c.read(id, 4)
    i2c.stop(id)
    return c
end

-- get content of register 0x6B of device 0x15
tempL = read_reg(0x6B, 0x15)
tempH = read_reg(0x6B, 0x16)
print(string.byte(tempL))
print(string.byte(tempH))
