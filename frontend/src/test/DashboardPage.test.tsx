import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { App } from "../app/App";

const domainsResponse = {
  status: "success",
  message: "Domains retrieved.",
  data: [
    {
      id: 1,
      domain: "openai.com",
      status: "active",
      provider_used: "rdap",
      expiration_date: "2026-07-01T00:00:00Z",
      days_left: 30,
      last_checked_at: "2026-03-17T08:00:00Z",
      next_check_at: "2026-03-18T08:00:00Z",
      scheduler_enabled: true,
      scheduler_preset: "daily",
      last_error_message: null,
    },
  ],
  errors: [],
};

const logsResponse = {
  status: "success",
  message: "Logs retrieved.",
  data: [
    {
      id: 1,
      level: "INFO",
      scope: "domain_check",
      message: "Domain check completed for openai.com.",
      domain_id: 1,
      run_id: 1,
      metadata_json: {
        provider_attempts: [{ provider: "rdap", status: "active" }],
      },
      created_at: "2026-03-17T08:00:00Z",
    },
  ],
  errors: [],
};

describe("DashboardPage", () => {
  beforeEach(() => {
    vi.spyOn(window, "open").mockImplementation(() => null);
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL) => {
        const url = input.toString();

        if (url.includes("/domains") && !url.includes("/exports")) {
          if (url.includes("/recheck")) {
            return Promise.resolve(
              new Response(JSON.stringify({ ...domainsResponse, data: domainsResponse.data[0] }), {
                status: 200,
                headers: { "Content-Type": "application/json" },
              }),
            );
          }
          return Promise.resolve(
            new Response(JSON.stringify(domainsResponse), {
              status: 200,
              headers: { "Content-Type": "application/json" },
            }),
          );
        }

        if (url.includes("/logs")) {
          return Promise.resolve(
            new Response(JSON.stringify(logsResponse), {
              status: 200,
              headers: { "Content-Type": "application/json" },
            }),
          );
        }

        if (url.includes("/imports")) {
          return Promise.resolve(
            new Response(
              JSON.stringify({
                status: "success",
                message: "Import completed.",
                data: {
                  id: 7,
                  source_type: "txt",
                  file_name: null,
                  total_rows: 2,
                  valid_rows: 1,
                  invalid_rows: 1,
                  status: "completed",
                  error_summary: "1 row(s) failed validation.",
                },
                errors: [],
              }),
              {
                status: 200,
                headers: { "Content-Type": "application/json" },
              },
            ),
          );
        }

        return Promise.resolve(
          new Response(JSON.stringify({ status: "success", message: "ok", data: {}, errors: [] }), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          }),
        );
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("renders dashboard data from backend responses", async () => {
    render(<App />);

    await waitFor(() => expect(screen.getAllByText("openai.com").length).toBeGreaterThan(0));
    expect(screen.getByText("Domain operations dashboard")).toBeInTheDocument();
    expect(screen.getByText("Domain check completed for openai.com.")).toBeInTheDocument();
  });

  it("allows changing log severity filter", async () => {
    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => expect(screen.getAllByText("openai.com").length).toBeGreaterThan(0));
    await user.selectOptions(screen.getByLabelText("Level"), "ERROR");

    expect(screen.getByLabelText("Level")).toHaveValue("ERROR");
  });

  it("shows import feedback and export info", async () => {
    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => expect(screen.getAllByText("openai.com").length).toBeGreaterThan(0));
    await user.type(screen.getByLabelText("Bulk domain list"), "openai.com");
    await user.click(screen.getByRole("button", { name: "Import text" }));

    await waitFor(() => expect(screen.getByText(/Text import completed\./)).toBeInTheDocument());
    expect(screen.getByText("Last import summary")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Download CSV" }));
    expect(screen.getByText("CSV export download started.")).toBeInTheDocument();
  });
});
