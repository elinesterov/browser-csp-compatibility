var EXPECT_BLOCK = true;
var EXPECT_LOAD = false;
var INJECT_IFRAME = 'iframe';
var INJECT_FRAME = 'frame';

var iframe;
var checkResultsTimeout = 500;

function injectFrame(policy, header, frame_type, shouldBlock) {

    window.onload = function () {
        iframe = document.createElement('iframe');
        // iframe.onload = iframeLoaded(shouldBlock);
        /* BUG:
           because of issue with iframe.onload https://bugzilla.mozilla.org/show_bug.cgi?id=444165
           it doesn't work properly in Firefox :( seems when Firefox blocks URL loading
           due to CSP violation, behavior is exactly the same as in issue above.
        */
        var alertUrlPath = shouldBlock ? '/alert/pass' : '/alert/fail'
        var injection = header ? '?header=true' : '?meta=true'
        var url = alertUrlPath + injection + '&policy=' + policy;

        iframe.src = url;
        document.body.appendChild(iframe);
        setTimeout(function(){checkIframeTestResults(shouldBlock);}, checkResultsTimeout);
    };
}


function checkIframeTestResults(expectBlock){
    if (expectBlock && typeof window.top.__test === 'undefined'){
        testPassed('iFrame should be blocked and was blocked');
    } else if (expectBlock && typeof window.top.__test !== 'undefined'){
        testFailed('iFrame should be blocked but was not');
    } else if (!expectBlock && typeof window.top.__test !== 'undefined'){
        testPassed('iFrame should be loaded and it was');
    } else if (!expectBlock && typeof window.top.__test === 'undefined'){
        testFailed('iFrame should be loaded but  it was not');
    }

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