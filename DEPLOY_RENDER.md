# Deploying CargoProof on Render

The included `render.yaml` creates four services in Singapore:

- `cargoproof-dashboard`: public static dashboard.
- `cargoproof-api`: public Node API.
- `cargoproof-verification-engine`: FastAPI rules engine.
- `cargoproof-evidence-api`: FastAPI simulated-evidence API.

The Blueprint uses public service URLs so it works on Render's free plan, which does not support private services. No URL is hardcoded: Render injects each dependent service's URL during Blueprint sync. The static-site build writes the API's public URL to `frontend/config.js`. Local development is unchanged because that file is blank in Git and the frontend retains its `localhost:4021` fallback.

## Deploy

1. Push these changes to the repository branch you want to deploy.
2. In Render, select **New > Blueprint** and choose this repository. Render detects `render.yaml` at the repository root.
3. Create the Blueprint and wait for all four health checks to become healthy.
4. Open the `cargoproof-dashboard` URL.

The Blueprint intentionally uses `DEMO_MODE=true`, so no wallet or x402 signing secret is required. The evidence service reseeds its synthetic SQLite database each time it starts, which is appropriate for this demo and avoids relying on Render's ephemeral filesystem.

## Enabling real x402 payments

On `cargoproof-api`, change `DEMO_MODE` to `false` and add these Render secret environment variables: `PAY_TO` and either `AVM_PRIVATE_KEY_BASE64` or `AVM_MNEMONIC`. Add optional `GEMINI_API_KEY` or `GROQ_API_KEY` only if assistant wording should use an LLM. Never commit these values.
