// Create the application helper and add its render target to the page
let app = new PIXI.Application({ width: 800, height: 640 });
let root = document.getElementsByClassName("pixi-canvas");
if (root.length > 0) {
  root[0].appendChild(app.view);
} else {
  console.error(`Where's "pixi-canvas"?`)
}

// Create the sprite and add it to the stage
let sprite = PIXI.Sprite.from('robot.png');
sprite.y = 50;
app.stage.addChild(sprite);

// Add a ticker callback to move the sprite back and forth
let elapsed = 0.0;
app.ticker.add((delta) => {
  elapsed += delta;
  sprite.x =  100.0 + Math.cos(elapsed/50.0) * 100.0;
});