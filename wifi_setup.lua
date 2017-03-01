dofile("wifi.lua")
function firebase_put()
    test = {}
    test.fish = "fishes"
    test.fire = "hot"
    json = cjson.encode(test)
    http.put("https://shotanalytics-17fc3.firebaseio.com/test/",
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
    
    http.get("http://httpbin.org/ip", nil, function(code, data)
        if (code < 0) then
          print("HTTP request failed")
        else
          print(code, data)
        end
      end)

    firebase_put()

    
end

setup()
