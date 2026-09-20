import { createServer } from "node:http";
import { readFile } from "node:fs/promises";

const fixture = await readFile(new URL("./fixtures/portal.html", import.meta.url));
createServer((request, response) => {
  const path = new URL(request.url, "http://127.0.0.1:8765").pathname;
  if (path === "/health") {
    response.writeHead(200).end("ok");
  } else if (path === "/portal.html") {
    response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" }).end(fixture);
  } else {
    response.writeHead(404).end("Not found");
  }
}).listen(8765, "127.0.0.1");
