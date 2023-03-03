// Create the application helper and add its render target to the page
let app = new PIXI.Application({
  width: 800,
  height: 640,
  background: '#1099bb',
});
let root = document.getElementsByClassName("pixi-canvas");
if (root.length > 0) {
  root[0].appendChild(app.view);
} else {
  console.error(`Where's "pixi-canvas"?`)
}


const container = new PIXI.Container();
app.stage.addChild(container);

const thickness = 2;
const line_color = 0xffffff;

const y_cell = 64;
const y_lines = 5;
const width = y_cell * y_lines;
let template = new PIXI.Graphics();
for (let y = 0; y <= y_lines; ++y) {
  template
  .lineStyle(thickness, line_color)
  .moveTo(0, y * y_cell)
  .lineTo(width, y * y_cell);
}

const x_cell = 64;
const x_lines = 5;
const height = x_cell * x_lines;
for (let x = 0; x <= x_lines; ++x) {
  template
  .lineStyle(thickness, line_color)
  .moveTo(x * x_cell, 0)
  .lineTo(x * x_cell, height);
}

// // Create a 5x5 grid of bunnies
// for (let i = 0; i < 25; i++) {
//   const bunny = new PIXI.Sprite(texture);
//   bunny.anchor.set(0.5);
//   bunny.x = (i % 5) * 40;
//   bunny.y = Math.floor(i / 5) * 40;
//   container.addChild(bunny);
// }

container.addChild(template);

// Move container to the center
container.x = app.screen.width / 2;
container.y = app.screen.height / 2;

// Center bunny sprite in local container coordinates
container.pivot.x = container.width / 2;
container.pivot.y = container.height / 2;

// Create the sprite and add it to the stage
let robot = PIXI.Sprite.from('robot-64.png');
robot.x = 0;
robot.y = 0;
container.addChild(robot);

// // Add a ticker callback to move the sprite back and forth
// let elapsed = 0.0;
// app.ticker.add((delta) => {
//   elapsed += delta;
//   sprite.x =  100.0 + Math.cos(elapsed/50.0) * 100.0;
// });