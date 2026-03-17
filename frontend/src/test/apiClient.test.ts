import { apiClient } from "../services/apiClient";

describe("apiClient", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns domains from typed API response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              status: "success",
              message: "Domains retrieved.",
              data: [
                {
                  id: 1,
                  domain: "openai.com",
                  status: "active",
                  provider_used: "rdap",
                  expiration_date: null,
                  days_left: null,
                  last_checked_at: null,
                  next_check_at: null,
                  scheduler_enabled: false,
                  scheduler_preset: null,
                  last_error_message: null,
                },
              ],
              errors: [],
            }),
            { status: 200, headers: { "Content-Type": "application/json" } },
          ),
        ),
      ),
    );

    const domains = await apiClient.getDomains();
    expect(domains[0].domain).toBe("openai.com");
  });
});
