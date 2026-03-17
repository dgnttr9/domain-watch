export function formatDate(value: string | null): string {
  if (!value) {
    return "Not available";
  }

  return new Intl.DateTimeFormat("en-GB", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function formatRelativeDays(value: number | null): string {
  if (value === null) {
    return "Unknown";
  }
  if (value < 0) {
    return `${Math.abs(value)} day overdue`;
  }
  if (value === 0) {
    return "Today";
  }
  return `${value} days`;
}
