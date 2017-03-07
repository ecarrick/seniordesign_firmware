dofile("wifi.lua")
function firebase_put()

    json = cjson.encode(test)
    http.put("https://shotanalytics-17fc3.firebaseio.com/test/data146.json",
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

function setup()
    wifi.sta.config(wifi_ssid, wifi_password)
    while (wifi.sta.status() ~= 5 )
    do
        print(wifi.sta.status())
        tmr.delay(1000000)
    end
    
    print(wifi.sta.getip())
    
    
    firebase_put()

    
end

--setup()
