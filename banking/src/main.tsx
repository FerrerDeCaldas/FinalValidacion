import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import './lib/namespace'
import { DirectionProvider } from './components/ui/direction.tsx'


const root = createRoot(document.getElementById('root') as HTMLElement)

function renderApp(layoutDirection: string) {
  root.render(
    <StrictMode>
      <DirectionProvider dir={layoutDirection}>
        <App />
      </DirectionProvider>
    </StrictMode>,
  )
}

function renderError(message: string) {
  root.render(
    <StrictMode>
      <div style={{ padding: 24, fontFamily: 'system-ui, sans-serif' }}>
        <h1>Error cargando la app</h1>
        <p>{message}</p>
      </div>
    </StrictMode>,
  )
}

if (import.meta.env.DEV) {
  fetch('/api/method/erpnext.www.banking.get_context_for_dev', {
    method: 'POST',
  }).then(response => response.json()).then((values) => {
    if (!window.frappe) window.frappe = {};
    //@ts-expect-error - frappe will be available
    frappe.boot = JSON.parse(values.message.boot);
    //@ts-expect-error - frappe will be available
    frappe._messages = frappe.boot["__messages"];

    // Set document direction to rtl
    document.dir = values.message.layout_direction;
    //@ts-expect-error - frappe will be available
    frappe.model.sync(frappe.boot.docs);
    renderApp(values.message.layout_direction)

  }).catch((error) => {
    console.error('Failed to fetch dev context', error)
    renderError('No se pudo cargar el contexto de desarrollo. Revisa que el servidor Frappe/ERPNext esté disponible y que el proxy esté configurado en el puerto correcto.')
  })
} else {
  //@ts-expect-error - frappe will be available
  frappe.model.sync(frappe.boot.docs);
  createRoot(document.getElementById('root') as HTMLElement).render(
    <StrictMode>
      <DirectionProvider dir={window.frappe?.boot?.layout_direction ?? 'ltr'}>
        <App />
      </DirectionProvider>
    </StrictMode>,
  )
}
