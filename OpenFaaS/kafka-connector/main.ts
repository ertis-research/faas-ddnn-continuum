import { Kafka } from "npm:kafkajs@2.2.4";
import {
  getConfig,
  EnvExtractor,
  JsonExtractor,
} from "https://deno.land/x/chimera@v1.0.29/mod.ts";
import { z } from "https://deno.land/x/zod@v3.21.0/mod.ts";

const CONFIG_SCHEME = z.object({
  brokers: z.string().array(),
  topic: z.string(),
  callback: z.object({
    url: z.string().transform((x) => new URL(x)),
    options: z.any().default({}),
  }),
});

const configAny = await getConfig({
  extractors: [
    new JsonExtractor<z.infer<typeof CONFIG_SCHEME>>("/etc/kafkac/config.json"),
    new EnvExtractor<z.infer<typeof CONFIG_SCHEME>>("kafkac_"),
  ],
});
const config = CONFIG_SCHEME.parse(configAny);
console.info(config);

const kafka = new Kafka({
  brokers: config.brokers,
  clientId: "openfaas-kafka-connector",
});
const consumer = kafka.consumer({ groupId: "openfaas-kafka-connector" });
await consumer.connect();
await consumer.subscribe({ topics: [config.topic] });

Deno.addSignalListener("SIGTERM", async () => {
  await consumer.disconnect();
  Deno.exit();
});

async function handle({ topic, partition, message, heartbeat, pause }: any) {
  const valueStr = message.value.toString();
  const payload = JSON.parse(valueStr);
  const response = await fetch(config.callback.url, {
    ...config.callback.options,
    body: JSON.stringify({
      ...message,
      key: message.key?.toString(),
      value: payload.value,
    }),
  });
  return {
    timestamp: new Date(),
    status: response.status,
    body: await response.text(),
  };
}

await consumer.run({
  // deno-lint-ignore require-await
  eachMessage: async (payload: unknown) => {
    handle(payload)
      .then((x) => console.info(x))
      .catch((x) => console.error(x));
  },
});
