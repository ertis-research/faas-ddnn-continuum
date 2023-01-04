import http from "k6/http";
import exec from "k6/execution";
import { SharedArray } from "k6/data";

const env = {
  // URL to post data
  url: __ENV.SCRIPT_URL,
  // File containing an JSON array of payloads
  dataset: __ENV.SCRIPT_DATASET,
  duration: __ENV.SCRIPT_DURATION,
  rate: Number(__ENV.SCRIPT_RATE),
  timeUnit: __ENV.SCRIPT_TIMEUNIT,
};

export const options = {
  scenarios: {
    lambda: {
      executor: "constant-arrival-rate",
      duration: env.duration,
      rate: env.rate,
      timeUnit: env.timeUnit,
      preAllocatedVUs: 1,
      maxVUs: 1,
    },
  },
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
  const payload = data[exec.vu.iterationInScenario];
  const response = postData(env.url, payload);
  // From https://community.k6.io/t/log-request-url-and-body-for-failing-requests/1464
  if (response.status >= 400) {
    console.error({
      request: { url: env.url, payload },
      response: { status: response.status, body: response.request.body },
    });
  } else {
    console.log("OK");
  }
}
