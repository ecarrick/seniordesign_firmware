dofile("data.lua")

-- a button press can trigger an interrupt and be monitored for a continued press
-- wired to two pins
gpio.mode(0, gpio.INPUT, gpio.PULLUP)
gpio.mode(8, gpio.INT, gpio.PULLUP)

-- setup pwm for LED
pwm.setup(5, 500, 512)
pwm.setup(6, 500, 512)
pwm.setup(7, 500, 512)
pwm.start(5)
pwm.start(6)
pwm.start(7)

-- function to operate LED (PWM is 10bit, so 255 => 1023)
color = {RED = {}, YELLOW = {}, GREEN = {}, BLUE = {}, OFF = {}}
color.RED = {750, 0, 0}
color.YELLOW = {750, 750, 0}
color.GREEN = {0, 750, 0}
color.BLUE = {0, 0, 750}
color.OFF = {0, 0, 0}
function LED(color)
    pwm.setduty(5, color[1])
    pwm.setduty(6, color[2])
    pwm.setduty(7, color{3})
end

-- interrupt function, if pb is not held down a shot will begin recording
function pbpress(level, time)
    tmr.delay(1000000)
    if gpio.read(0) then begin_shot()
    else    goto_config()
    end
end

gpio.trig(8, "low", pbpress)
