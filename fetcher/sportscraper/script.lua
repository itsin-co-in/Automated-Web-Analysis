function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(1))  -- Wait for 1 second

    -- Define JavaScript function to check if the loading overlay is present
    local checkOverlay = splash:jsfunc([[
        function () {
            var overlay = document.querySelector('.LoadingOverlay_loader__iZ0Nm');
            return overlay && window.getComputedStyle(overlay).getPropertyValue('display') === 'none';
        }
    ]])

    -- Wait until the loading overlay is removed or until a timeout occurs
    local end_time = os.time() + 10  -- Set end time for waiting (10 seconds)
    while os.time() < end_time do
        if splash:evaljs(checkOverlay()) then
            return {
                html = splash:html(),
            }
        else
            splash:wait(0.5)  -- Wait for 0.5 seconds before checking again
        end
    end

    -- If the loading overlay is still present after the timeout, return an empty response
    return {
        html = '',
    }
end
