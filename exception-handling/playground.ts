class DatabaseError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'DatabaseError';
  }
}

class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

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
} catch (error) {
  // Check the instance of the error
  if (error instanceof DatabaseError) {
    console.error('A database error occurred:', error.message);
    // Handle database error
  } else if (error instanceof NetworkError) {
    console.error('A network error occurred:', error.message);
    // Handle network error
  } else {
    console.error('An unexpected error occurred:', error);
    // Handle generic error
  }
}
