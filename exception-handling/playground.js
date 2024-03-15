var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var DatabaseError = /** @class */ (function (_super) {
    __extends(DatabaseError, _super);
    function DatabaseError(message) {
        var _this = _super.call(this, message) || this;
        _this.name = 'DatabaseError';
        return _this;
    }
    return DatabaseError;
}(Error));
var NetworkError = /** @class */ (function (_super) {
    __extends(NetworkError, _super);
    function NetworkError(message) {
        var _this = _super.call(this, message) || this;
        _this.name = 'NetworkError';
        return _this;
    }
    return NetworkError;
}(Error));
// Simulate different operations that might fail
function performDatabaseOperation() {
    // Logic that might fail
    throw new DatabaseError('Failed to connect to the database');
}
function performNetworkRequest() {
    // Logic that might fail
    throw new NetworkError('Failed to reach the server');
}
// Use in a real-life scenario
try {
    // This might be a part of your application logic where errors can occur
    performDatabaseOperation();
    performNetworkRequest();
}
catch (error) {
    // Check the instance of the error
    if (error instanceof DatabaseError) {
        console.error('A database error occurred:', error.message);
        // Handle database error
    }
    else if (error instanceof NetworkError) {
        console.error('A network error occurred:', error.message);
        // Handle network error
    }
    else {
        console.error('An unexpected error occurred:', error);
        // Handle generic error
    }
}
