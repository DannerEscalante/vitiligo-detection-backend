import { CalendarCheck, Stethoscope, UsersRound, ClipboardList } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card";

interface KpiCardsProps {
  pendingAppointments: number;
  totalPatients: number;
  totalDoctors: number;
  totalTreatmentsRegistered: number;
}

const items = [
  {
    key: "pendingAppointments",
    label: "Citas pendientes",
    icon: CalendarCheck
  },
  {
    key: "totalPatients",
    label: "Pacientes registrados",
    icon: UsersRound
  },
  {
    key: "totalDoctors",
    label: "Doctores disponibles",
    icon: Stethoscope
  },
  {
    key: "totalTreatmentsRegistered",
    label: "Tratamientos registrados",
    icon: ClipboardList
  }
] as const;

export function KpiCards({
  pendingAppointments,
  totalPatients,
  totalDoctors,
  totalTreatmentsRegistered
}: KpiCardsProps) {
  const values = {
    pendingAppointments,
    totalPatients,
    totalDoctors,
    totalTreatmentsRegistered
  };

  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {items.map((item) => (
        <Card key={item.key}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardDescription>{item.label}</CardDescription>
            <item.icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-semibold">{values[item.key]}</p>
          </CardContent>
        </Card>
      ))}
    </section>
  );
}
