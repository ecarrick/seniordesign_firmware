function time()
    timezone = -4
    request=string.char(227,0,6,236,0,0,0,0,0,0,0,0,49,78,49,52,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    
    time = 0
    sk=net.createConnection(net.UDP, 0)
    sk:on("receive", function(sck, payload)
        print("YAY!")
        local highw,loww,ntpstamp
        highw = payload:byte(41) * 256 + payload:byte(42)
        loww = payload:byte(43) * 256 + payload:byte(44)
        ntpstamp=( highw * 65536 + loww ) + ( timezone* 3600)
        time = ntpstamp - 1104494400 - 1104494400
        print(time)
     
        sck:close()
    
    end )
end

time()