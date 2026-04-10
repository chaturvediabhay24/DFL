**FastAPI & API Engineering**

*Interview Q&A --- Deep Dive*

**FastAPI Internals**

1.  **How does FastAPI\'s dependency injection system work?**

> FastAPI\'s DI uses Python\'s function signature inspection. Any
> callable declared as a parameter with Depends(my_func) is called by
> FastAPI before the route handler, with its return value injected.
> Dependencies can themselves have dependencies (nested DI). This is
> used for: database session management (yield-based dependencies with
> cleanup), authentication (extract and validate JWT token), rate
> limiting, and feature flag resolution. yield-based dependencies act as
> context managers --- setup before yield, teardown after the response.

2.  **When should you use async def vs def in FastAPI routes?**

> async def: use when the route awaits IO-bound operations (DB queries
> via async driver, HTTP calls via httpx/aiohttp, Redis). FastAPI runs
> these in the event loop --- no thread overhead. def (sync): FastAPI
> runs these in a threadpool automatically, preventing them from
> blocking the event loop. Critical: never use sync blocking IO
> (requests.get, time.sleep) inside async def --- it blocks the entire
> event loop. Use asyncio.sleep for delays and async DB clients
> (asyncpg, motor) for async routes. For CPU-bound tasks (model
> inference), use sync def or offload to ProcessPoolExecutor.

3.  **Explain FastAPI middleware and give an ML use case.**

> Middleware wraps every request/response cycle. Defined with
> \@app.middleware(\'http\') or as Starlette BaseHTTPMiddleware. Use
> cases in ML APIs: (1) Request ID injection --- add X-Request-ID header
> to every request for distributed tracing. (2) Latency logging ---
> measure and log inference time per endpoint. (3) Authentication ---
> validate API keys before routing. (4) Rate limiting --- check Redis
> token bucket per API key. (5) Input sanitisation --- strip dangerous
> characters from user queries before LLM prompts.

4.  **How do you handle long-running ML inference in FastAPI?**

> Pattern 1 --- Async job queue: POST /infer returns a job_id
> immediately; worker (Celery, RQ, or Ray) processes the job; client
> polls GET /infer/{job_id}/status or uses webhooks. Pattern 2 ---
> Server-Sent Events (SSE): for streaming LLM responses, use
> StreamingResponse with an async generator that yields tokens as they
> are produced. Pattern 3 --- WebSockets: bidirectional streaming for
> interactive agents. Pattern 4 --- Background tasks: FastAPI\'s
> BackgroundTasks for lightweight post-response work (logging, cache
> warming) --- not for heavy inference.

**API Security**

5.  **Explain JWT authentication and how to implement it in FastAPI.**

> JWT (JSON Web Token) has three parts: header (algorithm), payload
> (claims: user_id, roles, exp), and signature (HMAC-SHA256 or RS256).
> Flow: client logs in → server generates signed JWT → client sends JWT
> in Authorization: Bearer \<token\> header. FastAPI implementation:
> OAuth2PasswordBearer defines the token URL; a
> Depends(get_current_user) dependency decodes and validates the JWT
> using python-jose or PyJWT, checking signature and expiry. Use RS256
> with public/private key pair in production (never share the signing
> key).

6.  **What is OAuth2 and how does it differ from API key
    authentication?**

> OAuth2 is an authorisation framework enabling third-party apps to
> access resources on behalf of a user without sharing credentials. It
> uses access tokens (short-lived) and refresh tokens (long-lived).
> Flows: Authorization Code (web apps), Client Credentials
> (machine-to-machine, common for ML API access), PKCE (mobile). API
> keys are simpler --- a static secret per client, passed in headers or
> query params. Use API keys for server-to-server ML API access where
> OAuth2 delegation is unnecessary. Use OAuth2 when user-level
> permissions and delegation are needed.

**Pydantic & Validation**

7.  **How do you use Pydantic for complex ML request/response
    validation?**

> Define BaseModel subclasses for request and response schemas. Use
> Field() for constraints (min_length, gt, pattern). Use validators
> (@field_validator) for custom logic (e.g., ensure feature vector
> length matches model input size). Use discriminated unions
> (Annotated\[Union\[\...\], Field(discriminator=\'type\')\]) for
> polymorphic request types (different model types have different
> feature schemas). Use response_model in route decorators to
> auto-filter and validate output --- prevents accidental PII leakage in
> responses.

**Performance & Observability**

8.  **How do you implement distributed tracing for a FastAPI ML
    service?**

> Use OpenTelemetry (OTEL) with the
> opentelemetry-instrumentation-fastapi package --- it auto-instruments
> all routes with spans. Add custom spans for model loading,
> preprocessing, and inference steps. Export traces to Jaeger or AWS
> X-Ray. Add trace_id to structured logs (JSON logging with structlog or
> python-json-logger) so logs and traces can be correlated. Include
> trace_id in error responses to the client for debugging. This is
> essential for diagnosing latency issues in multi-hop LLM pipelines
> (router → retrieval → LLM → postprocessing).
