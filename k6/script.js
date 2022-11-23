import http from "k6/http";

// export const options = {};

const env = {
  url: __ENV.SCRIPT_URL,
};

export default function () {
  http.get(env.url);
}
