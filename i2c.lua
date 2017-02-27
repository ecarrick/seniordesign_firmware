id  = 0
sda = 2
scl = 1
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
    register_write_value = bit.bor(register_write_value, bit.lshift(0x3, 3))
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

-- generic function to read either a gyro or accelerometer value from registers
function _read_imu_value(iic_address,lo_register, hi_register)

    lower_byte = string.byte(read_reg_byte(iic_address, lo_register))
    upper_byte = string.byte(read_reg_byte(iic_address, hi_register))

    -- shift upper byte over and add lower byte
    upper_byte = bit.lshift(upper_byte, 8)
    imu_value = bit.bor(upper_byte, lower_byte)

    -- convert unsigned to signed
    if (imu_value > 2^15) then
        imu_value = imu_value - 2^16
    end

    return imu_value
    
end

function read_x_accel()
    return _read_imu_value(0x6B, OUT_X_L_XL, OUT_X_H_XL)
end

function read_x_gyro()
    return _read_imu_value(0x6B, OUT_X_L_G, OUT_X_H_G)
end

function read_y_accel()
    return _read_imu_value(0x6B, OUT_Y_L_XL, OUT_Y_H_XL)
end

function read_y_gyro()
    return _read_imu_value(0x6B, OUT_Y_L_G, OUT_Y_H_G)
end

function read_z_accel()
    return _read_imu_value(0x6B, OUT_Z_L_XL, OUT_Z_H_XL)
end

function read_z_gyro()
    return _read_imu_value(0x6B, OUT_Z_L_G, OUT_Z_H_G)
end

init_accel()
temp_z_accel = read_z_accel()
print(temp_z_accel)
init_gyro()
temp_z_gyro = read_z_gyro()
print(temp_z_gyro)
