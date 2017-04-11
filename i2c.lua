dofile("reg.lua")
id  = 0
sda = 2
scl = 1

node.setcpufreq(node.CPU160MHZ)

-- initialize i2c, set pin1 as sda, set pin2 as scl
i2c.setup(id, sda, scl, i2c.SLOW)

function write_to_mux(val)
    i2c.start(id)
    -- setup the write for device
    i2c.address(id, 0x70, i2c.TRANSMITTER)
    -- write onto bus what register to be written
    i2c.write(id, val)
    -- write the value onto bus for specified register
    i2c.stop(id)
end

function read_imu_data(dev_addr)
    local data
   -- local out = {0, 0,  0, 0, 0, 0}
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.TRANSMITTER)
    i2c.write(id, reg.OUT_X_L_G)
    i2c.stop(id)
    i2c.start(id)
    i2c.address(id, dev_addr, i2c.RECEIVER)
    data = i2c.read(id, 12)
    i2c.stop(id)
    
    return data

end 

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
    -- set Zen_XL, Yen_XL, Xen_XL bits to 1 enable each accelerometer
    register_write_value = bit.bor(register_write_value, bit.lshift(0x7, 3))
    write_reg_byte(0x6B, reg.CTRL_REG5_XL, register_write_value)

    -- set ctrl_reg6_xl
    register_write_value = 0
    -- set ODR_XL bits to 110 to set output data rate to 952 Hz
    register_write_value = bit.lshift(bit.band(6, 0x07), 5)
    -- set FS_XL bits to 11 to set accel scale to (+/-) 8g
    register_write_value = bit.bor(register_write_value, bit.lshift(0x3, 3))
    write_reg_byte(0x6B, reg.CTRL_REG6_XL, register_write_value)
    
    -- set ctrl_reg7_xl
    register_write_value = 0
    write_reg_byte(0x6B, reg.CTRL_REG7_XL, register_write_value)
    
end

-- set up gyro registers
function init_gyro()
    -- set ctrl_reg1_g
    register_write_value = 0
    -- set ODR_G bitsto 110 to set output data rate to 952 Hz
    register_write_value = bit.lshift(bit.band(6, 0x07), 5)
    -- set FS_G bits to 01 to set gyro scale to (+/-) 500 dps
    register_write_value = bit.bor(register_write_value, bit.lshift(0x1, 3))
    write_reg_byte(0x6B, reg.CTRL_REG1_G, register_write_value)
 
    -- set ctrl_reg2_g
    register_write_value = 0
    write_reg_byte(0x6B, reg.CTRL_REG2_G, register_write_value)

    -- set ctrl_reg3_g
    register_write_value = 0
    write_reg_byte(0x6B, reg.CTRL_REG3_G, register_write_value)
    
end

-- read acc/gyro data through a low pass filter
-- gain is a positive integer that weighs previous calculation more heavily than raw data
function collect_filter(gain, prev)
    local y = {}
    y[1] = (read_x_accel() + gain * prev[1])/(gain + 1)
    y[2] = (read_y_accel() + gain * prev[2])/(gain + 1)
    y[3] = (read_z_accel() + gain * prev[3])/(gain + 1)
    y[4] = (read_x_gyro() + gain * prev[4])/(gain + 1)
    y[5] = (read_y_gyro() + gain * prev[5])/(gain + 1)
    y[6] = (read_z_gyro() + gain * prev[6])/(gain + 1)
    return y
end


-- 10000 samples should operate for ~10.5 seconds before timing out (*need pushbutton interrupt*)
-- we'll have to see if the truncation becomes a problem 
function record(calib_val, nsamp)
    gain = 3
    count = 1
    local y = {[1] = calib_val}
    while count < nsamp do
        y[count + 1] = collect_filter(gain, y[count])
        print(node.heap())
        tmr.wdclr()
        tmr.delay(1050)
        count = count + 1
    end
    return y
end

function record_to_file(nsamp, file_name)
    count = 1
    if file.open(file_name, "w") then
        print("start\n")
        local line = ""
        local linecount = 1
        while count < nsamp do
            -- get imu data from ch 1
            write_to_mux(0x01)
            temp1 = read_imu_data(0x6B)
            temp2 = read_imu_data(0x6B)

            -- get imu data from ch 2
            write_to_mux(0x02)
            temp3 = read_imu_data(0x6B)
            temp4 = read_imu_data(0x6B)
            
            tmr.wdclr()
            count = count + 1
            -- encode data into one line JSON format
            --line = cjson.encode({temp1, temp2, temp3, temp4})
            --print(line)
            --print(temp1)
            line = "[\"" ..encoder.toHex(temp1) .."\",\"".. encoder.toHex(temp2) .."\",\"".. encoder.toHex(temp3) .."\",\"".. encoder.toHex(temp4) .. "\"," .. tmr.now() .. "]"
            --print(line)
            -- write line to file
            file.writeline(line)
        end
    end
    file.close()
end

-- potential implementation of a calibration to set initial orientation with variable sensitivity for testing
-- sensitivity is in LSB 
function calibrate(sensitivity)
    clear = false
    local y
    while not clear do
        local x = {}
        x[1] = read_x_accel()
        x[2] = read_y_accel()
        x[3] = read_z_accel()
        x[4] = read_x_gyro()
        x[5] = read_y_gyro()
        x[6] = read_z_gyro()
        y = record(x, 5)
        a = (y[5][1] > -sensitivity and y[5][1] < sensitivity)
        b = (y[5][2] > -sensitivity and y[5][2] < sensitivity)
        c = (y[5][3] > 4096 - sensitivity and y[5][3] < 4096 + sensitivity)
        if a and b and c then clear = true end
    end
    return y[5]
end    
    
init_accel()
init_gyro()
-- calib = calibrate(300)
-- IMU = record(calib, 100)
-- print(IMU[50][1],IMU[50][3])
