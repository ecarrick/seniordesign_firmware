id  = 0
sda = 2
scl = 1
OUT_X_L_XL = 0x28 -- reg address for lower 8-bits of accel in x 
OUT_X_H_XL = 0x29 -- reg address for upper 8-bits of accel in x
OUT_Y_L_XL = 0x2A -- accel, lower 8-bits in y
OUT_Y_H_XL = 0x2B -- accel, upper 8-bits in y
OUT_Z_L_XL = 0x2C -- accel, lower 8-bits in z
OUT_Z_H_XL = 0x2D -- accel, upper 8-bits in z
CTRL_REG5_XL = 0x1F
CTRL_REG6_XL = 0x20
CTRL_REG7_XL = 0x21

-- initialize i2c, set pin1 as sda, set pin2 as scl
i2c.setup(id, sda, scl, i2c.SLOW)

-- user defined function: read single byte from reg_addr content of dev_addr
function read_reg_byte(dev_addr, reg_addr)
    i2c.start(id)  -- initialize i2c
    i2c.address(id, dev_addr, i2c.TRANSMITTER) -- set device to xmit
    i2c.write(id, reg_addr) -- need to send register value that you want on the bus, after that you can read data
    i2c.stop(id)
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.RECEIVER)
    c = i2c.read(id, 1)
    i2c.stop(id)
    return c
end

-- write value to specified address
function write_reg_byte(dev_addr, reg_addr, write_value)
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.TRANSMITTER)
    i2c.write(id, reg_addr)
    i2c.stop(id)
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.RECEIVER)
    c = i2c.write(id, write_value)
    i2c.stop(id)
end
  

-- set up accelerometer registers
function init_accel()
    -- set ctrl_reg5_xl
    register_write_value = 0
    register_write_value = bit.bor(register_write_value, bit.lshift(1, 5))
    register_write_value = bit.bor(register_write_value, bit.lshift(1, 4))
    register_write_value = bit.bor(register_write_value, bit.lshift(1, 3))
    write_reg_byte(0x6B, CTRL_REG5_XL, register_write_value)

    -- set ctrl_reg6_xl
    register_write_value = 0
    register_write_value = bit.bor(register_write_value, bit.lshift(0x07, 5))
    write_reg_byte(0x6B, CTRL_REG6_XL, register_write_value)
    
    -- set ctrl_reg7_xl
    register_write_value = 0
    write_reg_byte(0x6B, CTRL_REG6_XL, register_write_value)
    
end

-- read x acceleration
function read_x_accel()
    -- read lower and upper byte of accel data in x
    x_low = read_reg_byte(0x6B, OUT_X_L_XL)
    x_high = read_reg_byte(0x6B, OUT_X_H_XL)
    -- shift upper byte of accel data to the left and then or it with lower byte
    x_high = bit.lshift(x_high, 8)
    x_accel = bit.bor(x_high, x_low)
    
    return x_accel
end

-- read y acceleration
function read_y_accel()
    -- read lower and upper byte of accel data in y
    y_low = read_reg_byte(0x6B, OUT_Y_L_XL)
    y_high = read_reg_byte(0x6B, OUT_Y_H_XL)
    -- shift upper byte of accel data to the left and then or it with lower byte
    y_high = bit.lshift(y_high, 8)
    y_accel = bit.bor(y_high, y_low)
    
    return y_accel
end

-- read z acceleration
function read_z_accel()
    -- read lower and upper byte of accel data in z
    z_low = read_reg_byte(0x6B, OUT_Z_L_XL)
    z_high = read_reg_byte(0x6B, OUT_Z_H_XL)
    -- shift upper byte of accel data to the left and then or it with lower byte
    z_high = bit.lshift(z_high, 8)
    z_accel = bit.bor(z_high, z_low)
    
    return z_accel
end

-- get content of register 0x6B of device 0x15
init_accel()
temp_x = read_x_accel()
print(string.byte(temp_x))
