// Checking conditions
// Method 1: Using if-else
function ifElseMethod() {
    var start = new Date().getTime();
    var x = 1;
    if (x === 1) {
        console.log('x is 1');
    } else if (x === 2) {
        console.log('x is 2');
    } else if (x === 3) {
        console.log('x is 3');
    } else {
        console.log('x is not 1, 2 or 3');
    }
    var end = new Date().getTime();
    console.log('Time taken by if-else method: ' +
        (end - start) + 'ms');
}

// Method 2: Using switch-case
function switchCaseMethod() {
    var start = new Date().getTime();
    var x = 1;
    switch (x) {
        case 1:
            console.log('x is 1');
            break;
        case 2:
            console.log('x is 2');
            break;
        case 3:
            console.log('x is 3');
            break;
        default:
            console.log('x is not 1, 2 or 3');
    }
    var end = new Date().getTime();
    console.log('Time taken by switch-case method: ' +
        (end - start) + 'ms');
}

ifElseMethod();
switchCaseMethod();
