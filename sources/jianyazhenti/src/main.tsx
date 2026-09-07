import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { APP_BASE, markEmbedded } from './lib/embed'
import './index.css'

markEmbedded()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter basename={APP_BASE || undefined}>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
