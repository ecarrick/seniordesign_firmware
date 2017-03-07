dofile("i2c.lua")

dofile("wifi.lua")
function firebase_put(data)

    json = cjson.encode(data)
    http.put("https://shotanalytics-17fc3.firebaseio.com/test/data.json",
                nil,
                json,
                function(code,data)
                if (code < 0) then
                  print("HTTP request failed")
                else
                  print(code, data)
    end
  end)
end

function start()
    data = record(4000, 100)

    json = cjson.encode(data)
    print(json)
end

function setup()
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
