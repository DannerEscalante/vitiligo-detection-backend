"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { CalendarCheck, ClipboardList, LayoutDashboard, Stethoscope, UsersRound } from "lucide-react";

import { cn } from "@/lib/utils";

const navigation = [
  { name: "Resumen", href: "/dashboard", icon: LayoutDashboard },
  { name: "Citas", href: "/dashboard/citas", icon: CalendarCheck },
  { name: "Pacientes", href: "/dashboard/pacientes", icon: UsersRound },
  { name: "Doctores", href: "/dashboard/doctores", icon: Stethoscope },
  { name: "Tratamientos", href: "/dashboard/tratamientos", icon: ClipboardList }
];

export function AdminSidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-72 shrink-0 border-r bg-white lg:block">
      <div className="flex h-full flex-col">
        <div className="border-b px-6 py-5">
          <p className="text-sm font-medium text-muted-foreground">Panel gerente</p>
          <h1 className="mt-1 text-xl font-semibold text-foreground">Vitiligo Admin</h1>
        </div>
        <nav className="flex-1 space-y-1 px-4 py-6">
          {navigation.map((item) => {
            const isCurrent =
              item.href === "/dashboard"
                ? pathname === item.href
                : pathname.startsWith(item.href);

            return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isCurrent
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <item.icon className="h-4 w-4" aria-hidden="true" />
              {item.name}
            </Link>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
