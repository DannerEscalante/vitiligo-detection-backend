import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function TratamientosPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Tratamientos</CardTitle>
        <CardDescription>Base para consultar tratamientos y predicciones IA.</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">Modulo pendiente de conexion con el backend.</p>
      </CardContent>
    </Card>
  );
}
