import http from "k6/http";
import { sleep } from "k6";
import { SharedArray } from "k6/data";

// export const options = {};

const env = {
  // URL to post data
  url: __ENV.SCRIPT_URL,
  // Sleep for duration, in seconds
  sleepFor: Number(__ENV.SCRIPT_SLEEP_FOR),
  // File containing an JSON array of payloads
  dataset: __ENV.SCRIPT_DATASET,
};

const data = new SharedArray(env.dataset, function () {
  return JSON.parse(open(env.dataset));
});

function postData(url, payload) {
  return http.post(url, JSON.stringify(payload), {
    headers: { "Content-Type": "application/json" },
  });
}

export default function () {
  for (const payload of data) {
    const response = postData(env.url, payload);
    // From https://community.k6.io/t/log-request-url-and-body-for-failing-requests/1464
    if (response.status >= 400) {
      console.error({
        request: { url: env.url, payload },
        response: { status: response.status, body: response.request.body },
      });
    }
    sleep(env.sleepFor);
  }
}
