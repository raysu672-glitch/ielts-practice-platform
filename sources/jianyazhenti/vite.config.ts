import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import fs from 'node:fs'
import type { IncomingMessage, ServerResponse } from 'node:http'

const DATA_ROOT = path.resolve(import.meta.dirname, 'exam-data')
const APP_BASE = '/jianyazhenti/'

function contentType(ext: string) {
  const types: Record<string, string> = {
    '.json': 'application/json; charset=utf-8',
    '.html': 'text/html; charset=utf-8',
    '.mp3': 'audio/mpeg',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
  }
  return types[ext] || 'application/octet-stream'
}

function sendFile(res: ServerResponse, file: string) {
  res.setHeader('Content-Type', contentType(path.extname(file).toLowerCase()))
  fs.createReadStream(file).pipe(res)
}

function examDataMiddleware() {
  return (req: IncomingMessage, res: ServerResponse, next: () => void) => {
    try {
      const urlPath = decodeURIComponent((req.url || '/').split('?')[0])

      if (urlPath === '/catalog.json' || urlPath === 'catalog.json') {
        const books = fs
          .readdirSync(DATA_ROOT, { withFileTypes: true })
          .filter((d) => d.isDirectory() && /^academic\d+$/.test(d.name))
          .map((d) => {
            const id = Number(d.name.replace('academic', ''))
            const manifestPath = path.join(DATA_ROOT, d.name, 'manifest.json')
            let label = `ACADEMIC ${id}`
            let scrapedAt = ''
            if (fs.existsSync(manifestPath)) {
              try {
                const m = JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
                label = m.label || label
                scrapedAt = m.scrapedAt || ''
              } catch {
                /* ignore */
              }
            }
            return { bookId: id, folder: d.name, label, scrapedAt }
          })
          .sort((a, b) => b.bookId - a.bookId)
        res.setHeader('Content-Type', 'application/json; charset=utf-8')
        res.end(JSON.stringify({ books }))
        return
      }

      const file = path.normalize(path.join(DATA_ROOT, urlPath.replace(/^\//, '')))
      if (!file.startsWith(DATA_ROOT)) {
        res.statusCode = 403
        res.end('Forbidden')
        return
      }
      if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        next()
        return
      }
      sendFile(res, file)
    } catch {
      next()
    }
  }
}

function examDataPlugin(): Plugin {
  return {
    name: 'exam-data-static',
    configureServer(server) {
      server.middlewares.use('/exam-data', examDataMiddleware())
    },
    configurePreviewServer(server) {
      server.middlewares.use('/exam-data', examDataMiddleware())
    },
  }
}

export default defineConfig({
  base: APP_BASE,
  plugins: [react(), examDataPlugin()],
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, 'src'),
    },
  },
  server: {
    port: 5173,
    fs: {
      allow: [path.resolve(import.meta.dirname)],
    },
  },
})
