import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface BarReportCardProps {
  title: string;
  description: string;
  emptyText: string;
  rows: Array<{
    label: string;
    value: number;
  }>;
}

export function BarReportCard({ title, description, emptyText, rows }: BarReportCardProps) {
  const maxValue = Math.max(...rows.map((row) => row.value), 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        {rows.length === 0 ? (
          <div className="rounded-md border border-dashed p-5 text-sm text-muted-foreground">
            {emptyText}
          </div>
        ) : (
          <div className="space-y-4">
            {rows.slice(0, 6).map((row) => {
              const width = maxValue > 0 ? `${Math.max((row.value / maxValue) * 100, 8)}%` : "8%";

              return (
                <div key={row.label} className="space-y-2">
                  <div className="flex items-center justify-between gap-4 text-sm">
                    <span className="truncate font-medium">{row.label}</span>
                    <span className="text-muted-foreground">{row.value}</span>
                  </div>
                  <div className="h-2 rounded-full bg-muted">
                    <div className="h-2 rounded-full bg-primary" style={{ width }} />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
