# Vitiligo Admin Frontend

Frontend administrativo para gerente del sistema de seguimiento de pacientes con vitiligo.

## Stack

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui compatible structure

## Ejecutar

```bash
cd admin-frontend
npm install
npm run dev
```

Configura la URL del backend en `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Esta app se mantiene separada del backend FastAPI para no modificar modelos, rutas ni contratos usados por la app movil.
