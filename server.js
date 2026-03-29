const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const DIR = __dirname;

const mimeTypes = {
    '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css',
    '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.bin': 'application/octet-stream',
    '.glb': 'model/gltf-binary', '.gltf': 'model/gltf+json',
    '.tif': 'image/tiff', '.tiff': 'image/tiff',
    '.webp': 'image/webp', '.hdr': 'application/octet-stream'
};

http.createServer((req, res) => {
    const filePath = path.join(DIR, decodeURIComponent(req.url === '/' ? '/app.html' : req.url));
    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    // TIF dosya listesi API
    if (req.url === '/api/tif-list') {
        const site01 = path.join(DIR, 'Site01');
        fs.readdir(site01, (err, files) => {
            if (err) { res.writeHead(500); res.end('[]'); return; }
            const tifs = files.filter(f => /\.tiff?$/i.test(f)).map(f => {
                const s = fs.statSync(path.join(site01, f));
                return { name: f, size: s.size };
            });
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(tifs));
        });
        return;
    }

    fs.stat(filePath, (err, stat) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found: ' + req.url);
            return;
        }

        const range = req.headers.range;
        if (range) {
            const parts = range.replace(/bytes=/, '').split('-');
            const start = parseInt(parts[0], 10);
            const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
            res.writeHead(206, {
                'Content-Type': contentType,
                'Content-Range': `bytes ${start}-${end}/${stat.size}`,
                'Content-Length': end - start + 1,
                'Accept-Ranges': 'bytes'
            });
            fs.createReadStream(filePath, { start, end }).pipe(res);
        } else {
            res.writeHead(200, {
                'Content-Type': contentType,
                'Content-Length': stat.size,
                'Accept-Ranges': 'bytes'
            });
            fs.createReadStream(filePath).pipe(res);
        }
    });
}).listen(PORT, () => {
    console.log(`Server: http://localhost:${PORT}`);
});
