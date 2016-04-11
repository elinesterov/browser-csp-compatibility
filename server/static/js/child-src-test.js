var EXPECT_BLOCK = true;
var EXPECT_LOAD = false;
var iframe;

function injectFrame(url, shouldBlock) {
    window.onload = function () {
        iframe = document.createElement('iframe');
        iframe.onload = iframeLoaded(shouldBlock);
        /* BUG:
           because of issue with iframe.onload https://bugzilla.mozilla.org/show_bug.cgi?id=444165
           it doesn't work properly in Firefox :( seems when Firefox blocks URL loading
           due to CSP violation, behavior is exactly the same as in issue above.
        */
        //iframe.onerror = console.log('onerror fired');//iframeLoaded(console.log('onerror fired'));
        iframe.src = url;
        document.body.appendChild(iframe);
    };
}

function iframeLoaded(expectBlock) {
    return function(ev) {
        var failed = true;
        try {
            console.log("IFrame load event fired: the IFrame's location is '" + ev.target.contentWindow.location.href + "'.");
            if (expectBlock) {
                testFailed("The IFrame should have been blocked (or cross-origin). It wasn't.");
                failed = true;
            } else {
                testPassed("The IFrame should not have been blocked. It wasn't.");
                failed = false;
            }
        } catch (ex) {
            console.log("IFrame load event fired: the IFrame is cross-origin (or was blocked).");
            if (expectBlock) {
                testPassed("The IFrame should have been blocked (or cross-origin). It was.");
                failed = false;
            } else {
                testFailed("The IFrame should not have been blocked. It was.");
                failed = true;
            }
        }
        finishJSTest();
    };
}

function injectFrameRedirectingTo(url, shouldBlock) {
    //need to do some redirect
    injectFrame("/security/contentSecurityPolicy/resources/redir.php?url=" + url, shouldBlock);
}

function shouldThrow(worker, error){
    if (typeof worker === 'undefined' || error === true) {
        testPassed('Worker is Blocked');
    }
    else {
        testFailed('Worker is not Blocked but it should');
    }
}

function shouldNotThrow(worker, error){
    if (typeof worker === 'undefined' || error === true) {
        
        testFailed('Worker is not Blocked but it should');
    }
    else {
        testPassed('Worker is Blocked');
    }
}

function injectWorker(url, expectBlock) {

    window.onload = function() {

        var got_error = false;
        var checkResultsTimeout = 500;

        try{
            var worker = new Worker(url);
            /*  BUG: ???
                request to create a worker from URL /js/alert/<state>
                will be blocked if not allowed by CSP policy, but in Firefox 
                worker object is created successfully. Though it's code execution is blocked.
                To workaround, I didn't find better solution that catch error via worker.onerror
                and then, after checkResultsTimeout, check if error has been thrown.
                That slows down test, but I don't see a better alternative at this point
                Also the fact that I rely on variable passed to eval is not a god idea :(
            */
            worker.onerror = function(err){
                if (err.message.indexOf('Failed to load script') != -1){
                    got_error = true;
                }
            };
        }
        catch (e) {
            console.log('exception thrown ', e);
        }

        setTimeout(checkResults, checkResultsTimeout)

        function checkResults(){
            if (expectBlock == EXPECT_BLOCK){
                shouldThrow(worker, got_error);
            }
            else{
                shouldNotThrow(worker, got_error);
            }
        }

        finishJSTest();
    };
}

function injectSharedWorker(url, expectBlock) {
    window.onload = function() {
        if (expectBlock == EXPECT_BLOCK)
            shouldThrow("var w = new SharedWorker('" + url + "');");
        else
            shouldNotThrow("var w = new SharedWorker('" + url + "');");
        finishJSTest();
    };
}

function testPassed(message){
    console.log("PASSED " + message);
    addTestReults('Pass');
}

function testFailed(message){
    console.log("Failed " + message);
    addTestReults('Fail');
}

function finishJSTest(){
    console.log("TEST COMPLETE");
}
