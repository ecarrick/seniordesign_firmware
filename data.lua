dofile("i2c.lua")
dofile("wifi.lua")

shot_num = 0

function firebase_put(data)

    -- set this to where you want to store each shot
    json_name = "My_Test"
    
    firebase_str = "https://shotanalytics-17fc3.firebaseio.com/" .. json_name .. "/shot" .. shot_num .. ".json"
    
    json = cjson.encode(data)
    http.put(firebase_str,
                nil,
                json,
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
    
    -- having trouble recording/sending more than about 20 samples
    data = record(calib, 20)

    json = cjson.encode(data)
    print(json)
    
    --uncomment next line to send recording to firebase
    --firebase_put(data)
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

start()
