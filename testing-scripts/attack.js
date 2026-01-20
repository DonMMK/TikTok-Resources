import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1000,       // 10 virtual users
  duration: '10s', // Test for 10 seconds (short burst)
};

export default function () {
  // We grab the URL from the command line environment variable
  const url = __ENV.TARGET_URL;

  if (!url) {
    console.error("ERROR: No URL provided. Use -e TARGET_URL=https://...");
    return;
  }

  const res = http.get(url);

  // We print the status code so you can see if WAF kicks in (403/429)
  check(res, { 
    'status was 200': (r) => r.status == 200,
    'status was blocked': (r) => r.status == 403 || r.status == 429 
  });
  
  sleep(0.1); // Wait 100ms between hits
}
