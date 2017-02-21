function startup()
    if abort then
        print('startup aborted')
        return
    end
    print('in startup')
    dofile('user.lua')
end

print("safety timeout 2s to stop autorun")
abort = false
tmr.alarm(0,2000,0,startup)

