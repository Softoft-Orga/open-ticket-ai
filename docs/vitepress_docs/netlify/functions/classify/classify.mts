const QUEUE_EP = "https://uwlzdugezcmrk5vk.eu-west-1.aws.endpoints.huggingface.cloud";
const PRIORITY_EP = "https://rxnypflnfgdbgoxr.us-east-1.aws.endpoints.huggingface.cloud";

interface HFOutput {
    label: string;
    score: number;
}

interface RequestPayload {
    subject: string;
    body: string;
}

function constructModelInput(subject: string, body: string) {
    return {
        inputs: (subject + " ").repeat(2) + body,
        parameters: {},
    };
}

async function query<T>(endpoint: string, payload: object): Promise<T> {
    const res = await fetch(endpoint, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json() as Promise<T>;
}

async function predictQueue(subject: string, body: string): Promise<HFOutput[]> {
    return query<HFOutput[]>(QUEUE_EP, constructModelInput(subject, body));
}

async function predictPriority(subject: string, body: string): Promise<HFOutput[]> {
    return query<HFOutput[]>(PRIORITY_EP, constructModelInput(subject, body));
}

export default async (req: Request): Promise<Response> => {
    if (req.method !== "POST") {
        return new Response("Only POST allowed", {status: 405});
    }

    const {subject, body}: Partial<RequestPayload> = await req.json().catch(() => ({}));
    if (!subject || !body) {
        return new Response(JSON.stringify({error: "Missing subject/body"}), {
            status: 400,
            headers: {"Content-Type": "application/json"},
        });
    }

    try {
        const [queuePred, prioPred] = await Promise.all([
            predictQueue(subject, body),
            predictPriority(subject, body),
        ]);

        const best = (arr?: HFOutput[]) => (Array.isArray(arr) && arr.length > 0 ? arr[0] : null);

        const queue = best(queuePred);
        const priority = best(prioPred);

        return new Response(
            JSON.stringify({
                queue: queue?.label ?? null,
                queue_conf: queue?.score ?? null,
                priority: priority?.label ?? null,
                priority_conf: priority?.score ?? null,
            }),
            {headers: {"Content-Type": "application/json"}}
        );
    } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        return new Response(JSON.stringify({error: message}), {
            status: 500,
            headers: {"Content-Type": "application/json"},
        });
    }
};
