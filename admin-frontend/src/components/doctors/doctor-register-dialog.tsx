"use client";

import { useState } from "react";
import { AlertCircle, Calendar, Check, Copy, Key, Loader2, Mail, User, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { createDoctorAdmin } from "@/lib/doctors-api";
import type { DoctorRegistrationPayload, DoctorRegistrationResult } from "@/types/doctors";

interface DoctorRegisterDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function DoctorRegisterDialog({ isOpen, onClose, onSuccess }: DoctorRegisterDialogProps) {
  const [nombre, setNombre] = useState("");
  const [sexo, setSexo] = useState("masculino");
  const [fechaNacimiento, setFechaNacimiento] = useState("");
  const [email, setEmail] = useState("");
  const [contrasenaTemporal, setContrasenaTemporal] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successResult, setSuccessResult] = useState<DoctorRegistrationResult | null>(null);
  const [copied, setCopied] = useState(false);

  if (!isOpen) {
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    if (!nombre.trim() || !fechaNacimiento || !email.trim()) {
      setError("Por favor completa todos los campos obligatorios.");
      setIsLoading(false);
      return;
    }

    const payload: DoctorRegistrationPayload = {
      nombre,
      sexo,
      fecha_nacimiento: fechaNacimiento,
      email
    };

    if (contrasenaTemporal.trim()) {
      payload.contrasena_temporal = contrasenaTemporal;
    }

    try {
      const result = await createDoctorAdmin(payload);
      setSuccessResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al registrar el doctor.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!successResult) return;
    try {
      await navigator.clipboard.writeText(successResult.contrasena_temporal);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
    }
  };

  const handleCloseSuccess = () => {
    // Resetear formulario
    setNombre("");
    setSexo("masculino");
    setFechaNacimiento("");
    setEmail("");
    setContrasenaTemporal("");
    setSuccessResult(null);
    setError(null);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-lg rounded-xl border bg-white shadow-2xl transition-all duration-300">
        
        {/* Encabezado */}
        <div className="flex items-center justify-between border-b px-6 py-4">
          <h2 className="text-lg font-semibold text-slate-800">
            {successResult ? "Registro Exitoso" : "Registrar Nuevo Doctor"}
          </h2>
          {!isLoading && (
            <Button
              variant="ghost"
              size="icon"
              onClick={successResult ? handleCloseSuccess : onClose}
              className="text-slate-400 hover:bg-slate-100 hover:text-slate-600"
            >
              <X className="h-5 w-5" />
            </Button>
          )}
        </div>

        {/* Contenido */}
        <div className="p-6">
          {error && (
            <div className="mb-4 flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <div>{error}</div>
            </div>
          )}

          {successResult ? (
            /* Pantalla de éxito con contraseña temporal */
            <div className="space-y-6 text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600">
                <Check className="h-6 w-6" />
              </div>

              <div className="space-y-2">
                <h3 className="text-md font-medium text-slate-900">
                  ¡Cuenta de Doctor Creada Correctamente!
                </h3>
                <p className="text-sm text-slate-500 px-4">
                  El médico ya puede iniciar sesión en la aplicación móvil con sus credenciales.
                </p>
              </div>

              {/* Caja de credenciales */}
              <div className="rounded-lg border bg-slate-50 p-4 text-left space-y-3">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Correo de acceso
                  </span>
                  <div className="mt-0.5 font-medium text-slate-700">{successResult.email}</div>
                </div>

                <hr className="border-slate-200" />

                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Contraseña temporal
                  </span>
                  <div className="mt-1 flex items-center justify-between gap-3">
                    <code className="rounded bg-slate-200 px-2.5 py-1 text-sm font-mono font-bold text-slate-800 tracking-wider">
                      {successResult.contrasena_temporal}
                    </code>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleCopy}
                      className="gap-2 text-xs"
                    >
                      {copied ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-green-600" />
                          ¡Copiado!
                        </>
                      ) : (
                        <>
                          <Copy className="h-3.5 w-3.5 text-slate-500" />
                          Copiar clave
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </div>

              <div className="text-xs text-amber-600 bg-amber-50 rounded-lg p-3 text-left border border-amber-200">
                <strong>Importante:</strong> Asegúrate de copiar la contraseña temporal ahora. Por seguridad, no podrá visualizarse de nuevo en el panel gerencial. El doctor deberá actualizarla manualmente en su primer inicio de sesión desde la app móvil.
              </div>

              <Button onClick={handleCloseSuccess} className="w-full">
                Entendido y Finalizar
              </Button>
            </div>
          ) : (
            /* Formulario de registro */
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Nombre */}
              <div className="space-y-1.5">
                <Label htmlFor="nombre">Nombre completo *</Label>
                <div className="relative">
                  <User className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <Input
                    id="nombre"
                    required
                    placeholder="Dr. Carlos Mendoza"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>

              {/* Email */}
              <div className="space-y-1.5">
                <Label htmlFor="email">Correo Electrónico *</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <Input
                    id="email"
                    type="email"
                    required
                    placeholder="carlos.mendoza@clinica.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>

              {/* Sexo y Fecha de Nacimiento */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label htmlFor="sexo">Sexo</Label>
                  <select
                    id="sexo"
                    value={sexo}
                    onChange={(e) => setSexo(e.target.value)}
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                  >
                    <option value="masculino">Masculino</option>
                    <option value="femenino">Femenino</option>
                    <option value="otro">Otro</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="fechaNacimiento">Fecha de Nacimiento *</Label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                    <Input
                      id="fechaNacimiento"
                      type="date"
                      required
                      value={fechaNacimiento}
                      onChange={(e) => setFechaNacimiento(e.target.value)}
                      className="pl-9"
                    />
                  </div>
                </div>
              </div>

              {/* Contraseña temporal (Opcional) */}
              <div className="space-y-1.5">
                <Label htmlFor="contrasenaTemporal" className="flex items-center gap-1.5">
                  Contraseña Temporal
                  <span className="text-xs text-slate-400 font-normal">(Opcional)</span>
                </Label>
                <div className="relative">
                  <Key className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <Input
                    id="contrasenaTemporal"
                    type="text"
                    placeholder="Dejar vacío para autogenerar"
                    value={contrasenaTemporal}
                    onChange={(e) => setContrasenaTemporal(e.target.value)}
                    className="pl-9"
                  />
                </div>
                <p className="text-xs text-slate-400">
                  Si no se especifica, el sistema generará una contraseña segura aleatoria de 8 caracteres.
                </p>
              </div>

              {/* Botones */}
              <div className="flex justify-end gap-3 pt-4 border-t">
                <Button type="button" variant="outline" onClick={onClose} disabled={isLoading}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={isLoading} className="gap-2">
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Registrando...
                    </>
                  ) : (
                    "Registrar Doctor"
                  )}
                </Button>
              </div>
            </form>
          )}
        </div>

      </div>
    </div>
  );
}
