export default {
    content: ["./index.html", "./src/**/*.{ts,tsx}"],
    theme: {
        extend: {
            colors: {
                ink: {
                    950: "#0f172a",
                    900: "#172033",
                    800: "#243247",
                },
                mist: {
                    50: "#f8fafc",
                    100: "#f1f5f9",
                    200: "#e2e8f0",
                },
                signal: {
                    success: "#0f9f6e",
                    warning: "#d97706",
                    danger: "#dc2626",
                    neutral: "#475569",
                },
            },
            boxShadow: {
                panel: "0 18px 40px rgba(15, 23, 42, 0.08)",
            },
            backgroundImage: {
                "hero-grid": "radial-gradient(circle at top left, rgba(15,23,42,0.08), transparent 30%), linear-gradient(135deg, rgba(255,255,255,0.95), rgba(241,245,249,0.98))",
            },
        },
    },
    plugins: [],
};
