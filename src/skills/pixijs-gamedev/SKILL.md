---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-pixijs-gamedev
  name: pixijs-gamedev
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "PixiJS 2D rendering and game development — sprites, animation loops, interaction, and WebGL/Canvas rendering."
  category: framework
  layer: null
  when_to_use: "Use when building PixiJS apps, creating 2D games, integrating sprites and animations, or implementing interactive graphics in the browser."
---

# PixiJS Game Development

## Level 1 — Intro

PixiJS renders 2D scenes through a display-object tree (`Application`
holds a `stage` `Container`, which holds `Sprite`s, `Graphics`, and
nested `Container`s). Drive updates from the `Ticker`, load assets
through `Assets`, and reach for `ParticleContainer` only when raw
batch performance matters.

## Level 2 — Overview

### Application setup

Create an `Application`, `await app.init({...})`, then append
`app.canvas` to the DOM. Pass `resizeTo: window` for a responsive
canvas, `antialias: true` for smoother edges, and
`resolution: window.devicePixelRatio` plus `autoDensity: true` for
sharp HiDPI rendering. PixiJS picks WebGL by default and falls back
to Canvas automatically.

### Sprites and textures

Load textures via `Assets.load('hero.png')` (returns a promise) and
construct sprites with `new Sprite(texture)` or `Sprite.from(texture)`.
Set `anchor.set(0.5)` to center the origin so rotation and scaling
behave intuitively. `Assets` caches by URL — loading the same source
twice is free. Use `Texture.EMPTY` as a placeholder while assets are
still loading.

### Display hierarchy

`Container` is the base group: children inherit position, scale,
rotation, and alpha from their parent. Set `sortableChildren = true`
on a container and assign `zIndex` to children to control draw order.
Remove off-screen objects from the stage rather than just hiding them.
Use `ParticleContainer` for thousands of identical sprites — it
trades features for raw throughput.

### Animation and the ticker

Drive everything from `app.ticker.add((ticker) => { ... })`. The
`ticker.deltaTime` value is normalized to 1.0 at the target FPS so
movement stays frame-rate independent. Use `AnimatedSprite` for
spritesheet animations and control `animationSpeed` independently of
the main ticker. For complex tweening, integrate GSAP rather than
hand-rolling easing.

### Interaction and events

Set `eventMode = 'static'` on any display object that should receive
pointer events, then attach handlers with `.on('pointerdown', ...)`.
The same events fire for mouse and touch. Custom hit regions go on
`hitArea` (Circle, Rectangle, Polygon). The drag pattern is
`pointerdown` on the sprite → `pointermove` on the stage → `pointerup`
on the stage. Disable interaction on non-interactive children to keep
hit-testing fast.

### Graphics and effects

`new Graphics()` exposes vector primitives — `rect`, `circle`,
`moveTo`/`lineTo`, `roundRect` — with chainable `fill()` and
`stroke()` calls. For static shapes that you'll reuse, render once to
a texture with `app.renderer.generateTexture()`. Apply filters via
`displayObject.filters = [new BlurFilter(...)]`; chain filters by
adding them to the array in order. Filters are GPU-intensive — use
them sparingly on mobile.

### Asset loading

Use `Assets.add({ alias, src })` then `Assets.load(alias)` for named
assets, or define bundles with `Assets.addBundle('game', {...})` and
`await Assets.loadBundle('game')`. Bundle loading reports progress
via a callback. Supported formats: PNG, JPG, WebP, SVG, JSON
(spritesheets), and audio via plugins. Preload critical assets before
showing the game; lazy-load secondary assets in the background.

## Level 3 — Full reference

### Application boilerplate

```js
import { Application, Assets, Sprite, Container, Graphics, Text } from 'pixi.js';

const app = new Application();
await app.init({
  width: 800,
  height: 600,
  background: '#1a1a2e',
  antialias: true,
  resolution: window.devicePixelRatio || 1,
  autoDensity: true,
});
document.body.appendChild(app.canvas);
```

### Core classes

| Class               | Purpose                                  | Key properties                                  |
|---------------------|------------------------------------------|-------------------------------------------------|
| `Application`       | Entry point, manages renderer and ticker | `stage`, `ticker`, `screen`, `canvas`           |
| `Sprite`            | Displays a texture                       | `texture`, `anchor`, `tint`, `alpha`            |
| `Container`         | Groups display objects                   | `children`, `sortableChildren`, `zIndex`        |
| `Graphics`          | Vector drawing                           | `rect()`, `circle()`, `fill()`, `stroke()`      |
| `Text`              | Renders text                             | `text`, `style`, `resolution`                   |
| `AnimatedSprite`    | Frame-based animation                    | `textures`, `animationSpeed`, `currentFrame`    |
| `ParticleContainer` | High-performance sprite batch            | `maxSize`, `properties`                         |
| `Ticker`            | Game loop manager                        | `deltaTime`, `FPS`, `speed`                     |

### Asset loading patterns

```js
// Single asset
const texture = await Assets.load('hero.png');
const sprite = new Sprite(texture);

// Bundled assets
Assets.addBundle('level1', {
  background: 'bg.png',
  tileset: 'tiles.json',
  music: 'theme.mp3',
});
await Assets.loadBundle('level1');

// With progress tracking
Assets.loadBundle('level1', (progress) => {
  console.log(`Loading: ${Math.round(progress * 100)}%`);
});
```

### Sprite operations

```js
const sprite = Sprite.from(texture);
sprite.anchor.set(0.5);           // Center origin
sprite.position.set(400, 300);    // Set position
sprite.scale.set(2);              // Uniform scale
sprite.rotation = Math.PI / 4;    // Rotate 45 degrees
sprite.alpha = 0.8;               // Semi-transparent
sprite.tint = 0xff6b6b;           // Color tint
sprite.eventMode = 'static';      // Enable interaction
sprite.cursor = 'pointer';        // Pointer cursor
```

### Game loop

```js
app.ticker.add((ticker) => {
  // ticker.deltaTime = 1.0 at 60fps, scales with frame time
  sprite.x += speed * ticker.deltaTime;
  sprite.rotation += 0.01 * ticker.deltaTime;
});

// Control ticker
app.ticker.speed = 0.5;   // Half speed
app.ticker.stop();         // Pause
app.ticker.start();        // Resume
```

### Drag pattern

```js
let dragging = false;
sprite.eventMode = 'static';
sprite.on('pointerdown', () => { dragging = true; });

app.stage.eventMode = 'static';
app.stage.hitArea = app.screen;
app.stage.on('pointermove', (e) => {
  if (dragging) sprite.position.copyFrom(e.global);
});
app.stage.on('pointerup', () => { dragging = false; });
```

### Graphics drawing

```js
const g = new Graphics();
g.rect(0, 0, 200, 100).fill({ color: 0x3498db, alpha: 0.8 });
g.circle(100, 100, 50).fill(0xe74c3c).stroke({ color: 0xffffff, width: 2 });
g.moveTo(0, 0).lineTo(200, 200).stroke({ color: 0x2ecc71, width: 3 });
g.roundRect(10, 10, 180, 80, 12).fill(0x9b59b6);
```

### Text rendering

```js
const text = new Text({
  text: 'Score: 0',
  style: {
    fontFamily: 'Arial',
    fontSize: 36,
    fontWeight: 'bold',
    fill: 0xffffff,
    stroke: { color: 0x000000, width: 4 },
    dropShadow: { color: 0x000000, blur: 4, distance: 2 },
  },
});
text.anchor.set(0.5);
```

### AnimatedSprite from spritesheet

```js
import { AnimatedSprite, Spritesheet } from 'pixi.js';

const sheet = await Assets.load('character.json');
const walkFrames = sheet.animations['walk']; // array of textures
const character = new AnimatedSprite(walkFrames);
character.animationSpeed = 0.15;
character.play();

// Control
character.stop();
character.gotoAndPlay(0);
character.loop = true;
character.onComplete = () => { /* animation finished */ };
```

### Object pooling

```js
const pool = [];
function getSprite(texture) {
  const sprite = pool.pop() || new Sprite(texture);
  sprite.visible = true;
  return sprite;
}
function releaseSprite(sprite) {
  sprite.visible = false;
  pool.push(sprite);
}
```

### Scene management

```js
const scenes = { menu: new Container(), game: new Container() };
function switchScene(name) {
  Object.values(scenes).forEach(s => s.visible = false);
  scenes[name].visible = true;
}
app.stage.addChild(scenes.menu, scenes.game);
switchScene('menu');
```

### Performance tips

- Use `ParticleContainer` for 10k+ identical sprites
- Each filter forces a render-texture pass — limit them
- Pool and reuse objects rather than creating/destroying every frame
- Texture atlases reduce draw calls (PixiJS batches automatically)
- Always call `destroy()` on removed display objects to free GPU
  memory
- Avoid frequent `blendMode` changes — they break batching
- Profile with `app.ticker.FPS` and the browser DevTools Performance
  tab

### Further reading

- [PixiJS Documentation](https://pixijs.download/release/docs/)
- [PixiJS Examples](https://pixijs.io/examples/)
