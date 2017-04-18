dofile("wifi.lua")
reg={}
----------------------------------------/
-- LSM9DS1 Accel/Gyro (XL/G) Registers --
----------------------------------------/
reg.ACT_THS=0x04
reg.ACT_DUR=0x05
reg.INT_GEN_CFG_XL=0x06
reg.INT_GEN_THS_X_XL=0x07
reg.INT_GEN_THS_Y_XL=0x08
reg.INT_GEN_THS_Z_XL=0x09
reg.INT_GEN_DUR_XL=0x0A
reg.REFERENCE_G=0x0B
reg.INT1_CTRL=0x0C
reg.INT2_CTRL=0x0D
reg.WHO_AM_I_XG=0x0F
reg.CTRL_REG1_G=0x10
reg.CTRL_REG2_G=0x11
reg.CTRL_REG3_G=0x12
reg.ORIENT_CFG_G=0x13
reg.INT_GEN_SRC_G=0x14
reg.OUT_TEMP_L=0x15
reg.OUT_TEMP_H=0x16
reg.STATUS_REG_0=0x17
reg.OUT_X_L_G=0x18
reg.OUT_X_H_G=0x19
reg.OUT_Y_L_G=0x1A
reg.OUT_Y_H_G=0x1B
reg.OUT_Z_L_G=0x1C
reg.OUT_Z_H_G=0x1D
reg.CTRL_REG4=0x1E
reg.CTRL_REG5_XL=0x1F
reg.CTRL_REG6_XL=0x20
reg.CTRL_REG7_XL=0x21
reg.CTRL_REG8=0x22
reg.CTRL_REG9=0x23
reg.CTRL_REG10=0x24
reg.INT_GEN_SRC_XL=0x26
reg.STATUS_REG_1=0x27
reg.OUT_X_L_XL=0x28
reg.OUT_X_H_XL=0x29
reg.OUT_Y_L_XL=0x2A
reg.OUT_Y_H_XL=0x2B
reg.OUT_Z_L_XL=0x2C
reg.OUT_Z_H_XL=0x2D
reg.FIFO_CTRL=0x2E
reg.FIFO_SRC=0x2F
reg.INT_GEN_CFG_G=0x30
reg.INT_GEN_THS_XH_G=0x31
reg.INT_GEN_THS_XL_G=0x32
reg.INT_GEN_THS_YH_G=0x33
reg.INT_GEN_THS_YL_G=0x34
reg.INT_GEN_THS_ZH_G=0x35
reg.INT_GEN_THS_ZL_G=0x36
reg.INT_GEN_DUR_G=0x37

--------------------------------
--LSM9DS1WHO_AM_IResponses--

reg.WHO_AM_I_AG_RSP=0x68
reg.WHO_AM_I_M_RSP=0x3D

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
    local data = i2c.read(id, 12)
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
    local c = i2c.read(id, 1)
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
    local c = i2c.write(id, write_value)
    i2c.stop(id)
end

-- set up accelerometer registers
function init_accel()
    -- set ctrl_reg5_xl
    local register_write_value = 0
    -- set Zen_XL, Yen_XL, Xen_XL bits to 1 enable each accelerometer
    register_write_value = bit.bor(register_write_value, bit.lshift(0x7, 3))
    write_reg_byte(0x6B, reg.CTRL_REG5_XL, register_write_value)
    write_reg_byte(0x6A, reg.CTRL_REG5_XL, register_write_value)


    -- set ctrl_reg6_xl
    register_write_value = 0
    -- set ODR_XL bits to 110 to set output data rate to 952 Hz
    register_write_value = bit.lshift(bit.band(6, 0x07), 5)
    -- set FS_XL bits to 11 to set accel scale to (+/-) 8g
    register_write_value = bit.bor(register_write_value, bit.lshift(0x3, 3))
    write_reg_byte(0x6B, reg.CTRL_REG6_XL, register_write_value)
    write_reg_byte(0x6A, reg.CTRL_REG6_XL, register_write_value)
    
    -- set ctrl_reg7_xl
    register_write_value = 0
    write_reg_byte(0x6B, reg.CTRL_REG7_XL, register_write_value)
    write_reg_byte(0x6A, reg.CTRL_REG7_XL, register_write_value)
    
end

-- set up gyro registers
function init_gyro()
    -- set ctrl_reg1_g
    local register_write_value = 0
    -- set ODR_G bitsto 110 to set output data rate to 952 Hz
    register_write_value = bit.lshift(bit.band(6, 0x07), 5)
    -- set FS_G bits to 01 to set gyro scale to (+/-) 500 dps
    register_write_value = bit.bor(register_write_value, bit.lshift(0x1, 3))
    write_reg_byte(0x6B, reg.CTRL_REG1_G, register_write_value)
    write_reg_byte(0x6A, reg.CTRL_REG1_G, register_write_value)
 
    -- set ctrl_reg2_g
    register_write_value = 0
    write_reg_byte(0x6B, reg.CTRL_REG2_G, register_write_value)
    write_reg_byte(0x6A, reg.CTRL_REG2_G, register_write_value)

    -- set ctrl_reg3_g
    register_write_value = 0
    write_reg_byte(0x6B, reg.CTRL_REG3_G, register_write_value)
    write_reg_byte(0x6A, reg.CTRL_REG3_G, register_write_value)
    
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
            temp1 = read_imu_data(0x6A)
            temp2 = read_imu_data(0x6B)

            -- get imu data from ch 2
            write_to_mux(0x02)
            temp3 = read_imu_data(0x6B)
            temp4 = read_imu_data(0x6A)
            
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

write_to_mux(0x01)
init_accel()
init_gyro()
write_to_mux(0x02)
init_accel()
init_gyro()

shot_num = 0
sample_num = 0
still_sending = false

-- session ID saved to "record.txt" and incremented on reset

if file.open("record.txt") then
    session = file.readline()
    session = session + 1
    file.close("record.txt")
else
    session = 1
end
file.open("record.txt", "w")
file.writeline(session)
file.close()

function firebase_put(data)

    -- set this to where you want to store each shot
    json_name = "DataSession" .. session
    
    firebase_str = "https://shotanalytics-17fc3.firebaseio.com/" .. json_name .. "/shot" .. shot_num .. ".json"
    print(firebase_str)
    print(data)
    http.post(firebase_str,
                nil,
                data,
                function(code,data)           
                if (code < 0) then
                  print("HTTP request failed")
                else
                  print(code, data)
                end
                
                if still_sending then
                    node.task.post(send_line)
                else
                    print("done!")
                end
  end)
    sample_num = sample_num + 1
end

function start_and_record_to_file()
    sample_num = 1
    file_name = "test.txt"
    -- first parameter is number of values to record
    record_to_file(100, file_name)
    gpio.write(3, gpio.LOW)
    print(node.heap())
    file.open(file_name)
    firebase_put_count = 1
    still_sending = true
    send_line()
end

function finish_recording()
    file.close()
    shot_num = shot_num + 1
    flash = true
    recording = false
    startup()
end

function send_line()

    line = file.readline()
    if (line == nil) then
        still_sending = false
        finish_recording()
        print("done!")
        return
    else
        firebase_put(line)
    end
end

function setup()
    print("setting up wifi")
    local status = wifi.sta.status()
    print(status)
    if status ~= 5 then
        wifi.setmode(wifi.STATION)
        print(wifi.sta.config(station_cfg))
        while (wifi.sta.status() ~= 5 )
        do
            print(wifi.sta.status())
            tmr.delay(1000000)
        end
    end

    print(wifi.sta.getip())
end


-- a button press can trigger an interrupt and be monitored for a continued press
-- wired to two pins
gpio.mode(5, gpio.INT, gpio.PULLUP)
gpio.mode(3, gpio.OUTPUT)

flash = true
on = false
recording = false
    
-- interrupt function, if pb is not held down a shot will begin recording
-- will continue triggering on pb press, but wont start a second recording
function pbpress(level, time)
    tmr.delay(1000000)
    if gpio.read(5)==1 then
        flash = false
        if recording == false then
            recording = true
            gpio.write(3, gpio.HIGH)
            start_and_record_to_file()
        end
    else    print("Abort")
    end
end

-- wait ~30 seconds before attempting to connect
function connect(level, time)
    gpio.write(3, gpio.HIGH)
    setup()
    startup()
end

-- LED flasher function
function flip(timer)
    if on == false then
        gpio.write(3, gpio.LOW)
        on = true
    else
        gpio.write(3, gpio.HIGH)
        on = false
    end
    if flash then
        tmr.alarm(0, 500, 0, flip)
    end
    if on == true and flash == false then
        gpio.write(3, gpio.HIGH)
        on = false
    end
end

-- prep for recording
function startup()
    gpio.trig(5, "down", pbpress)
    tmr.alarm(0,500,0,flip)
end

-- insert Network details (works better with MAC address)
--station_cfg.ssid = ""
--station_cfg.pwd = ""
--station_cfg.bssid = "AA:BB:CC:DD:EE:FF"
gpio.write(3, gpio.LOW)
gpio.trig(5, "down", connect)


