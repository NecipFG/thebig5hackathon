# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DM1 Moon Station ("DM1 Ay Istasyonu") - A browser-based 3D terrain visualization tool for lunar/planetary GeoTIFF surface data. The UI and code comments are in Turkish.

## Running the Project

```bash
node server.js
# Opens at http://localhost:8080 (serves 3d_V1.3.html by default)
```

No build step, no package manager. All dependencies are loaded via CDN in the HTML files.

## Architecture

The project consists of standalone HTML pages with inline JS — no modules, no bundler.

### Active Files

- **3d_V1.3.html** — Current version. The main application served by default. Three.js-based 3D terrain viewer with:
  - GeoTIFF loading and terrain mesh generation (solid box with side walls and edge alpha fade)
  - Two-point distance measurement along the terrain surface
  - Wall-E vehicle animation that follows the surface path between marked points
  - Three camera modes: free orbit, 3rd-person follow, 1st-person follow
  - Black-and-white (lunar) color mode toggle
  - Bilinear elevation interpolation for fast surface-following (`getTerrainY`)
- **index.html** — Alternative viewer using CesiumJS with a lunar ellipsoid globe (requires Cesium Ion token)
- **3d-viewer.html** — Earlier standalone Three.js terrain viewer (simpler, no vehicle animation)
- **server.js** — Minimal Node.js static file server (no dependencies). Handles MIME types for .glb, .gltf, .tif, and standard web formats.

### Version History

`3d_V1.1.html` → `3d_V1.2.html` → `3d_V1.3.html` are iterative versions. Only V1.3 is actively served.

### Data & Assets

- **Site01/** — GeoTIFF terrain data files (.tif, .xyzi, .tgz). `*_surf.tif` = surface elevation, `*_slp.tif` = slope, `*_ldec.tif` = local declination. Resolution: 5m per pixel (`PIXEL_SIZE = 5`).
- **Assets/WALLE.glb** — Optimized GLB model used for vehicle animation (auto-scaled to ~8 scene units on load)
- **Assets/wall-e/** — Source GLTF model with separate textures
- **wall-e.glb** — Root-level copy of the GLB model (63MB)

## Key Technical Details

- Three.js r128 (legacy non-module build via CDN, uses `THREE.PlaneBufferGeometry`, `THREE.GLTFLoader` from examples)
- GeoTIFF.js v2.1.3 via CDN for client-side .tif parsing
- Terrain is downsampled to max 512x512 grid when source is larger (`step = ceil(max(w,h) / 512)`)
- Height scale is computed dynamically: `heightScale = (terrainSize * 0.3) / elevationRange`
- Vehicle speed constant: 1000 m/s (`VEHICLE_SPEED`)
- Edge fade uses custom shader patching via `onBeforeCompile` to inject per-vertex alpha attributes
- The terrain group is lifted so min elevation sits at Y=50, base at Y=0
