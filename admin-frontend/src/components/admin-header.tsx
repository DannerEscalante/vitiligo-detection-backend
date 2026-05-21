import { Bell, Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function AdminHeader() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-4 sm:px-6">
      <div>
        <p className="text-sm text-muted-foreground">Gestion clinica</p>
        <h2 className="text-lg font-semibold">Resumen operativo</h2>
      </div>
      <div className="hidden w-full max-w-sm items-center gap-2 md:flex">
        <Search className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
        <Input placeholder="Buscar paciente, doctor o cita" />
      </div>
      <Button variant="outline" size="icon" aria-label="Notificaciones">
        <Bell />
      </Button>
    </header>
  );
}
