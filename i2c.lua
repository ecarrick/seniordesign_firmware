id  = 0
sda = 2
scl = 1
aRes = 0.000061
gRes = 0.00875
OUT_X_L_XL = 0x28 -- reg address for lower 8-bits of accel in x 
OUT_X_H_XL = 0x29 -- reg address for upper 8-bits of accel in x
OUT_Y_L_XL = 0x2A -- accel, lower 8-bits in y
OUT_Y_H_XL = 0x2B -- accel, upper 8-bits in y
OUT_Z_L_XL = 0x2C -- accel, lower 8-bits in z
OUT_Z_H_XL = 0x2D -- accel, upper 8-bits in z
OUT_X_L_G = 0x18
OUT_X_H_G = 0x19
OUT_Y_L_G = 0x1A
OUT_Y_H_G = 0x1B
OUT_Z_L_G = 0x1C
OUT_Z_H_G = 0x1D
CTRL_REG1_G = 0x10
CTRL_REG2_G = 0x11
CTRL_REG3_G = 0x12
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
    -- setup the write for device
    i2c.address(id, dev_addr, i2c.TRANSMITTER)
    -- write onto bus what register to be written
    i2c.write(id, reg_addr)
    -- write the value onto bus for specified register
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
    register_write_value = bit.lshift(bit.band(6, 0x07), 5)
    write_reg_byte(0x6B, CTRL_REG6_XL, register_write_value)
    
    -- set ctrl_reg7_xl
    register_write_value = 0
    write_reg_byte(0x6B, CTRL_REG7_XL, register_write_value)
    
end

-- set up gyro registers
function init_gyro()
    -- set ctrl_reg1_g
    register_write_value = 0
    register_write_value = bit.lshift(bit.band(6, 0x07), 5)
    write_reg_byte(0x6B, CTRL_REG1_G, register_write_value)
 
    -- set ctrl_reg2_g
    register_write_value = 0
    write_reg_byte(0x6B, CTRL_REG2_G, register_write_value)
    
    -- set ctrl_reg3_g
    register_write_value = 0
    write_reg_byte(0x6B, CTRL_REG3_G, register_write_value)
    
end

-- read x acceleration
function read_x_accel()
    -- read lower and upper byte of accel data in x
    x_low = string.byte(read_reg_byte(0x6B, OUT_X_L_XL))
    print(x_low)
    x_high = string.byte(read_reg_byte(0x6B, OUT_X_H_XL))
    print(x_high)
    -- shift upper byte of accel data to the left and then or it with lower byte
    x_high = bit.lshift(x_high, 8)
    x_accel = bit.bor(x_high, x_low)
    x_accel = x_accel * aRes
    return x_accel
end

function read_x_gyro()
    x_low = string.byte(read_reg_byte(0x6B, OUT_X_L_G))
    print(x_low)
    x_high = string.byte(read_reg_byte(0x6B, OUT_X_H_G))
    print(x_high)
    x_high = bit.lshift(x_high, 8)
    x_gyro = bit.bor(x_high, x_low)
    x_gyro = x_gyro * gRes
    return x_gyro
end

-- read y acceleration
function read_y_accel()
    -- read lower and upper byte of accel data in y
    y_low = string.byte(read_reg_byte(0x6B, OUT_Y_L_XL))
    y_high = string.byte(read_reg_byte(0x6B, OUT_Y_H_XL))
    -- shift upper byte of accel data to the left and then or it with lower byte
    y_high = bit.lshift(string.byte(y_high), 8)
    y_accel = bit.bor(y_high, y_low)
    y_accel = y_accel * aRes
    return y_accel
end

function read_y_gyro()
    y_low = string.byte(read_reg_byte(0x6B, OUT_Y_L_G))
    print(y_low)
    y_high = string.byte(read_reg_byte(0x6B, OUT_Y_H_G))
    print(y_high)
    y_high = bit.lshift(y_high, 8)
    y_gyro = bit.bor(y_high, y_low)
    y_gyro = y_gyro * gRes
    return y_gyro
end

-- read z acceleration
function read_z_accel()
    -- read lower and upper byte of accel data in z
    z_low = string.byte(read_reg_byte(0x6B, OUT_Z_L_XL))
    z_high = string.byte(read_reg_byte(0x6B, OUT_Z_H_XL))
    -- shift upper byte of accel data to the left and then or it with lower byte
    z_high = bit.lshift(z_high, 8)
    z_accel = bit.bor(z_high, z_low)
    z_accel = z_accel * aRes
    return z_accel
end

-- read g gyro
function read_z_gyro()
    z_low = string.byte(read_reg_byte(0x6B, OUT_Z_L_G))
    print(z_low)
    z_high = string.byte(read_reg_byte(0x6B, OUT_Z_H_G))
    print(z_high)
    z_high = bit.lshift(z_high, 8)
    z_gyro = bit.bor(z_high, z_low)
    z_gyro = z_gyro * gRes
    return z_gyro
end

-- get content of register 0x6B of device 0x15
init_accel()
temp_x = read_x_accel()
print(string.byte(temp_x))
init_gyro()
temp_x_gyro = read_x_gyro()
print(string.byte(temp_x_gyro))
