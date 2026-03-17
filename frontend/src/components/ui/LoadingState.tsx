export function LoadingState() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white px-4 py-5 shadow-panel">
      <div className="animate-pulse space-y-3">
        <div className="h-4 w-40 rounded-full bg-slate-200" />
        <div className="h-3 w-full rounded-full bg-slate-100" />
        <div className="h-3 w-11/12 rounded-full bg-slate-100" />
        <div className="h-3 w-10/12 rounded-full bg-slate-100" />
      </div>
    </div>
  );
}
