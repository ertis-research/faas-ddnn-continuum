import { Kafka, logLevel } from "npm:kafkajs@2.2.4";
import {
  getConfig,
  EnvExtractor,
  JsonExtractor,
} from "https://deno.land/x/chimera@v1.1.0/mod.ts";
import { z } from "https://deno.land/x/zod@v3.21.0/mod.ts";
import * as log from "https://deno.land/std@0.151.0/log/mod.ts";

const CONFIG_SCHEME = z.object({
  brokers: z.string().array(),
  topic: z
    .string()
    .array()
    .or(z.string().transform((x) => [x])),
  clientid: z.string().default("kafka-connector"),
  groupid: z.string().default("kafka-connector"),
  callback: z.object({
    url: z.string().transform((x) => new URL(x)),
    retries: z.number().min(0).default(5),
    retrySleep: z.number().positive().optional(),
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
log.info({ config });

const kafka = new Kafka({
  brokers: config.brokers,
  clientId: config.clientid,
  logCreator:
    () =>
    ({ level, label, ...kafkajs }: any) => {
      switch (level) {
        case logLevel.ERROR:
          log.error({ kafkajs });
          break;
        case logLevel.WARN:
          log.warning({ kafkajs });
          break;
        case logLevel.INFO:
          log.info({ kafkajs });
          break;
        default:
          log.debug({ kafkajs });
      }
    },
});
const consumer = kafka.consumer({ groupId: config.groupid });
await consumer.connect();
await consumer.subscribe({ topics: config.topic });

Deno.addSignalListener("SIGTERM", async () => {
  await consumer.disconnect();
});

async function handle({ topic, partition, message, heartbeat, pause }: any) {
  const headers = Object.fromEntries(
    Object.entries(message.headers).map(([key, value]: any) => [
      key,
      value.toString(),
    ])
  );

  const attempts = [];
  for (let i = 0; i <= config.callback.retries; i++) {
    const response = await fetch(config.callback.url, {
      ...config.callback.options,
      body: JSON.stringify({
        ...message,
        key: message.key?.toString(),
        value: JSON.parse(message.value),
        headers,
      }),
    });
    attempts.push({
      timestamp: new Date(),
      status: response.status,
      body: await response.text(),
    });
    if (response.ok) {
      break;
    }
    if (config.callback.retrySleep) {
      await new Promise((resolve) =>
        setTimeout(resolve, config.callback.retrySleep)
      );
    }
  }
  return attempts;
}

await consumer.run({
  eachMessage: (payload: unknown) => {
    handle(payload)
      .then((response) => log.info({ response }))
      .catch((response) => log.error({ response }));
  },
});
