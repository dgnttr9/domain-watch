export function Header() {
  return (
    <header className="mb-8 rounded-[2rem] bg-ink-950 px-6 py-6 text-white shadow-panel">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Domain Watch</p>
          <h1 className="mt-3 text-3xl font-semibold">Domain operations dashboard</h1>
          <p className="mt-3 max-w-2xl text-sm text-slate-300">
            Review domain health, imports, scheduler presets, exports, and provider logs in one clean control surface.
          </p>
        </div>
        <div className="rounded-2xl bg-white/10 px-4 py-3 text-sm text-slate-200 ring-1 ring-white/10">
          React + Vite + TypeScript frontend connected directly to the backend API.
        </div>
      </div>
    </header>
  );
}
