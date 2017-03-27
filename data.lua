dofile("i2c.lua")
dofile("wifi.lua")

shot_num = 0
sample_num = 0

function firebase_put(data)
    -- set this to where you want to store each shot
    json_name = "testdata"
    
    firebase_str = "https://shotanalytics-17fc3.firebaseio.com/" .. json_name .. "/shot" .. shot_num .. "/sample" .. sample_num .. ".json"
    print(firebase_str)
    print(data)
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
    sample_num = sample_num + 1
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
    sample_num = 1
    file_name = "test.txt"
    -- first parameter is number of values to record
    record_to_file(3, file_name)
    file.open(file_name)

    while true do
        line = file.readline()
        if (line == nil) then break
        end
        value_count = 1
        value_table = {}
        for val in string.gmatch(line, "-?%d+") do
            value_table[value_count] = val
            value_count = value_count + 1
            --print(val)
        end
        firebase_put(value_table)
        tmr.wdclr()
    end
    file.close()
    shot_num = shot_num + 1

end

function setup()
    wifi.setmode(wifi.STATION)
    wifi.sta.config(station_cfg.ssid, station_cfg.pwd)
    while (wifi.sta.status() ~= 5 )
    do
        print(wifi.sta.status())
        tmr.delay(1000000)
    end
    print(wifi.sta.getip())
end


