dofile("i2c.lua")
dofile("wifi.lua")

shot_num = 0

function firebase_put(data)

    -- set this to where you want to store each shot
    json_name = "testdata"
    
    firebase_str = "https://shotanalytics-17fc3.firebaseio.com/" .. json_name .. "/shot" .. shot_num .. ".json"
    print(firebase_str)
    
    http.post(firebase_str,
                nil,
                cjson.encode(data),
                function(code,data)
                if (code < 0) then
                  print("HTTP request failed")
                else
                  print(code, data)
    end
  end)
    shot_num = shot_num + 1
end

function start()
    calib = calibrate(500)
    counter = 0
    while counter < 1 do

        print(counter)
        -- having trouble recording/sending more than about 20 samples
        local data = record(calib, 20)
        firebase_put(data)
        tmr.delay(5000000)
        counter = counter+1
    end
    --uncomment next line to send recording to firebase
    --firebase_put(data)
end

function start_and_record_to_file()
    
    file_name = "test.txt"
    -- first parameter is number of values to record
    record_to_file(5, file_name)
    file.open(file_name)

    firebase_put_count = 1
    firebase_table = {}
    while true do
        line = file.readline()
        if (line == nil) then break
        end
        value_count = 1
        value_table = {}
        -- parse values from text file, this regex extracts each integer
        -- "-?" finds optional - sign in case integer is negative, "d+" fids integer and stops at next non integer char.,
        -- in this case a comma
        for val in string.gmatch(line, "-?%d+") do
            value_table[value_count] = val
            value_count = value_count + 1
            print(val)
        end
        firebase_table[firebase_put_count] = value_table
        firebase_put_count = firebase_put_count + 1
        tmr.wdclr()
    end
    firebase_put(firebase_table)
    file.close()

   
end

function setup()
    wifi.setmode(wifi.STATION)
    wifi.sta.config(wifi_ssid, wifi_password)
    while (wifi.sta.status() ~= 5 )
    do
        print(wifi.sta.status())
        tmr.delay(1000000)
    end
    
    print(wifi.sta.getip())
    
    
    start()
    
end

setup()
