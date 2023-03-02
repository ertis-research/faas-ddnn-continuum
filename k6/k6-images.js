import http from "k6/http";
import { b64encode } from "k6/encoding";
import { SharedArray } from "k6/data";

const env = {
  // URL to post data
  url: __ENV.SCRIPT_URL,
  // File containing an JSON array of payloads
  files: __ENV.SCRIPT_FILES,
};

export const options = {
  scenarios: {
    lambda: {
      executor: "ramping-arrival-rate",
      preAllocatedVUs: 500,
      timeUnit: "1s",
      stages: [{ duration: "2m", target: 30 }],
    },
  },
};

const data = new SharedArray(env.dataset, function () {
  return JSON.parse(open(env.files))
    .map((filename) => open(filename, "b"))
    .map((file) => b64encode(file));
});

function postData(url, payload) {
  return http.post(url, JSON.stringify(payload), {
    headers: { "Content-Type": "application/json" },
  });
}

export default function () {
  const image = data[Math.floor(Math.random() * data.length)];
  const payload = { image };
  const response = postData(env.url, payload);
  // From https://community.k6.io/t/log-request-url-and-body-for-failing-requests/1464
  if (response.status >= 400) {
    console.error({
      request: { url: env.url, image },
      response: { status: response.status, body: response.request.body },
    });
  } else {
    console.log("OK");
  }
}
