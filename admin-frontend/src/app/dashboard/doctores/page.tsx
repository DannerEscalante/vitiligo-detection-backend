import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function DoctoresPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Doctores</CardTitle>
        <CardDescription>Base para disponibilidad y asignacion medica.</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">Modulo pendiente de conexion con el backend.</p>
      </CardContent>
    </Card>
  );
}
