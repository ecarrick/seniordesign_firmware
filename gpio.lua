dofile("data.lua")

-- a button press can trigger an interrupt and be monitored for a continued press
-- wired to two pins
gpio.mode(5, gpio.INT, gpio.PULLUP)
gpio.mode(3, gpio.OUTPUT)

flash = true
    
-- interrupt function, if pb is not held down a shot will begin recording
function pbpress(level, time)
    tmr.delay(1000000)
    if gpio.read(5)==1 then print("Start")
    else    print("Held")
    end
    flash = false
end

gpio.trig(5, "down", pbpress)
on = false
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
tmr.alarm(0,500,0,flip)
