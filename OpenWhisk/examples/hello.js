// wsk action create helloJS hello.js
// wsk action invoke helloJS --result --param name world
function main({ name }) {
  return {
    greeting: `Hello ${name || "unknown"}`,
  };
}
